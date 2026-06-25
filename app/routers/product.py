from ast import alias
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query,status
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db


router=APIRouter(tags=["product"],prefix="/products")



@router.post("/",status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.Product,status_code=status.HTTP_201_CREATED,db:Session=Depends(get_db)):
    prod=models.Product(**product.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod





@router.get("/")
def get_product(product_type:Optional[str]=Query(None,alias="ProductType"),warehouse_pin:Optional[int]=Query(None,alias="WarehousePin"),discount_status:Optional[bool]=Query(None,alias="DiscountStatus"),db:Session=Depends(get_db)):
    base_query=db.query(models.Product)
    
    
    if (product_type is None) and (warehouse_pin is None) and (discount_status is None):

        return base_query.all()
    
    if product_type:
        base_query=base_query.filter(models.Product.product_type==product_type)
        product=base_query.all()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invlaid query")
    if warehouse_pin:
        base_query=base_query.filter(models.Product.warehouse_pin==warehouse_pin)
        product=base_query.all()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invlaid query")

    if discount_status is not None:
        base_query=base_query.filter(models.Product.discount_status==discount_status)
        product=base_query.all()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invlaid query")


    return base_query.all()


@router.get("/{id}")
def get_product(id:int,db:Session=Depends(get_db)):
    prd=db.query(models.Product).filter(models.Product.id==id).first()
    if not prd:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product with id:{id} not found") 
    return prdoucts


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session=Depends(get_db)):
    base_query=db.query(models.Product).filter(models.Product.id==id)
    if not base_query:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product with id:{id} not found")
    base_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}")
def update_product(id:int,prod:schemas.Product,db:Session=Depends(get_db)):
    prd=db.query(models.Product).filter(models.Product.id==id)
    prd_ist=prd.first()
    if not prd.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id:{id} not found")
    
    prd.update(prod.dict(),synchronize_session=False)
    db.commit()
    db.refresh(prd_ist)
    return {"upadted product":prd_ist}



@router.put("/discount/{id}")
def  update_discount(prod:schemas.Discount,id:int,db:Session=Depends(get_db),):
    


    if not prod.discount_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="for updatind the discount discount status should be true")
    
    prd=db.query(models.Product).filter(models.Product.id==id)
    prd_ist=prd.first()
    if not prd.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id:{id} not found")
    
    prd.update(prod.model_dump(),synchronize_session=False)
    db.commit()
    db.refresh(prd_ist)
    
    return {"details":prd_ist}




