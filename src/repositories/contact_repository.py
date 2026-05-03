from datetime import date

from sqlalchemy import and_, extract, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.contact_model import ContactModel
from src.schemas.contact_schemas import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create_contact(self, body: ContactCreate) -> ContactModel:
        contact = ContactModel(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def get_all_contacts(self, skip: int = 0, limit: int = 100) -> list[ContactModel]:
        stmt = select(ContactModel).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_contact_by_id(self, contact_id: int) -> ContactModel | None:
        stmt = select(ContactModel).where(ContactModel.id == contact_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> ContactModel | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> ContactModel | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search_contacts_by_query(
        self,
        name: str | None = None,
        surname: str | None = None,
        email: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ContactModel]:
        filters = []
        if name:
            filters.append(ContactModel.name.ilike(f"%{name}%"))
        if surname:
            filters.append(ContactModel.surname.ilike(f"%{surname}%"))
        if email:
            filters.append(ContactModel.email.ilike(f"%{email}%"))

        stmt = select(ContactModel)
        if filters:
            stmt = stmt.where(or_(*filters))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_upcoming_birthdays(
        self, _start_date: date, _end_date: date
    ) -> list[ContactModel]:
        start_md = _start_date.month * 100 + _start_date.day
        end_md = _end_date.month * 100 + _end_date.day
        birthday_md = extract("month", ContactModel.birthday) * 100 + extract(
            "day", ContactModel.birthday
        )

        if start_md <= end_md:
            date_filter = and_(birthday_md >= start_md, birthday_md <= end_md)
        else:
            date_filter = or_(birthday_md >= start_md, birthday_md <= end_md)

        stmt = select(ContactModel).where(date_filter)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
