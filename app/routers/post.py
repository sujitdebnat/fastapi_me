# from operator import mod
# from pickletools import optimize
# from re import search
# from turtle import pos
from unittest import result
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, oauth2#,vote

route = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



# @route.get("/")
@route.get("/",response_model=List[schemas.PostOut])

def root(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit:int = 10,skip:int = 0
,search:Optional[str]=""):

    # posts=db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return result

@route.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def creat_post(post:schemas.PostCreat,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post=models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@route.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # da=db.query(models.Post).filter(models.Post.id==id).first()


    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    # post=da
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"this is fine{id}")

    # if post.owner_id != user_id.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={"data":"invalid"})

    return post



@route.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    da=db.query(models.Post).filter(models.Post.id==id)
    post=da.first()
    if da.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"data":"This is not found 404"})

    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={"data":"invalid"})


    da.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@route.put("/{id}",response_model=schemas.Post)
def update_post(id:int,update_post:schemas.PostBase,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    da=db.query(models.Post).filter(models.Post.id==id)
    post=da.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"data":"This is not found 404"})

    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"data":"Invalid credential"})
    da.update(update_post.dict(),synchronize_session=False)
    db.commit()
    return da.first()
