from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.entity.models import Contact
from src.schemas.todo import ContactSchema, ContactUpdateSchema, ContactResponse


async def get_contact_with_upcoming_birthday(upcoming_days: int, limit: int, offset: int, db: AsyncSession,
                                             future_date=None):
    current_date = datetime.now().date()
    future_date = current_date + timedelta(days = upcoming_days)

    data = select(Contact).filter(Contact.birthday.between(current_date, future_date)).offset(offset).limit(limit)

    contacts = await db.execute(data)
    return contacts.scalars().all()


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    data = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(data)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    data = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(data)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    data = select(Contact).filter_by(id=contact_id)
    result = await db.execute(data)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.address = body.address
        contact.notes = body.notes
        contact.interests = body.interests
        contact.is_active = body.is_active
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    data = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(data)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact