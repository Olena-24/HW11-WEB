import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, create_engine, func
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Role(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    role = Column(Enum(Role), default=Role.user, nullable=False)

    contacts = relationship('Contact', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role.name}')>"

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), index=True)
    description = Column(String(250))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='contacts')

    def __repr__(self):
        return f"<Contact(id={self.id}, title='{self.title}', user_id={self.user_id})>"