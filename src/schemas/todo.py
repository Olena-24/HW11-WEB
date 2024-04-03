from pydantic import BaseModel, EmailStr, Field, constr, field_validator
from typing import Optional
from datetime import date
import re

class ContactSchema(BaseModel):
    """
    Schema for contact creation.
    """
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone_number: constr(min_length=3, max_length=20) # type: ignore
    birthday: date
    address: str = Field(..., min_length=3, max_length=250)
    notes: Optional[str] = None
    interests: Optional[str] = None
    is_active: bool = Field(default=False)

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if not re.match(r'^\+?[0-9\-\s()]*$', value):
            raise ValueError('invalid phone number')
        return value


class ContactUpdateSchema(ContactSchema):
    """
    Schema for updating contact details.
    """
    pass


class ContactResponse(BaseModel):
    """
    Schema for returning contact details.
    """
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    address: str
    notes: Optional[str]
    interests: Optional[str]
    is_active: bool

    class Config:
        """
        Pydantic config settings.
        """
        from_attributes = True