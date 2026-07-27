from sqlalchemy.orm import Session

from app.models.class_model import SchoolClass
from app.schemas.class_schema import ClassCreate, ClassUpdate


class ClassRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, class_data: ClassCreate) -> SchoolClass:
        db_class = SchoolClass(
            classname=class_data.classname, section=class_data.section
        )
        self.db.add(db_class)
        self.db.commit()
        self.db.refresh(db_class)
        return db_class

    def get_all(self) -> list[SchoolClass]:
        return self.db.query(SchoolClass).all()

    def get_by_id(self, class_id: int) -> SchoolClass | None:
        return self.db.query(SchoolClass).filter(SchoolClass.id == class_id).first()

    def update(self, class_id: int, class_data: ClassUpdate) -> SchoolClass | None:
        db_class = self.get_by_id(class_id)
        if db_class is None:
            return None
        db_class.classname = class_data.classname
        db_class.section = class_data.section
        self.db.commit()
        self.db.refresh(db_class)
        return db_class

    def delete(self, class_id: int) -> bool:
        db_class = self.get_by_id(class_id)
        if db_class is None:
            return False
        self.db.delete(db_class)
        self.db.commit()
        return True
