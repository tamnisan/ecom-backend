from pydantic import BaseModel

class Product(BaseModel):
    product_name:str
    inventory:int
    product_type:str
    warehouse_pin:int