from datetime import date as date_type

from app.models.attendance_model import Attendance
from app.repositories.attendance_repository import AttendanceRepository
from app.schemas.attendance_schema import AttendanceHistoryEntry, AttendanceRecordIn


class AttendanceService:
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def get_for_class_today(self, class_id: int) -> list[Attendance]:
        return self.repository.get_for_class_date(class_id, date_type.today())

    def save_for_class_today(
        self, class_id: int, records: list[AttendanceRecordIn]
    ) -> list[Attendance]:
        return self.repository.replace_for_class_date(class_id, date_type.today(), records)

    def get_dates_for_class(self, class_id: int) -> list[date_type]:
        return self.repository.get_dates_for_class(class_id)

    def get_history_for_class_date(
        self, class_id: int, date: date_type
    ) -> list[AttendanceHistoryEntry]:
        rows = self.repository.get_for_class_date_with_students(class_id, date)
        return [
            AttendanceHistoryEntry(
                student_id=student.id,
                first_name=student.first_name,
                last_name=student.last_name,
                is_present=attendance.is_present,
            )
            for attendance, student in rows
        ]
