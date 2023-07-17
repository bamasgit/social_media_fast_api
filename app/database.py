from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:\
{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL);
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# #DB connection with raw sql- right now we are using SQLALCHEMY
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'Fastapi',
#         user = 'postgres', password = 'sundari', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("success")
#         break;
#     except Exception as error:
#         print("failed");
#         print(error);
#         time.sleep(2)
