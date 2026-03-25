from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    name: str
    email: str
    salary: int
    field: str

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    salary: int
    field: str

    class Config:
        from_attributes = True