from datetime import date
import re

from sqlalchemy import Date, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.conf.constants import (
    NAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    PASSWORD_REGEX,
    EMAIL_REGEX,
)
from src.db.base import Base


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    email: Mapped[str] = mapped_column(String(EMAIL_MAX_LENGTH), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=False)

    @validates("first_name")
    def validate_first_name(self, key, value: str) -> str:
        if value.strip() == "":
            raise ValueError("First name cannot be empty")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value: str) -> str:
        if value.strip() == "":
            raise ValueError("Last name cannot be empty")
        return value

    @validates("email")
    def validate_email(self, key, value: str) -> str:
        if value.strip() == "":
            raise ValueError("Email cannot be empty")
        if not re.match(EMAIL_REGEX, value):
            raise ValueError("Invalid email address")
        return value

    @validates("password")
    def validate_password(self, key, value: str) -> str:
        if value.strip() == "":
            raise ValueError("Password cannot be empty")
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, and one number"
            )
        return value

    def __repr__(self) -> str:
        return f"UserModel(id={self.id}, user_name={self.first_name + ' ' + self.last_name})"
