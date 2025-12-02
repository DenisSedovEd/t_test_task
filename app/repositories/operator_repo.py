from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.operator import Operator
from app.schemas.operator import OperatorUpdate


def get_operator_repo(
    session: AsyncSession = Depends(get_session),
) -> "OperatorRepository":
    return OperatorRepository(session)


class OperatorRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        name: str,
        max_load: int,
    ) -> Operator:
        op = Operator(name=name, max_load_limit=max_load)
        self._session.add(op)
        await self._session.commit()
        await self._session.refresh(op)
        return op

    async def get_all(self):
        result = await self._session.execute(select(Operator))
        return result.scalars().all()

    async def get_by_id(self, op_id: int) -> Operator | None:
        return await self._session.get(Operator, op_id)

    async def update(self, op_id: int, data: OperatorUpdate) -> Operator | None:
        operator = await self.get_by_id(op_id)
        if not operator:
            return None

        update_data = data.model_dump(exclude_none=True)

        if update_data:
            for key, value in update_data.items():
                setattr(operator, key, value)

            await self._session.commit()
            await self._session.refresh(operator)

        return operator
