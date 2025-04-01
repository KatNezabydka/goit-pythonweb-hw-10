from _operator import or_
from datetime import  timedelta, date
from sqlalchemy import func
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contacts = await self.db.execute(stmt)
        return contacts.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id)

    async def update_contact(
            self, contact_id: int, body: ContactUpdate
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.dict().items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def remove_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search_contacts(self, first_name: str = None, last_name: str = None, email: str = None) -> List[Contact]:
        stmt = select(Contact)
        filters = []

        if first_name:
            filters.append(Contact.first_name == first_name)
        if last_name:
            filters.append(Contact.last_name == last_name)
        if email:
            filters.append(Contact.email == email)

        if filters:
            condition = filters[0]
            for f in filters[1:]:
                condition = or_(condition, f)
            stmt = stmt.filter(condition)

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contacts_upcoming_birthday(self) -> List[Contact]:
        today = date.today()

        next_week = today + timedelta(days=7)

        stmt = select(Contact).filter(
            func.extract('month', Contact.birthday) == today.month,
            func.extract('day', Contact.birthday) >= today.day,
            (func.extract('month', Contact.birthday) == func.extract('month', next_week)) |
            (func.extract('month', Contact.birthday) == today.month)
        )
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()
