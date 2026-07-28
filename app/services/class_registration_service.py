from app.models.student_model import Student
from app.repositories.class_registration_repository import ClassRegistrationRepository


class ClassRegistrationService:
    def __init__(self, repository: ClassRegistrationRepository):
        self.repository = repository

    def get_registered_students(self, class_id: int) -> list[Student]:
        return self.repository.get_registered_students(class_id)

    def replace_registrations(self, class_id: int, student_ids: list[int]) -> list[Student]:
        return self.repository.replace_registrations(class_id, student_ids)
