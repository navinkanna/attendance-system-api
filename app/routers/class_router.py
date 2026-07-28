from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.class_model import SchoolClass
from app.repositories.class_registration_repository import ClassRegistrationRepository
from app.repositories.class_repository import ClassRepository
from app.schemas.class_schema import ClassCreate, ClassResponse, ClassUpdate
from app.services.class_service import ClassService

router = APIRouter(prefix="/classes", tags=["classes"])


def get_class_service(db: Session = Depends(get_db)) -> ClassService:
    return ClassService(ClassRepository(db))


def get_class_registration_repository(db: Session = Depends(get_db)) -> ClassRegistrationRepository:
    return ClassRegistrationRepository(db)


def to_response(db_class: SchoolClass, student_count: int) -> ClassResponse:
    return ClassResponse(
        id=db_class.id,
        classname=db_class.classname,
        section=db_class.section,
        student_count=student_count,
    )


@router.post("", response_model=ClassResponse, status_code=201)
def register_class(
    class_data: ClassCreate, service: ClassService = Depends(get_class_service)
):
    db_class = service.register_class(class_data)
    return to_response(db_class, 0)


@router.get("", response_model=list[ClassResponse])
def get_all_classes(
    service: ClassService = Depends(get_class_service),
    registration_repository: ClassRegistrationRepository = Depends(
        get_class_registration_repository
    ),
):
    classes = service.get_all_classes()
    counts = registration_repository.get_counts_by_class()
    return [to_response(db_class, counts.get(db_class.id, 0)) for db_class in classes]


@router.get("/{class_id}", response_model=ClassResponse)
def get_class_by_id(
    class_id: int,
    service: ClassService = Depends(get_class_service),
    registration_repository: ClassRegistrationRepository = Depends(
        get_class_registration_repository
    ),
):
    db_class = service.get_class_by_id(class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return to_response(db_class, registration_repository.get_count_for_class(class_id))


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: int,
    class_data: ClassUpdate,
    service: ClassService = Depends(get_class_service),
    registration_repository: ClassRegistrationRepository = Depends(
        get_class_registration_repository
    ),
):
    db_class = service.update_class(class_id, class_data)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return to_response(db_class, registration_repository.get_count_for_class(class_id))


@router.delete("/{class_id}", status_code=204)
def delete_class(class_id: int, service: ClassService = Depends(get_class_service)):
    deleted = service.delete_class(class_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Class not found")
