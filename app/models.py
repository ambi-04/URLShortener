import datetime

from sqlalchemy import DateTime, PrimaryKeyConstraint, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class UrlMapper(Base):
    __tablename__ = 'url_mapper'
    __table_args__ = (
        PrimaryKeyConstraint('short_url', name='url_mapper_pkey'),
    )

    short_url: Mapped[str] = mapped_column(String(255), primary_key=True)
    long_url: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
