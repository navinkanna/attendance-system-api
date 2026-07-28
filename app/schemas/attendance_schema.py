from datetime import date as date_type

from pydantic import BaseModel, ConfigDict


class AttendanceRecordIn(BaseModel):
    student_id: int
    is_present: bool


class AttendanceSaveRequest(BaseModel):
    records: list[AttendanceRecordIn]


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date_type
    class_id: int
    student_id: int
    is_present: bool


class AttendanceHistoryEntry(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    is_present: bool
