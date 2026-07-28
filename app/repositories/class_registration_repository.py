from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.class_registration_model import ClassRegistration
from app.models.student_model import Student


class ClassRegistrationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_registered_students(self, class_id: int) -> list[Student]:
        return (
            self.db.query(Student)
            .join(ClassRegistration, ClassRegistration.student_id == Student.id)
            .filter(ClassRegistration.class_id == class_id)
            .all()
        )

    def get_count_for_class(self, class_id: int) -> int:
        return (
            self.db.query(func.count(ClassRegistration.id))
            .filter(ClassRegistration.class_id == class_id)
            .scalar()
            or 0
        )

    def get_counts_by_class(self) -> dict[int, int]:
        rows = (
            self.db.query(ClassRegistration.class_id, func.count(ClassRegistration.id))
            .group_by(ClassRegistration.class_id)
            .all()
        )
        return dict(rows)

    def replace_registrations(self, class_id: int, student_ids: list[int]) -> list[Student]:
        self.db.query(ClassRegistration).filter(
            ClassRegistration.class_id == class_id
        ).delete()
        for student_id in student_ids:
            self.db.add(ClassRegistration(class_id=class_id, student_id=student_id))
        self.db.commit()
        return self.get_registered_students(class_id)
