from pydantic import BaseModel


class ClassRegistrationUpdate(BaseModel):
    student_ids: list[int]
