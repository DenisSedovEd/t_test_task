from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db import get_session
from app.models.contact import Contact
from app.models.lead import Lead
from app.models.operator import Operator


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
        query = (
            select(func.count(Contact.id))
            .where(Contact.operator_id == operator_id)
            .where(Contact.status == "active")
        )
        result = await self._session.execute(query)
        return result.scalar() or 0

    async def get_current_distribution(self):
        load_query = (
            select(Contact.operator_id, func.count(Contact.id).label("current_load"))
            .where(Contact.status == "active")
            .where(Contact.operator_id.isnot(None))
            .group_by(Contact.operator_id)
        )
        load_result = await self._session.execute(load_query)
        load_map = {row.operator_id: row.current_load for row in load_result}

        operators_query = select(Operator)
        operators_result = await self._session.execute(operators_query)
        operators = operators_result.scalars().all()

        distribution = []
        for op in operators:
            distribution.append(
                {
                    "operator_id": op.id,
                    "name": op.name,
                    "max_load_limit": op.max_load_limit,
                    "is_active": op.is_active,
                    "current_load": load_map.get(op.id, 0),
                }
            )

        return distribution

    async def get_all_leads_with_contacts(self):
        query = select(Lead).options(
            selectinload(Lead.contacts).selectinload(Contact.source),
            selectinload(Lead.contacts).selectinload(Contact.operator),
        )
        result = await self._session.execute(query)
        return result.scalars().all()
