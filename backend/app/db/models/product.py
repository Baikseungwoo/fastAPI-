from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Product(Base):
    __tablename__ = "product"

    pro_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fac_id = Column(Integer, ForeignKey("factory.fac_id"), nullable=False)
    pro_category = Column(String(50), nullable=False)
    pro_name = Column(String(50), nullable=False)
    pro_price = Column(Integer, nullable=False)

    factory = relationship("Factory", back_populates="products")
