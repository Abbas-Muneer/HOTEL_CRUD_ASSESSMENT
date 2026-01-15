from datetime import datetime, date

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class RateAdjustment(Base):
    __tablename__ = "rate_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(
        Integer, ForeignKey("room_types.id", ondelete="CASCADE"), nullable=False, index=True
    )
    effective_date = Column(Date, nullable=False)
    adjustment_amount = Column(Numeric(10, 2), nullable=False)
    reason = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    room_type = relationship("RoomType", back_populates="rate_adjustments")
