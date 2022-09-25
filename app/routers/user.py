from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils


route = APIRouter(
    prefix="/for_users",
    tags=['Users']
)



@route.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def  create_post(user:schemas.UserCreat, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_post=models.User(**user.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@route.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_post(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"This user id {id} is not valid")
    
    return user