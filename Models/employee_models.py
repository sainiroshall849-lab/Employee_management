"""
Database models for the Employee Management System.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.database import Base


class Employee(Base):
    """
    Employee database model representing the employees table.

    Attributes:
        id: Unique identifier for the employee
        name: Employee's full name
        email: Employee's email address (unique)
        field: Employee's department or field
        salary: Employee's salary
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """

    __tablename__ = "employees"
    __table_args__ = {"comment": "Employee records table"}

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique employee identifier"
    )
    name = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Employee full name"
    )
    email = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="Employee email address"
    )
    field = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Employee department/field"
    )
    salary = Column(
        Integer,
        nullable=False,
        comment="Employee salary in dollars"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Record last update timestamp"
    )

    def __repr__(self) -> str:
        """String representation of Employee instance."""
        return f"<Employee(id={self.id}, name='{self.name}', email='{self.email}')>"