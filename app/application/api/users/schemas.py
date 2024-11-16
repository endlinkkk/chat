from pydantic import BaseModel, model_validator


class SignUpRequestSchema(BaseModel):
    username: str
    phone: str
    password1: str
    password2: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "SignUpRequestSchema":
        if self.password1 != self.password2:
            raise ValueError("passwords do not match")
        return self


class ConfirmCodeRequestSchema(BaseModel):
    phone: str
    code: str


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserResponseSchema(BaseModel):
    username: str
    phone: str


class SignInRequestSchema(BaseModel):
    phone: str
    password: str
