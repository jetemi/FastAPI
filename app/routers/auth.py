from fastapi import status, HTTPException, Depends, APIRouter
from app import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.dbconn import get_db

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post('/', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.user_id})

    return {"access_token": access_token, "token_type": "bearer"}