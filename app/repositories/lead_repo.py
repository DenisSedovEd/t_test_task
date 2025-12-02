from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.lead import Lead


def get_lead_repo(
    session: AsyncSession = Depends(get_session),
) -> "LeadRepository":
    return LeadRepository(session)


class LeadRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_or_create(self, external_id: str) -> Lead:
        result = await self._session.execute(
            select(Lead).where(Lead.external_id == external_id)
        )
        lead = result.scalar_one_or_none()

        if not lead:
            lead = Lead(external_id=external_id)
            self._session.add(lead)
            await self._session.commit()
            await self._session.refresh(lead)

        return lead
