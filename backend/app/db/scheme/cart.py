from pydantic import BaseModel
from datetime import datetime

class CartBase(BaseModel):
    pro_id:int

class CartCreate(CartBase):
    pass 

class CartInDb(CartBase):
    car_id:int
    created_at:datetime
    use_id:int

    class Config:
        from_attributes = True

class CartRead(CartInDb):
    pass