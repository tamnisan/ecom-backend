from itertools import product
from typing import Optional

from pydantic import BaseModel, EmailStr,ConfigDict

class Product(BaseModel):
    product_name:str
    inventory:int
    product_type:str
    warehouse_pincode:int
    discount_status: Optional[bool] = False
    discount_percent:Optional[int]=0



class Discount(BaseModel):
    discount_status:bool
    discount_percent:int




    # __tablename__="user"
    # id=Column(Integer,primary_key=True,nullable=False)
    # email=Column(String,nullable=False,unique=True)
    # password=Column(String,nullable=False)
    # user_pincode=Column(Integer,nullable=False)
    # wallet=Column(Integer,server_default=text('0'),nullable=False)
    # completed_order=Column(Integer,server_default=text('0'),nullable=False)
    # pending_order=Column(Integer,server_default=text('0'),nullable=False)
    # failed_order=Column(Integer,server_default=text('0'),nullable=False)



class User(BaseModel):
    email:EmailStr
    password:str
    user_pincode:int
 

class UserResponse(BaseModel):
    email:EmailStr
    user_pincode:int
    id:int

    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
     access_token:str
     token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None



class Wallet(BaseModel):
    wallet:int


class ReturnWallet(BaseModel):
    message:str
    wallet:int
    model_config=ConfigDict(from_attributes=True)



class UpgradeUser(BaseModel):
    username:str



class PlaceOrder(BaseModel):
    product_id:int
    quantity:int


class CancelProduct(BaseModel):
    order_id:int
    