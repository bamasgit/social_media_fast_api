from app import models,schemas,utils
import time
from typing import Optional, List
from fastapi import FastAPI, Response,status,HTTPException,Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine, get_db
from passlib.context import CryptContext
from .routers import post,user,auth,vote;
from fastapi.middleware.cors import CORSMiddleware
#tells to run all the cretate command in SQLALCHEMY but since we have alembic
# now, we can comment it out
# models.Base.metadata.create_all(bind = engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#DB connection
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'Fastapi',
        user = 'postgres', password = 'sundari', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("success")
        break;
    except Exception as error:
        print("failed");
        print(error);
        time.sleep(2)


app = FastAPI();
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return{"Message": "message"}

app.include_router(post.router);
app.include_router(user.router);
app.include_router(auth.router);
app.include_router(vote.router);