from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import  TIMESTAMP, func, ForeignKey
# from .user import User
# from .product import Product

class Purchase(Base):
    __tablename__="purchase"
    pur_id:Mapped[int]=mapped_column(primary_key=True, index=True)
    use_id:Mapped[int]=mapped_column(ForeignKey("user.use_id"), nullable=False)
    pro_id:Mapped[int]=mapped_column(ForeignKey("product.pro_id"), nullable=False)
    pur_date:Mapped[datetime]=mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )

    # user: Mapped["User"]=relationship("User", back_populates="carts")
    # product: Mapped["Product"]=relationship("Product", back_populates="carts")