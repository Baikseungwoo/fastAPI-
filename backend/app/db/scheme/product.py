from pydantic import BaseModel


class ProductCreate(BaseModel):
    pro_category: str
    pro_name: str
    pro_price: int


class ProductUpdate(BaseModel):
    pro_category: str | None = None
    pro_name: str | None = None
    pro_price: int | None = None


class ProductResponse(BaseModel):
    pro_id: int
    fac_id: int
    pro_category: str
    pro_name: str
    pro_price: int

    class Config:
        from_attributes = True
