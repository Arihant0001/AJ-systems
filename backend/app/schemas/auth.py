from pydantic import BaseModel, EmailStr


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class SignupIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    token: str
    new_password: str
