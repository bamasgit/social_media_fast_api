from jose import JWTError, jwt
from datetime import datetime, timedelta;
from fastapi.security import OAuth2PasswordBearer;
from fastapi import Depends, status,HTTPException
from . import schemas,database,models
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_toekn(data: dict):
    to_encode = data.copy();
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES);
    to_encode.update({"exp": expire})
    encodec_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encodec_jwt;

# returns id bcs in TokenData schema we only have token id
def verify_access_token(token :str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM]);
        id: str = payload.get("user_id")
        print("*************",id);
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

# can automatically fetch user from the DB and associate with each path operation
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not valid credentials", headers={"www-Authenticate":"Bearer"});
    token = verify_access_token(token,credential_exception);
    user = db.query(models.User).filter(models.User.id == token.id).first();
    return user;