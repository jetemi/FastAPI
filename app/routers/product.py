from typing import Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import schemas, models, oauth2
from sqlalchemy.orm import Session
from app.dbconn import get_db

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)

@router.get("/", response_model = list[schemas.ResponseBase])
def get_all_products(db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user),
limit: int = 5, skip: int = 0,
search: Optional[str] = ""):  #limit, offset
    posts = db.query(models.Products).filter(models.Products.name.contains(search)).\
                            limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model = schemas.ResponseBase)
def get_product_by_id(id: int, response: Response, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail= f"post with id: {id} was not found")
    return product

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ResponseBase)
def create_product(new_post: schemas.PostBase, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    post_created = models.Products(owner_id = current_user.user_id, **new_post.dict())
    db.add(post_created)
    db.commit()
    db.refresh(post_created)
    return post_created 

@router.put("/{id}", response_model=schemas.ResponseBase)
def update_product_by_id(id: int, new_post: schemas.UpdateBase, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    updated_query = db.query(models.Products).filter(models.Products.id == id)

    if updated_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail= f"post with id: {id} does not exist")
    
    if updated_query.first().owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    updated_query.update(new_post.dict(), synchronize_session=False)
    
    db.commit()
    
    # db.refresh(updated_prod)
    return updated_query.first()

@router.delete("/{id}") #, status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_id(id: int, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
  
    query = db.query(models.Products).filter(models.Products.id == id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail= f"post with id: {id} does not exist")

    if query.first().owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)