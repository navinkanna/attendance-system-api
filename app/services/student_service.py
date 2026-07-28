from app.models.student_model import Student
from app.repositories.student_repository import StudentRepository
from app.schemas.student_schema import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def register_student(self, student_data: StudentCreate) -> Student:
        return self.repository.create(student_data)

    def get_all_students(self) -> list[Student]:
        return self.repository.get_all()

    def get_student_by_id(self, student_id: int) -> Student | None:
        return self.repository.get_by_id(student_id)

    def update_student(self, student_id: int, student_data: StudentUpdate) -> Student | None:
        return self.repository.update(student_id, student_data)

    def delete_student(self, student_id: int) -> bool:
        return self.repository.delete(student_id)
