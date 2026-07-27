from sqlalchemy import Column, Integer, String

from app.database import Base


class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    classname = Column(String, nullable=False)
    section = Column(String, nullable=False)
