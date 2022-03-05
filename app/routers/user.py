from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import schemas, models, utils
from sqlalchemy.orm import Session
from app.dbconn import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Userout)
def create_user(new_user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password

    user_created = models.Users(**new_user.dict())
    db.add(user_created)
    db.commit()
    db.refresh(user_created)
    return user_created 

@router.get("/", response_model = list[schemas.Userout])
def get_all_users(db: Session = Depends(get_db)):
    posts = db.query(models.Users).all()
    return posts

@router.get("/{id}", response_model = schemas.Userout)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"User with id: {id} does not exist")
    return user

@router.delete("/{id}")
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Users).filter(models.Users.user_id == id)

    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail= f"user does not exist")

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)