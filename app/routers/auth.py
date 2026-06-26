
from fastapi import HTTPException,Depends,APIRouter,status
from   sqlalchemy.orm import Session
from app import schemas,models,OAuth2
from app.database import get_db
from app.utils import verify
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(prefix="/login",tags=["login"])

@router.post("/",response_model=schemas.Token)
def login(pay: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    
    #so it return username and password
  
    user=db.query(models.User).filter(models.User.email==pay.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"the user with email:{pay.username} is not there in the database")
    if not verify(pay.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    

    #now create token
    #return token
    access_token=OAuth2.create_token({"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer" }