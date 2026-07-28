from pydantic import BaseModel, ConfigDict


class ClassBase(BaseModel):
    classname: str
    section: str


class ClassCreate(ClassBase):
    pass


class ClassUpdate(ClassBase):
    pass


class ClassResponse(ClassBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_count: int = 0
