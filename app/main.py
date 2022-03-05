from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .dbconn import engine
from .routers import product, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["*"]

app.add_middleware(
    CORSMiddleware,                    
    allow_origins= [], #origins,             # what origins do we want to allow?
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World, again"}

app.include_router(product.router)

app.include_router(user.router)

app.include_router(auth.router)