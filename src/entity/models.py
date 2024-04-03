from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone_number = Column(String(20), index=True)
    birthday = Column(Date, nullable=False)
    additional_data = Column(String(250))

    def __repr__(self):
        return f"<Contact(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, phone_number={self.phone_number}, birthday={self.birthday}, additional_data={self.additional_data})>"