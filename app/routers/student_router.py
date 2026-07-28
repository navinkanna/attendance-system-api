from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.student_repository import StudentRepository
from app.schemas.student_schema import StudentCreate, StudentResponse, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])


def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    return StudentService(StudentRepository(db))


@router.post("", response_model=StudentResponse, status_code=201)
def register_student(
    student_data: StudentCreate, service: StudentService = Depends(get_student_service)
):
    return service.register_student(student_data)


@router.get("", response_model=list[StudentResponse])
def get_all_students(service: StudentService = Depends(get_student_service)):
    return service.get_all_students()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student_by_id(
    student_id: int, service: StudentService = Depends(get_student_service)
):
    db_student = service.get_student_by_id(student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    service: StudentService = Depends(get_student_service),
):
    db_student = service.update_student(student_id, student_data)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.delete("/{student_id}", status_code=204)
def delete_student(
    student_id: int, service: StudentService = Depends(get_student_service)
):
    deleted = service.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
