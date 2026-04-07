from pydantic import BaseModel
from datetime import datetime

class PurchaseBase(BaseModel):
    pro_id:int

class PurchaseCreate(PurchaseBase):
    pass 

class PurchaseInDb(PurchaseBase):
    pur_id:int
    pur_date:datetime
    use_id:int

    class Config:
        from_attributes = True

class PurchaseRead(PurchaseInDb):
    pass