from sqlalchemy import Column, Integer, String
from db.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    field = Column(String(100))
    salary = Column(Integer)