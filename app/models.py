from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
# convention = {
#   "pk": "pk_%(table_name)s"
# }
# Base = declarative_base()
# Base.metadata = MetaData(naming_convention=convention)
# ORM model for post table
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer,primary_key = True , nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default= 'True')
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, 
                        server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable =False);
    # fetch some user imfo for each post, here User is the class name, also update 
    # post schema to display the user data in "schemas.py" file
    owner = relationship("User")

#ORM for user table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True , nullable = False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, 
                        server_default=text('now()'))
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "post.id", ondelete="CASCADE"), primary_key=True)