from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.class_registration_repository import ClassRegistrationRepository
from app.repositories.class_repository import ClassRepository
from app.schemas.attendance_schema import (
    AttendanceHistoryEntry,
    AttendanceResponse,
    AttendanceSaveRequest,
)
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/classes/{class_id}/attendance", tags=["attendance"])


def get_attendance_service(db: Session = Depends(get_db)) -> AttendanceService:
    return AttendanceService(AttendanceRepository(db))


def ensure_class_exists(class_id: int, db: Session = Depends(get_db)) -> None:
    if ClassRepository(db).get_by_id(class_id) is None:
        raise HTTPException(status_code=404, detail="Class not found")


@router.get("", response_model=list[AttendanceResponse])
def get_attendance_for_today(
    class_id: int,
    service: AttendanceService = Depends(get_attendance_service),
    _: None = Depends(ensure_class_exists),
):
    return service.get_for_class_today(class_id)


@router.post("", response_model=list[AttendanceResponse])
def save_attendance_for_today(
    class_id: int,
    data: AttendanceSaveRequest,
    db: Session = Depends(get_db),
    service: AttendanceService = Depends(get_attendance_service),
    _: None = Depends(ensure_class_exists),
):
    registered_ids = {
        s.id for s in ClassRegistrationRepository(db).get_registered_students(class_id)
    }
    for record in data.records:
        if record.student_id not in registered_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Student {record.student_id} is not registered to this class",
            )
    return service.save_for_class_today(class_id, data.records)


@router.get("/dates", response_model=list[date_type])
def get_attendance_dates(
    class_id: int,
    service: AttendanceService = Depends(get_attendance_service),
    _: None = Depends(ensure_class_exists),
):
    return service.get_dates_for_class(class_id)


@router.get("/history", response_model=list[AttendanceHistoryEntry])
def get_attendance_history(
    class_id: int,
    date: date_type,
    service: AttendanceService = Depends(get_attendance_service),
    _: None = Depends(ensure_class_exists),
):
    return service.get_history_for_class_date(class_id, date)
