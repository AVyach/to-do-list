from fastapi.routing import APIRouter
from domain.users import UserLogin
from domain.users import UserRegister, RefreshUserData
from fastapi.responses import JSONResponse
from infrastructure.api.auth.keycloak_auth import create_user
from infrastructure.api.auth.keycloak_auth import get_current_user, get_token, refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])




@router.post("/register")

def register(
    user: UserRegister
):
    """
    Fastapi endpoint for registering users

    Args:
        user (UserRegister): user object which contains user data when user is registered.

    Raises:
        HTTPException: if errors occured while registraging

    Returns:
        JSONResponse: if user registered successfully.
    """

    create_user(user)
    return JSONResponse(
        content={"message": "Пользователь успешно зарегистрирован."},
        status_code=200,
    )


@router.post("/token")
def login_for_access_token(
    user: UserLogin
):
    """
    Fastapi endpoint for authenticating

    Args:
        user (UserLogin): User object that contains email and password.

    Raises:
        HTTPException: Raised when error occurs in auth service.

    Returns:
       JSONResponse: JSON object that contains access token and user data.
    """
    token, refresh_token = get_token(user)
    user_info = get_current_user(token)
    return JSONResponse(
        content=  {
            "access_token": token,
            "refresh_token": refresh_token,
            "status_code":200,
            "token_type": "bearer",
            "user": {
                "username": user_info.get("preferred_username"),
                "email": user_info.get("email"),
                "id": user_info.get("sub")
            }

            })

    

@router.post("/token/refresh")
def get_new_token(data: RefreshUserData):
    raw_token = refresh_token(data.refresh_token)
    return JSONResponse(
        content=  {
            "access_token": raw_token["access_token"],
            "refresh_token": raw_token["refresh_token"],
            "status_code":200,
            "token_type": "bearer",
            })