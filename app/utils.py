from warnings import deprecated

from passlib.context import CryptContext



pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")

def hash(pwd:str):
    return pwd_context.hash(pwd)

def verify(plain_pwd, hased_pwd):
  
    return pwd_context.verify(plain_pwd, hased_pwd)
