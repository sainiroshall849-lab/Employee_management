"""
API routes for employee management endpoints.
Provides RESTful CRUD operations with proper error handling and responses.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from Schemas.employee_schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
    APIResponse
)
from Services import employee_services

logger = logging.getLogger(__name__)

# Create router with versioning and documentation
router = APIRouter(
    prefix="/employees",
    tags=["Employee Management"],
    responses={
        400: {"description": "Bad Request - Invalid input data"},
        404: {"description": "Not Found - Employee not found"},
        422: {"description": "Validation Error - Input validation failed"},
        500: {"description": "Internal Server Error"}
    }
)


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee",
    description="Create a new employee record in the system",
    response_description="Successfully created employee"
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
) -> EmployeeResponse:
    """
    Create a new employee.

    - **name**: Employee full name (2-100 characters)
    - **email**: Unique email address
    - **salary**: Salary amount (non-negative integer)
    - **field**: Department/field (2-100 characters)

    Returns the created employee with ID and timestamps.
    """
    try:
        logger.info(f"API request: Create employee - {employee_data.name}")

        employee, error = employee_services.create_employee(
            db,
            employee_data.name,
            employee_data.email,
            employee_data.field,
            employee_data.salary
        )

        if employee is None:
            logger.warning(f"Failed to create employee: {error}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )

        logger.info(f"Employee created via API: ID {employee.id}")
        return employee

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_employee endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while creating employee"
        )


@router.get(
    "/",
    response_model=EmployeeListResponse,
    summary="List All Employees",
    description="Retrieve all employee records with pagination info",
    response_description="List of all employees with total count"
)
def get_all_employees(db: Session = Depends(get_db)) -> EmployeeListResponse:
    """
    Get all employees.

    Returns a list of all employees in the system with total count.
    """
    try:
        logger.info("API request: Get all employees")

        employees, error = employee_services.get_all_employees(db)

        if error:
            logger.error(f"Failed to retrieve employees: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error
            )

        return EmployeeListResponse(
            total=len(employees),
            employees=employees
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_all_employees endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving employees"
        )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get Employee by ID",
    description="Retrieve a specific employee by their unique ID",
    response_description="Employee details"
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
) -> EmployeeResponse:
    """
    Get employee by ID.

    - **employee_id**: Unique employee identifier (must be positive integer)
    """
    try:
        logger.info(f"API request: Get employee by ID - {employee_id}")

        if employee_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Employee ID must be a positive integer"
            )

        employee, error = employee_services.get_employee(db, employee_id)

        if employee is None:
            logger.info(f"Employee not found: ID {employee_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error or "Employee not found"
            )

        return employee

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_employee endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving employee"
        )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update Employee",
    description="Update an existing employee's information",
    response_description="Updated employee details"
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
) -> EmployeeResponse:
    """
    Update employee information.

    - **employee_id**: Unique employee identifier
    - **employee_data**: Fields to update (all optional for partial updates)

    Only provided fields will be updated.
    """
    try:
        logger.info(f"API request: Update employee - ID {employee_id}")

        if employee_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Employee ID must be a positive integer"
            )

        employee, error = employee_services.update_employee(
            db,
            employee_id,
            employee_data.name,
            employee_data.email,
            employee_data.field,
            employee_data.salary
        )

        if employee is None:
            if error == "Employee not found":
                logger.info(f"Employee not found for update: ID {employee_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=error
                )
            else:
                logger.warning(f"Failed to update employee: {error}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error
                )

        logger.info(f"Employee updated via API: ID {employee_id}")
        return employee

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update_employee endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while updating employee"
        )


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Employee",
    description="Delete an employee record from the system",
    response_description="Deletion confirmation"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Delete employee by ID.

    - **employee_id**: Unique employee identifier

    Returns success confirmation.
    """
    try:
        logger.info(f"API request: Delete employee - ID {employee_id}")

        if employee_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Employee ID must be a positive integer"
            )

        success, error = employee_services.delete_employee(db, employee_id)

        if not success:
            if error == "Employee not found":
                logger.info(f"Employee not found for deletion: ID {employee_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=error
                )
            else:
                logger.warning(f"Failed to delete employee: {error}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error
                )

        logger.info(f"Employee deleted via API: ID {employee_id}")
        return APIResponse(
            success=True,
            message="Employee deleted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in delete_employee endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while deleting employee"
        )