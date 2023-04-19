from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    mail: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    formation: Mapped[str] = mapped_column(String(30))
    user_climbing_days: Mapped[Optional[List["UserClimbingDay"]]] = \
        relationship(
            back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, firstname={self.firstname!r},"
            f" firstname={self.lastname!r})")


class UserClimbingDay(Base):
    __tablename__ = "user_climbing_day"
    id: Mapped[int] = mapped_column(primary_key=True)
    climbing_day: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="user_climbing_days")

    def __repr__(self) -> str:
        return f"user_climbing_day(id={self.id!r})"
