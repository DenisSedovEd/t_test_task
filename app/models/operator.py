from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.contact import Contact
    from app.models.source import SourceOperatorWeight


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    max_load_limit: Mapped[int] = mapped_column(
        Integer,
        default=5,
    )

    weights: Mapped['SourceOperatorWeight'] = relationship(
        'SourceOperatorWeight',
        back_populates='operator',
    )
    contacts: Mapped['Contact'] = relationship(
        'Contact',
        back_populates='operator',
    )