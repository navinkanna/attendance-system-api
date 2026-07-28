from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, UniqueConstraint

from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("class_id", "student_id", "date", name="uq_attendance_class_student_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    is_present = Column(Boolean, nullable=False)
