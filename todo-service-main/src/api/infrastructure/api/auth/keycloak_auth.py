from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakOpenIDConnection
from domain.users import UserLogin, UserRegister
from fastapi import HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import logging

module_logger = logging.getLogger(__name__)

class KeycloakSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="keycloak_")
    client_id: str
    server_url: str
    realm_name: str
    client_secret_key: str


keycloak_openid = KeycloakOpenID(**KeycloakSettings().model_dump(), verify=False)


class KeycloakSettingsAdmin(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="keycloak_")
    server_url: str
    realm_name: str
    realm_admin_username: str
    realm_admin_password: str
    client_id: str
    client_secret_key: str


admin_settings = KeycloakSettingsAdmin()
keycloak_admin_connection = KeycloakOpenIDConnection(
    server_url=admin_settings.server_url.replace("/auth", ""),
    realm_name=admin_settings.realm_name,
    username=admin_settings.realm_admin_username,
    password=admin_settings.realm_admin_password,
    client_id=admin_settings.client_id,
    client_secret_key=admin_settings.client_secret_key,
    verify=False,
)
keycloak_admin = KeycloakAdmin(connection=keycloak_admin_connection)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_user(user: UserRegister):
    module_logger.debug(user)
    try:
        keycloak_admin.create_user(
            {
                "email": user.email,
                "username": user.username,
                "enabled": True,
                "firstName": "None",
                "lastName": "None",
                "credentials": [
                    {
                        "value": user.password,
                        "type": "password",
                    }
                ],
            },
            exist_ok=False,
        )
    except Exception as e:
        module_logger.error("Failed to create user", user, e)
        raise HTTPException(status_code=401, detail="User already exists")


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        user_info = keycloak_openid.decode_token(token)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_token(user: UserLogin):
    try:
        token_raw = keycloak_openid.token(
            username=user.username, password=user.password, scope="offline_access"
        )
        return token_raw["access_token"], token_raw["refresh_token"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def get_current_user(token: str):
    try:
        user_info = keycloak_openid.decode_token(token)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def refresh_token(token: str):
    try:
        new_token = keycloak_openid.refresh_token(token)
        return new_token
    except Exception as e:
        module_logger.error("Error refreshing_token", e.args, token)
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def get_user_roles(token: str = Depends(oauth2_scheme)):
    try:

        token_info = keycloak_openid.decode_token(
            token,
        )
        return token_info.get("realm_access", {}).get("roles", [])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


def role_checker(roles: List[str] = Depends(get_user_roles)):
    if "readonly" in roles:
        raise HTTPException(
            status_code=403, detail=f"Forbidden"
        )
    return True
