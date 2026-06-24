from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from app import schemas,models
from app.database import get_db


router=APIRouter(tags=["product"],prefix="/product")



@router.post("/")
def create_product(product:schemas.Product,status_code=status.HTTP_201_CREATED,db:Session=Depends(get_db)):
    prod=models.Product(**product.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod
