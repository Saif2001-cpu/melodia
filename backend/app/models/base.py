"""Database base model for common columns."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Mixin to add created_at and updated_at columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


def generate_uuid() -> str:
    """Generate a UUID4 string."""
    return str(uuid.uuid4())
