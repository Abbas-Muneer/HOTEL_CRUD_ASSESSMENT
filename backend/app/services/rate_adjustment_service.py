from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.rate_adjustment import RateAdjustment
from app.models.room_type import RoomType
from app.schemas.rate_adjustment import RateAdjustmentCreate


def ensure_non_negative_rate(base_rate: Decimal, adjustment: Decimal) -> None:
    if base_rate + adjustment < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Effective rate cannot be negative for given adjustment",
        )


def create_rate_adjustment(
    db: Session, room_type: RoomType, payload: RateAdjustmentCreate
) -> RateAdjustment:
    ensure_non_negative_rate(room_type.base_rate, payload.adjustment_amount)
    adjustment = RateAdjustment(
        room_type_id=room_type.id,
        effective_date=payload.effective_date,
        adjustment_amount=payload.adjustment_amount,
        reason=payload.reason,
    )
    db.add(adjustment)
    db.commit()
    db.refresh(adjustment)
    return adjustment


def list_rate_adjustments(db: Session, room_type: RoomType) -> list[RateAdjustment]:
    return (
        db.query(RateAdjustment)
        .filter(RateAdjustment.room_type_id == room_type.id)
        .order_by(desc(RateAdjustment.effective_date), desc(RateAdjustment.created_at))
        .all()
    )


def get_latest_adjustment(
    db: Session, room_type: RoomType, as_of: date
) -> Optional[RateAdjustment]:
    return (
        db.query(RateAdjustment)
        .filter(
            RateAdjustment.room_type_id == room_type.id,
            RateAdjustment.effective_date <= as_of,
        )
        .order_by(desc(RateAdjustment.effective_date), desc(RateAdjustment.created_at))
        .first()
    )


def get_next_adjustment(
    db: Session, room_type: RoomType, after: date
) -> Optional[RateAdjustment]:
    return (
        db.query(RateAdjustment)
        .filter(
            RateAdjustment.room_type_id == room_type.id,
            RateAdjustment.effective_date > after,
        )
        .order_by(RateAdjustment.effective_date.asc(), desc(RateAdjustment.created_at))
        .first()
    )


def compute_effective_rate(db: Session, room_type: RoomType, as_of: date):
    latest = get_latest_adjustment(db, room_type, as_of)
    adjustment_amount = latest.adjustment_amount if latest else Decimal("0")
    effective_rate = room_type.base_rate + adjustment_amount
    return {
        "latest_adjustment": latest,
        "adjustment_amount": adjustment_amount,
        "effective_rate": effective_rate,
    }
