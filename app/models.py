


from sqlalchemy import Boolean, Column, Integer, Nullable, String, TIMESTAMP, text,ForeignKey

from app.database import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, nullable=False, primary_key=True)
    product_name=Column(String,nullable=False)
    inventory=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    product_type=Column(String,nullable=False)
    discount_status=Column(Boolean,nullable=False,server_default=text('false'))
    discount_percent=Column(Integer,nullable=False,server_default=text('0'))
    warehouse_pincode=Column(Integer,nullable=False)
    price=Column(Integer,nullable=False,server_default=text('100'))



class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,nullable=False,)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    user_pincode=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    wallet=Column(Integer,server_default=text('0'),nullable=False)
    completed_order=Column(Integer,server_default=text('0'),nullable=False)
    pending_order=Column(Integer,server_default=text('0'),nullable=False)
    failed_order=Column(Integer,server_default=text('0'),nullable=False)
    role=Column(String,nullable=False,server_default=text("'customer'"))



class Order(Base):
    __tablename__="order"
    order_id=Column(Integer,primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey("user.id",ondelete='CASCADE'),nullable=False)
    product_id=Column(Integer,ForeignKey("product.id",ondelete='CASCADE'),nullable=False)
    quantity=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    order_status=Column(String,nullable=False)
    product_name=Column(String,nullable=False)
    order_price=Column(Integer,nullable=False)
