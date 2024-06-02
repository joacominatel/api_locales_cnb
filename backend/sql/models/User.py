# sql/models/User.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sql.db import conbra_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {
        'schema': 'dbo',
    } 

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now(), default=datetime.now())

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __str__(self):
        return f"<User {self.username}>"
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at,
            'updated_at': self.updated_at
       }
    
Base.metadata.create_all(conbra_engine)