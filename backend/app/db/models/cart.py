from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import  TIMESTAMP, func, ForeignKey
# from .user import User

class Cart(Base):
    __tablename__="cart"
    car_id:Mapped[int]=mapped_column(primary_key=True, index=True)
    use_id:Mapped[int]=mapped_column(ForeignKey("user.use_id"), nullable=False)
    pro_id:Mapped[int]=mapped_column(ForeignKey("product.pro_id"), nullable=False)
    created_at:Mapped[datetime]=mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )

    # user: Mapped["User"]=relationship("User", back_populates="carts")