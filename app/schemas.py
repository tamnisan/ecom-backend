from typing import Optional

from pydantic import BaseModel

class Product(BaseModel):
    product_name:str
    inventory:int
    product_type:str
    warehouse_pin:int
    discount_status: Optional[bool] = False
    discount_percent:Optional[int]=0



class Discount(BaseModel):
    discount_status:bool
    discount_percent:int
