import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.lead import Lead
    from app.models.operator import Operator
    from app.models.source import Source


class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    status: Mapped[String] = mapped_column(
        String,
        default='active',
    )
    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('leads.id'),
    )
    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('sources.id'),
    )

    operator_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('operators.id'),
        nullable=True,
    )

    lead: Mapped['Lead'] = relationship(
        'Lead',
        back_populates='contacts',
    )

    source: Mapped['Source'] = relationship(
        'Source',
        back_populates='contacts',
    )

    operator: Mapped['Operator'] = relationship(
        'Operator',
        back_populates='contacts',
    )