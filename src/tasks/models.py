# src/tasks/models.py
from datetime import datetime
from sqlalchemy import String, ForeignKey, func, null  # Fix 1: Import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.shared.database import Base  # Ensure this path is correct


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True)  #  3: Use | None for optional types
    status: Mapped[str] = mapped_column(String(50), default="todo")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    attachment_url: Mapped[str|None] = mapped_column(String(500), nullable=True)


    owner_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
