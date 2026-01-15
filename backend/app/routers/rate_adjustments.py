from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.rate_adjustment import RateAdjustmentCreate, RateAdjustmentRead
from app.services import room_type_service, rate_adjustment_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(
    "/room-types/{room_type_id}/rate-adjustments",
    response_model=RateAdjustmentRead,
    status_code=201,
)
def create_rate_adjustment(
    room_type_id: int, payload: RateAdjustmentCreate, db: Session = Depends(get_db)
):
    room_type = room_type_service.get_room_type_or_404(db, room_type_id)
    adjustment = rate_adjustment_service.create_rate_adjustment(db, room_type, payload)
    return adjustment


@router.get(
    "/room-types/{room_type_id}/rate-adjustments",
    response_model=list[RateAdjustmentRead],
)
def list_rate_adjustments(room_type_id: int, db: Session = Depends(get_db)):
    room_type = room_type_service.get_room_type_or_404(db, room_type_id)
    return rate_adjustment_service.list_rate_adjustments(db, room_type)
