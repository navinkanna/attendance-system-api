from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from app.database import Base


class ClassRegistration(Base):
    __tablename__ = "class_registrations"
    __table_args__ = (
        UniqueConstraint("class_id", "student_id", name="uq_class_registrations_class_student"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
