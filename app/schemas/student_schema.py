from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    age: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
