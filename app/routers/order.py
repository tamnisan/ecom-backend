

from ast import mod
from tkinter import S

from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app import schemas,OAuth2,models
from app.database import get_db



router=APIRouter(prefix="/orders",tags=["orders"])




@router.post("/")
def place_order(ord:schemas.PlaceOrder,db:Session=Depends(get_db),current_user:int=Depends(OAuth2.get_current_user)):
    prd=db.query(models.Product).filter(models.Product.id==ord.product_id)
    prod=prd.first()
    user_query=db.query(models.User).filter(models.User.id==current_user.id)
    user=user_query.first()
    if not prd.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id:{ord.product_id} does not exist")
    price=prd.first().price*ord.quantity
    if current_user.wallet<price:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"insufficent balance in wallet , the order price is {price}")
    a=models.Order(user_id=current_user.id,product_id=ord.product_id,quantity=ord.quantity,order_status="placed",product_name=prod.product_name,order_price=price)
    db.add(a)
    prd.update({"inventory":prod.inventory-ord.quantity})
    pending_order=user.pending_order+1
    wallet=user.wallet-price
    user_query.update({"pending_order":pending_order,"wallet":wallet})
    db.commit()
    db.refresh(a)
    return a



@router.post("/cancel")
def cancel_product(prd:schemas.CancelProduct,db:Session=Depends(get_db),current_user:int=Depends(OAuth2.get_current_user)):
    query=db.query(models.Order).filter(models.Order.order_id==prd.order_id)
    ord=query.first()
    if not ord:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    user_query=db.query(models.User).filter(models.User.id==current_user.id)
    user=user_query.first()
    if ord.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no order with order id:{prd.order_id} was placed by you")
    if ord.order_status=="canceled":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the order was already canceled")
    if ord.order_status=="shipped":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the order has been shipped cannot cancel order now") 
    query.update({"order_status":"canceled"},synchronize_session=False)
    prod_query=db.query(models.Product).filter(models.Product.id==ord.product_id)
    prod=prod_query.first()
    prod_query.update({"inventory":prod.inventory+ord.quantity},synchronize_session=False)
    pending_order=user.pending_order-1
    wallet=user.wallet+ord.order_price
    canceled_order=user.failed_order+1
    user_query.update({"pending_order":pending_order,"wallet":wallet,"failed_order":canceled_order})

    db.commit()

    return {"message":"order successfully canceled"}


@router.post("/ship")
def cancel_product(prd:schemas.CancelProduct,db:Session=Depends(get_db),current_user:int=Depends(OAuth2.get_current_user)):
    query=db.query(models.Order).filter(models.Order.order_id==prd.order_id)
    ord=query.first()

    if not ord:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    user_query=db.query(models.User).filter(models.User.id==ord.user_id)
    user=user_query.first()
    if current_user.role=="admin" or current_user.role=="superadmin":
        if ord.order_status=="shipped":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the order was already shipped")
        if ord.order_status=="canceled":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the order is canceled , cannot ship")       
        query.update({"order_status":"shipped"},synchronize_session=False)
        pending_order=user.pending_order-1
        ship=user.completed_order+1
        user_query.update({"pending_order":pending_order,"completed_order":ship})       
        db.commit()
        return {"message":"order successfully shipped"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="onnly admin and super admin can ship  product")

    
    


@router.get("/")
def get_order(db:Session=Depends(get_db),current_user:int=Depends(OAuth2.get_current_user)):
    ord=db.query(models.Order).filter(models.Order.user_id==current_user.id).all()
    if not ord:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no order ")
    return ord