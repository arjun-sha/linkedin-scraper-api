from pydantic import BaseModel


class AuthModel(BaseModel):
    x_api_key: str


class ProfileModel(AuthModel):
    email: str
    password: str


class ConnectionsModel(ProfileModel):
    pagination_id: str = None
