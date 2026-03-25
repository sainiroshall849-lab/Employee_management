"""
Business logic services for employee operations.
Handles all CRUD operations with proper error handling and validation.
"""

import logging
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from Models.employee_models import Employee

logger = logging.getLogger(__name__)


def validate_employee_data(name: str, email: str, field: str, salary: int) -> Tuple[bool, str]:
    """
    Validate employee data before database operations.

    Args:
        name: Employee name
        email: Employee email
        field: Employee department
        salary: Employee salary

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Validate name
        if not name or not isinstance(name, str):
            return False, "Name is required and must be a string"
        name = name.strip()
        if len(name) < 2 or len(name) > 100:
            return False, "Name must be between 2 and 100 characters"

        # Validate email
        if not email or not isinstance(email, str):
            return False, "Email is required and must be a string"
        email = email.strip().lower()
        if len(email) > 254:
            return False, "Email is too long"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"

        # Validate field
        if not field or not isinstance(field, str):
            return False, "Field is required and must be a string"
        field = field.strip()
        if len(field) < 2 or len(field) > 100:
            return False, "Field must be between 2 and 100 characters"

        # Validate salary
        if salary is None or not isinstance(salary, int):
            return False, "Salary is required and must be an integer"
        if salary < 0:
            return False, "Salary cannot be negative"
        if salary > 10000000:
            return False, "Salary exceeds maximum allowed amount"

        return True, ""

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return False, f"Validation failed: {str(e)}"


def create_employee(
    db: Session,
    name: str,
    email: str,
    field: str,
    salary: int
) -> Tuple[Optional[Employee], str]:
    """
    Create a new employee record.

    Args:
        db: Database session
        name: Employee name
        email: Employee email
        field: Employee department
        salary: Employee salary

    Returns:
        Tuple of (Employee object or None, error message)
    """
    try:
        logger.info(f"Creating employee: {name} ({email})")

        # Validate input data
        is_valid, error = validate_employee_data(name, email, field, salary)
        if not is_valid:
            logger.warning(f"Invalid employee data: {error}")
            return None, error

        # Create employee instance
        employee = Employee(
            name=name.strip(),
            email=email.strip().lower(),
            field=field.strip(),
            salary=salary
        )

        # Save to database
        db.add(employee)
        db.commit()
        db.refresh(employee)

        logger.info(f"Employee created successfully: ID {employee.id}")
        return employee, ""

    except IntegrityError as e:
        db.rollback()
        error_msg = "Email already exists in the system"
        logger.error(f"Integrity error creating employee: {str(e)}")
        return None, error_msg
    except SQLAlchemyError as e:
        db.rollback()
        error_msg = "Database error occurred while creating employee"
        logger.error(f"Database error: {str(e)}")
        return None, error_msg
    except Exception as e:
        db.rollback()
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error creating employee: {str(e)}")
        return None, error_msg


def get_all_employees(db: Session) -> Tuple[List[Employee], str]:
    """
    Retrieve all employee records.

    Args:
        db: Database session

    Returns:
        Tuple of (list of employees, error message)
    """
    try:
        logger.info("Retrieving all employees")
        employees = db.query(Employee).all()

        logger.info(f"Retrieved {len(employees)} employees")
        return employees, ""

    except SQLAlchemyError as e:
        error_msg = "Database error occurred while retrieving employees"
        logger.error(f"Database error: {str(e)}")
        return [], error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error retrieving employees: {str(e)}")
        return [], error_msg


def get_employee(db: Session, employee_id: int) -> Tuple[Optional[Employee], str]:
    """
    Retrieve a specific employee by ID.

    Args:
        db: Database session
        employee_id: Employee ID

    Returns:
        Tuple of (Employee object or None, error message)
    """
    try:
        if not isinstance(employee_id, int) or employee_id <= 0:
            error_msg = "Invalid employee ID"
            logger.warning(f"Invalid employee ID provided: {employee_id}")
            return None, error_msg

        logger.info(f"Retrieving employee with ID: {employee_id}")
        employee = db.query(Employee).filter(Employee.id == employee_id).first()

        if not employee:
            logger.info(f"Employee not found: ID {employee_id}")
            return None, "Employee not found"

        logger.info(f"Employee retrieved: {employee.name} (ID {employee.id})")
        return employee, ""

    except SQLAlchemyError as e:
        error_msg = "Database error occurred while retrieving employee"
        logger.error(f"Database error: {str(e)}")
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error retrieving employee: {str(e)}")
        return None, error_msg


def update_employee(
    db: Session,
    employee_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    field: Optional[str] = None,
    salary: Optional[int] = None
) -> Tuple[Optional[Employee], str]:
    """
    Update an existing employee record.

    Args:
        db: Database session
        employee_id: Employee ID
        name: New name (optional)
        email: New email (optional)
        field: New field (optional)
        salary: New salary (optional)

    Returns:
        Tuple of (Updated Employee object or None, error message)
    """
    try:
        if not isinstance(employee_id, int) or employee_id <= 0:
            error_msg = "Invalid employee ID"
            logger.warning(f"Invalid employee ID provided: {employee_id}")
            return None, error_msg

        logger.info(f"Updating employee with ID: {employee_id}")

        # Find employee
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            logger.info(f"Employee not found for update: ID {employee_id}")
            return None, "Employee not found"

        # Track if any changes were made
        changes_made = False

        # Update fields if provided
        if name is not None:
            is_valid, error = validate_employee_data(name, "test@test.com", "test", 1000)[0], ""
            if not is_valid:
                return None, f"Invalid name: {error}"
            employee.name = name.strip()
            changes_made = True

        if email is not None:
            is_valid, error = validate_employee_data("test", email, "test", 1000)[0], ""
            if not is_valid:
                return None, f"Invalid email: {error}"
            employee.email = email.strip().lower()
            changes_made = True

        if field is not None:
            is_valid, error = validate_employee_data("test", "test@test.com", field, 1000)[0], ""
            if not is_valid:
                return None, f"Invalid field: {error}"
            employee.field = field.strip()
            changes_made = True

        if salary is not None:
            is_valid, error = validate_employee_data("test", "test@test.com", "test", salary)[0], ""
            if not is_valid:
                return None, f"Invalid salary: {error}"
            employee.salary = salary
            changes_made = True

        if not changes_made:
            return employee, "No changes provided"

        # Save changes
        db.commit()
        db.refresh(employee)

        logger.info(f"Employee updated successfully: ID {employee.id}")
        return employee, ""

    except IntegrityError as e:
        db.rollback()
        error_msg = "Email already exists or data conflict occurred"
        logger.error(f"Integrity error updating employee: {str(e)}")
        return None, error_msg
    except SQLAlchemyError as e:
        db.rollback()
        error_msg = "Database error occurred while updating employee"
        logger.error(f"Database error: {str(e)}")
        return None, error_msg
    except Exception as e:
        db.rollback()
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error updating employee: {str(e)}")
        return None, error_msg


def delete_employee(db: Session, employee_id: int) -> Tuple[bool, str]:
    """
    Delete an employee record.

    Args:
        db: Database session
        employee_id: Employee ID

    Returns:
        Tuple of (success status, message)
    """
    try:
        if not isinstance(employee_id, int) or employee_id <= 0:
            error_msg = "Invalid employee ID"
            logger.warning(f"Invalid employee ID provided: {employee_id}")
            return False, error_msg

        logger.info(f"Deleting employee with ID: {employee_id}")

        # Find employee
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            logger.info(f"Employee not found for deletion: ID {employee_id}")
            return False, "Employee not found"

        # Delete employee
        db.delete(employee)
        db.commit()

        logger.info(f"Employee deleted successfully: ID {employee_id} - {employee.name}")
        return True, "Employee deleted successfully"

    except SQLAlchemyError as e:
        db.rollback()
        error_msg = "Database error occurred while deleting employee"
        logger.error(f"Database error: {str(e)}")
        return False, error_msg
    except Exception as e:
        db.rollback()
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error deleting employee: {str(e)}")
        return False, error_msg