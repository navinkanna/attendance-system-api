from app.models.class_model import SchoolClass
from app.repositories.class_repository import ClassRepository
from app.schemas.class_schema import ClassCreate, ClassUpdate


class ClassService:
    def __init__(self, repository: ClassRepository):
        self.repository = repository

    def register_class(self, class_data: ClassCreate) -> SchoolClass:
        return self.repository.create(class_data)

    def get_all_classes(self) -> list[SchoolClass]:
        return self.repository.get_all()

    def get_class_by_id(self, class_id: int) -> SchoolClass | None:
        return self.repository.get_by_id(class_id)

    def update_class(self, class_id: int, class_data: ClassUpdate) -> SchoolClass | None:
        return self.repository.update(class_id, class_data)

    def delete_class(self, class_id: int) -> bool:
        return self.repository.delete(class_id)
