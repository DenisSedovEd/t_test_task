from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db import get_session
from app.models.source import Source, SourceOperatorWeight


def get_source_repo(
    session: AsyncSession = Depends(get_session),
) -> "SourceRepository":
    return SourceRepository(session)


class SourceRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_with_weights(self, name: str, weights: list[dict]):
        source = Source(name=name)
        self._session.add(source)
        await self._session.flush()

        for w in weights:
            link = SourceOperatorWeight(
                source_id=source.id, operator_id=w["operator_id"], weight=w["weight"]
            )
            self._session.add(link)

        await self._session.commit()
        await self._session.refresh(source)
        return source

    async def get_weights_for_source(self, source_id: int):
        query = (
            select(SourceOperatorWeight)
            .where(SourceOperatorWeight.source_id == source_id)
            .options(selectinload(SourceOperatorWeight.operator))
        )
        result = await self._session.execute(query)
        return result.scalars().all()
