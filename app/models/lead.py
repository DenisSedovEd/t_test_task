from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Lead(Base):
    __tablename__ = 'leads'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True,
    )
    external_id: Mapped[str] = mapped_column(
        String, unique=True,
        index=True,
        nullable=False,
    )
    contacts: Mapped['Contact'] = relationship(
        'Contact',
        back_populates='lead',
    )
