from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.class_repository import ClassRepository
from app.schemas.class_schema import ClassCreate, ClassResponse, ClassUpdate
from app.services.class_service import ClassService

router = APIRouter(prefix="/classes", tags=["classes"])


def get_class_service(db: Session = Depends(get_db)) -> ClassService:
    return ClassService(ClassRepository(db))


@router.post("", response_model=ClassResponse, status_code=201)
def register_class(
    class_data: ClassCreate, service: ClassService = Depends(get_class_service)
):
    return service.register_class(class_data)


@router.get("", response_model=list[ClassResponse])
def get_all_classes(service: ClassService = Depends(get_class_service)):
    return service.get_all_classes()


@router.get("/{class_id}", response_model=ClassResponse)
def get_class_by_id(
    class_id: int, service: ClassService = Depends(get_class_service)
):
    db_class = service.get_class_by_id(class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: int,
    class_data: ClassUpdate,
    service: ClassService = Depends(get_class_service),
):
    db_class = service.update_class(class_id, class_data)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class


@router.delete("/{class_id}", status_code=204)
def delete_class(class_id: int, service: ClassService = Depends(get_class_service)):
    deleted = service.delete_class(class_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Class not found")
