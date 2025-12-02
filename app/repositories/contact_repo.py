from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.contact import Contact


def get_contact_repo(
    session: AsyncSession = Depends(get_session),
) -> "ContactRepository":
    return ContactRepository(session)


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self, lead_id: int, source_id: int, operator_id: int | None
    ) -> Contact:
        contact = Contact(
            lead_id=lead_id,
            source_id=source_id,
            operator_id=operator_id,
            status="active",
        )
        self._session.add(contact)
        await self._session.commit()
        await self._session.refresh(contact)
        return contact

    async def get_active_load(self, operator_id: int) -> int:
        """Считает количество активных обращений у оператора"""
        query = (
            select(func.count(Contact.id))
            .where(Contact.operator_id == operator_id)
            .where(Contact.status == "active")
        )
        result = await self._session.execute(query)
        return result.scalar() or 0
