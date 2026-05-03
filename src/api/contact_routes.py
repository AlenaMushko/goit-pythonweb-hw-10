from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.conf.constants import CONTACTS_PREFIX
from src.schemas.contact_schemas import (
    ContactBirthdayResponse,
    ContactCreate,
    ContactResponse,
    ContactUpdate,
)
from src.services.contact_service import ContactService

router = APIRouter(prefix=CONTACTS_PREFIX, tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.create_contact(body)


@router.get("/", response_model=list[ContactResponse])
async def get_all_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: str | None = Query(default=None),
    surname: str | None = Query(default=None),
    email: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    service = ContactService(db)

    if name or surname or email:
        return await service.search_contacts_by_query(
            name=name, surname=surname, email=email, skip=skip, limit=limit
        )

    return await service.get_all_contacts(skip=skip, limit=limit)


@router.get("/birthdays/upcoming", response_model=list[ContactBirthdayResponse])
async def get_upcoming_birthdays(
    days: int = Query(7, ge=1, le=30), db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.get_upcoming_birthdays(days=days)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact_by_id(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    contact = await service.get_contact_by_id(contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.update_contact(contact_id, body)


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.remove_contact(contact_id)
