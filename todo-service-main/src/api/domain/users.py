from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str 
    email: str
    password: str


class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    confirmPassword: str


class RefreshUserData(BaseModel):
    refresh_token: str