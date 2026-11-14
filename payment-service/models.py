from datetime import datetime, timezone
from database import Base
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Payment(Base):
  __tablename__ = "payments"

  id: Mapped[str] = mapped_column(String, primary_key=True)
  order_id: Mapped[str] = mapped_column(String, nullable=False)
  amount: Mapped[int] = mapped_column(Integer, nullable=False)
  status: Mapped[str] = mapped_column(String, default="PENDING")
  created_at: Mapped[datetime] = mapped_column(
      DateTime, default=lambda: datetime.now(timezone.utc)
  )