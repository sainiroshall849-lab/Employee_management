"""
Pydantic schemas for Employee API requests and responses.
Includes validation and data models for all CRUD operations.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationError


class EmployeeBase(BaseModel):
    """
    Base schema with common employee fields and validation.

    Attributes:
        name: Employee's full name
        email: Employee's email address
        salary: Employee's salary
        field: Employee's department/field
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Employee full name"
    )
    email: str = Field(
        ...,
        max_length=100,
        description="Employee email address"
    )
    salary: int = Field(
        ...,
        ge=0,
        le=10000000,
        description="Employee salary (must be non-negative)"
    )
    field: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Employee department/field"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Validate and clean employee name."""
        if not value or not isinstance(value, str):
            raise ValueError("Name is required and must be a string")

        value = value.strip()
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(value) > 100:
            raise ValueError("Name must not exceed 100 characters")

        # Allow only letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", value):
            raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Validate and clean email address."""
        if not value or not isinstance(value, str):
            raise ValueError("Email is required and must be a string")

        value = value.strip().lower()
        if len(value) > 254:
            raise ValueError("Email is too long (max 254 characters)")

        # Basic email regex pattern
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")

        return value

    @field_validator("field")
    @classmethod
    def validate_field(cls, value: str) -> str:
        """Validate and clean field/department."""
        if not value or not isinstance(value, str):
            raise ValueError("Field is required and must be a string")

        value = value.strip()
        if len(value) < 2:
            raise ValueError("Field must be at least 2 characters long")
        if len(value) > 100:
            raise ValueError("Field must not exceed 100 characters")

        return value


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee."""
    pass


class EmployeeUpdate(BaseModel):
    """
    Schema for updating an existing employee.
    All fields are optional for partial updates.
    """

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    salary: Optional[int] = Field(None, ge=0, le=10000000)
    field: Optional[str] = Field(None, min_length=2, max_length=100)

    @field_validator("name", "field")
    @classmethod
    def validate_string_fields(cls, value: str) -> Optional[str]:
        """Validate optional string fields."""
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Field cannot be empty")
        return value

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str) -> Optional[str]:
        """Validate optional email field."""
        if value is not None:
            value = value.strip().lower()
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
                raise ValueError("Invalid email format")
        return value


class EmployeeResponse(EmployeeBase):
    """
    Schema for employee response data.
    Includes all fields plus timestamps.
    """

    id: int = Field(..., description="Unique employee identifier")
    created_at: str = Field(..., description="Record creation timestamp")
    updated_at: str = Field(..., description="Record last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class EmployeeListResponse(BaseModel):
    """
    Schema for paginated employee list response.
    """

    total: int = Field(..., description="Total number of employees")
    employees: list[EmployeeResponse] = Field(..., description="List of employees")


class APIResponse(BaseModel):
    """
    Generic API response schema for success/error messages.
    """

    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[dict] = Field(None, description="Optional response data")