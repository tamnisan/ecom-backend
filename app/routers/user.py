from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app import models, schemas,OAuth2
from app.database import get_db
from app.utils import hash

router=APIRouter(prefix="/users",tags=["users"])



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(pay:schemas.User,db:Session=Depends(get_db)):
    hased=hash(pay.password)
    b=pay.model_dump()
    b.update({"password":hased})
    a=models.User(**b)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@router.get("/",response_model=list[schemas.UserResponse],)
def get_user(db:Session=Depends(get_db),current_user: models.User = Depends(OAuth2.get_current_user)):
    u=db.query(models.User).filter(models.User.id==current_user.id)
    
    if current_user.role=="admin" or current_user.role=="superadmin":
        a=db.query(models.User).all()
        return a
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="only admin and super admin can do this operation ")

    
    
    
    
@router.post("/wallet",response_model=schemas.ReturnWallet)
def push_money(pay:schemas.Wallet,current_user:int=Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    query=db.query(models.User).filter(models.User.id==current_user.id)
    user=query.first()

    query.update(pay.model_dump(),synchronize_session=False)
    db.commit()
    db.refresh(user)
    return {"message":"wallet updated successfully","wallet":user.wallet}


@router.get("/wallet")
def push_money(current_user:int=Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    query=db.query(models.User).filter(models.User.id==current_user.id)
    user=query.first()
    db.refresh(user)
    return {"message":f"the money in your wallet is  : {user.wallet}"}


@router.post("/promote")
def upgrade_user(pay:schemas.UpgradeUser,current_user: models.User = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    if current_user.role=="superadmin":
        query=db.query(models.User).filter(models.User.email==pay.username)
        user=query.first()
        query.update({"role":"admin"})
        db.commit()
        db.refresh(user)
        return {"message":f"the user with username:{user.email} has been promoted to admin "}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="only admin and super admin can do this operation ")

