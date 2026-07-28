from datetime import date as date_type

from sqlalchemy.orm import Session

from app.models.attendance_model import Attendance
from app.models.student_model import Student
from app.schemas.attendance_schema import AttendanceRecordIn


class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_for_class_date(self, class_id: int, date: date_type) -> list[Attendance]:
        return (
            self.db.query(Attendance)
            .filter(Attendance.class_id == class_id, Attendance.date == date)
            .all()
        )

    def get_dates_for_class(self, class_id: int) -> list[date_type]:
        rows = (
            self.db.query(Attendance.date)
            .filter(Attendance.class_id == class_id)
            .distinct()
            .order_by(Attendance.date.desc())
            .all()
        )
        return [row[0] for row in rows]

    def get_for_class_date_with_students(
        self, class_id: int, date: date_type
    ) -> list[tuple[Attendance, Student]]:
        return (
            self.db.query(Attendance, Student)
            .join(Student, Student.id == Attendance.student_id)
            .filter(Attendance.class_id == class_id, Attendance.date == date)
            .order_by(Student.first_name, Student.last_name)
            .all()
        )

    def replace_for_class_date(
        self, class_id: int, date: date_type, records: list[AttendanceRecordIn]
    ) -> list[Attendance]:
        self.db.query(Attendance).filter(
            Attendance.class_id == class_id, Attendance.date == date
        ).delete()
        for record in records:
            self.db.add(
                Attendance(
                    date=date,
                    class_id=class_id,
                    student_id=record.student_id,
                    is_present=record.is_present,
                )
            )
        self.db.commit()
        return self.get_for_class_date(class_id, date)
