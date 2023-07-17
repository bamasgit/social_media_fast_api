from .. import models,schemas,utils,oauth2;
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import FastAPI, Response,status,HTTPException,Depends, APIRouter
from ..database import get_db;
from typing import List,Optional

router = APIRouter(
    tags=['posts']#group all the root operations ralted to post in docs
);
#we can also all prefix in our router obj like bellow
# router = APIRouter(
#     prefix="/posts"
# )

#by adding the above prefix, we can just add "/", in out path opertaion in 
# the place of "/posts", like @router.get("/") insted of @router.get("/posts")



#new root operation with SQLALCHEMY
@router.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


#post operation with SQLALCEHMY
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
current_user: id = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title = post.title, content = post.content, 
    #                 published = post.published)
    #efficient way to write line 64,65
    new_post = models.Post(owner_id= current_user.id, **post.dict())
    print(current_user.email)
    db.add(new_post);
    db.commit();
    db.refresh(new_post);
    return new_post

#retriving an indivigual post and for not found post
@router.get("/posts/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: id = Depends(oauth2.get_current_user)):
   
    # get indivigual post without number of votes
    # new_post = db.query(models.Post).filter(models.Post.id == id).first();
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail = f"post{id} not found")
    return post

#delete post with SQLALCHEMY
@router.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: id = Depends(oauth2.get_current_user)):
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post = post_querry.first();
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="not found post")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised")

    post_querry.delete(synchronize_session = False)
    db.commit();
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update operation
@router.put("/posts/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
        ,current_user: id = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first();

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="not found post")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit();
    return post_query.first()