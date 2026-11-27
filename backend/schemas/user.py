from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    batch_or_graduation: str | None = Field(default=None, max_length=50)
    headline: str | None = Field(default=None, max_length=150)
    bio: str | None = Field(default=None, max_length=1000)
    linkedin_url: str | None = Field(default=None, max_length=300)


class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)