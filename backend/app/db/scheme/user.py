from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    use_id: int
    use_name: str
    use_email: str
    use_password: str


class CreateUser(BaseModel):
    use_name: str
    use_email: str
    use_password: Annotated[str, Field(max_length=72)]


class LoginUser(BaseModel):
    use_name: str
    use_password: str


class UserInDB(UserBase):
    use_id: int
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True


class ReadUser(UserInDB):
    pass


class UpdateEmail(BaseModel):
    old_email: str
    new_email: Annotated[str, EmailStr]


class UpdatePassword(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=8, max_length=72)]


class DeleteUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # Router reads `delete_data.password`; alias keeps backward compatibility
    # with clients that still send `use_password`.
    password: str = Field(alias="use_password")
