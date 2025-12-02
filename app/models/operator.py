from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[String] = mapped_column(
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

    weight: Mapped['sourceOperatorWeight'] = relationship(
        'sourceOperatorWeight',
        back_populates='operator',
    )
    contacts: Mapped['Contact'] = relationship(
        'Contact',
        back_populates='operator',
    )