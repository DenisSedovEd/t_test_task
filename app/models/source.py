from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.operator import Operator


class Source(Base):
    __tablename__ = 'sources'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True,
    )
    name: Mapped[String] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    weights: Mapped['SourceOperatorWeight'] = relationship(
        'SourceOperatorWeight',
        back_populates='source',
    )
    contacts: Mapped['Contact'] = relationship(
        'Contact',
        back_populates='source',
    )

class SourceOperatorWeight(Base):
    __tablename__ = 'source_operator_weights'

    source_id: Mapped[int] = mapped_column(
        ForeignKey('sources.id'),
        primary_key=True,
    )
    operator_id: Mapped[int] = mapped_column(
        ForeignKey('operators.id'),
        primary_key=True,
    )
    weight: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    source: Mapped[Source] = relationship(
        'Source',
        back_populates='weights',
    )

    operator: Mapped[Operator] = relationship(
        'Operator',
        back_populates='weights',
    )