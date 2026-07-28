from sqlalchemy.orm import Session

from app.models.student_model import Student
from app.schemas.student_schema import StudentCreate, StudentUpdate


class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, student_data: StudentCreate) -> Student:
        db_student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            age=student_data.age,
        )
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def get_all(self) -> list[Student]:
        return self.db.query(Student).all()

    def get_by_id(self, student_id: int) -> Student | None:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def update(self, student_id: int, student_data: StudentUpdate) -> Student | None:
        db_student = self.get_by_id(student_id)
        if db_student is None:
            return None
        db_student.first_name = student_data.first_name
        db_student.last_name = student_data.last_name
        db_student.age = student_data.age
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def delete(self, student_id: int) -> bool:
        db_student = self.get_by_id(student_id)
        if db_student is None:
            return False
        self.db.delete(db_student)
        self.db.commit()
        return True
