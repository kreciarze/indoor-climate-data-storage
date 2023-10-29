from pydantic import BaseModel


class UserData(BaseModel):
    login: str
    password: str


class UserBearerToken(BaseModel):
    user_bearer_token: str
