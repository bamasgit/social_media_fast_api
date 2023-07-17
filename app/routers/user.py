from .. import models,schemas,utils;
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from ..database import get_db;

router = APIRouter(
    tags=['users']#group all the root operations related to user in docs
);
# here we dont have access to app, so we cannot use @app.post()ect..
# so we are creating a router here called "router".

#operation for user
@router.post("/users", status_code=status.HTTP_201_CREATED, 
        response_model=schemas.UserOut)
def create_user(user : schemas.UserLogin,db: Session = Depends(get_db)):
    hashed_password = utils.hashed(user.password)
    user.password = hashed_password;
    new_user = models.User(**user.dict());
    db.add(new_user);
    db.commit();
    db.refresh(new_user);
    return new_user;

#retirve specific user
@router.get("/users/{id}", response_model = schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first();
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="User id {id} not dound");
    return user ;