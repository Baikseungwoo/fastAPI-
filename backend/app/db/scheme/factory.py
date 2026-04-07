from pydantic import BaseModel, EmailStr


class FactoryCreate(BaseModel):
    fac_name: str
    fac_email: EmailStr
    fac_size: str | None = None
    fac_pw: str


class FactoryLogin(BaseModel):
    fac_email: EmailStr
    fac_pw: str


class FactoryUpdate(BaseModel):
    fac_name: str | None = None
    fac_email: EmailStr | None = None
    fac_size: str | None = None
    fac_pw: str | None = None


class FactoryResponse(BaseModel):
    fac_id: int
    fac_name: str
    fac_email: EmailStr
    fac_size: str | None = None

    class Config:
        from_attributes = True


class FactoryTokenResponse(BaseModel):
    access_token: str
    token_type: str
