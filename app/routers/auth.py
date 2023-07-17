from fastapi import APIRouter,Depends,status,HTTPException,Response;
from sqlalchemy.orm import Session;
from ..import schemas,models,utils,oauth2
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm;

router = APIRouter(tags=['Authentication'])

@router.post("/login",response_model=schemas.Token)
def create_user(user : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.email == user.username).first()
    if not users:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid credencials")
    if not utils.verify(user.password,users.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid credencials")
    
    access_token = oauth2.create_access_toekn(data={"user_id":users.id})
    return {"access_token":access_token, "token_type":"bearer"};