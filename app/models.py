from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text

from app.database import Base

class Product(Base):
    __tablename__ = "user"
    id = Column(Integer, nullable=False, primary_key=True)
    product_name=Column(String,nullable=False)
    inventory=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    product_type=Column(String,nullable=False)
    discount_status=Column(Boolean,nullable=False,server_default=text('false'))
    discount_percent=Column(Integer,nullable=False,server_default=text('0'))
    warehouse_pin=Column(Integer,nullable=False)
