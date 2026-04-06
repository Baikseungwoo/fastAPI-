from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Factory(Base):
    __tablename__ = "Factory"

    fac_id = Column(Integer, primary_key=True, index=True)
    fac_name = Column(String(50), nullable=False)
    fac_email = Column(String(50), nullable=False)
    fac_size = Column(String(5), nullable=True)
    fac_password = Column(String(50), nullable=False)

    products = relationship("Product", back_populates="factory")



