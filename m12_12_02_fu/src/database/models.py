import enum
from datetime import date

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, generics
from sqlalchemy import String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str] = mapped_column(String(150))
    completed: Mapped[bool] = mapped_column(default=False, nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)
    user_id: Mapped[int] = mapped_column(generics.GUID(), ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship('User', backref="todos")


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(50))
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[Enum] = mapped_column('role', Enum(Role), default=Role.user)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
