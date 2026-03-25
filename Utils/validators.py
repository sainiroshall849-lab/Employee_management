"""Validation utilities for employee data."""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"
    
    email = email.strip()
    
    if len(email) > 254:
        return False, "Email is too long (max 254 characters)"
    
    # Simple email regex pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""


def validate_employee_name(name: str) -> Tuple[bool, str]:
    """
    Validate employee name.
    
    Args:
        name: Name string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, "Name is required and must be a string"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Name must not exceed 100 characters"
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    pattern = r"^[a-zA-Z\s\-']+$"
    if not re.match(pattern, name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, ""


def validate_salary(salary: int) -> Tuple[bool, str]:
    """
    Validate employee salary.
    
    Args:
        salary: Salary amount to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if salary is None:
        return False, "Salary is required"
    
    if not isinstance(salary, int):
        return False, "Salary must be an integer"
    
    if salary < 0:
        return False, "Salary cannot be negative"
    
    if salary > 10000000:  # Reasonable upper limit
        return False, "Salary exceeds maximum allowed amount"
    
    return True, ""


def validate_field(field: str) -> Tuple[bool, str]:
    """
    Validate employee field/department.
    
    Args:
        field: Field/department string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not field or not isinstance(field, str):
        return False, "Field is required and must be a string"
    
    field = field.strip()
    
    if len(field) < 2:
        return False, "Field must be at least 2 characters long"
    
    if len(field) > 100:
        return False, "Field must not exceed 100 characters"
    
    return True, ""
