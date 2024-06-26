from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class userDB(UserSchema):
    id: int


class userList(BaseModel):
    users: list[UserPublic]  # para retornar uma lista de public
