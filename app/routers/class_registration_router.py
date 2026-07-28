from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.class_registration_repository import ClassRegistrationRepository
from app.repositories.class_repository import ClassRepository
from app.repositories.student_repository import StudentRepository
from app.schemas.class_registration_schema import ClassRegistrationUpdate
from app.schemas.student_schema import StudentResponse
from app.services.class_registration_service import ClassRegistrationService

router = APIRouter(prefix="/classes/{class_id}/students", tags=["class-registrations"])


def get_class_registration_service(
    db: Session = Depends(get_db),
) -> ClassRegistrationService:
    return ClassRegistrationService(ClassRegistrationRepository(db))


def ensure_class_exists(class_id: int, db: Session = Depends(get_db)) -> None:
    if ClassRepository(db).get_by_id(class_id) is None:
        raise HTTPException(status_code=404, detail="Class not found")


@router.get("", response_model=list[StudentResponse])
def get_registered_students(
    class_id: int,
    service: ClassRegistrationService = Depends(get_class_registration_service),
    _: None = Depends(ensure_class_exists),
):
    return service.get_registered_students(class_id)


@router.put("", response_model=list[StudentResponse])
def replace_registered_students(
    class_id: int,
    data: ClassRegistrationUpdate,
    db: Session = Depends(get_db),
    service: ClassRegistrationService = Depends(get_class_registration_service),
    _: None = Depends(ensure_class_exists),
):
    student_repository = StudentRepository(db)
    for student_id in data.student_ids:
        if student_repository.get_by_id(student_id) is None:
            raise HTTPException(
                status_code=404, detail=f"Student {student_id} not found"
            )
    return service.replace_registrations(class_id, data.student_ids)
