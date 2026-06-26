from fastapi import FastAPI

from app.database import engine
from app.routers import product,user,auth,order



# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(order.router)



@app.get("/")
def root():
    return {"message": "welcome amigos"}





