from sqlalchemy import Integer, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
from datetime import datetime
from typing import Optional

class User(Base):
    __tablename__='user'
    use_id:Mapped[int]=mapped_column(Integer, primary_key=True, autoincrement=True)
    use_name:Mapped[str]=mapped_column(String(50), nullable=False)
    use_email:Mapped[str]=mapped_column(String(100), unique=True, nullable=False)
    use_password:Mapped[str]=mapped_column(String(100), nullable=False)
    use_joined_at:Mapped[datetime]=mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    refresh_token:Mapped[str]=mapped_column(String(300), nullable=True)