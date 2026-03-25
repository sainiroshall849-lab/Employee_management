from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from Schemas.employee_schemas import EmployeeCreate, EmployeeResponse
from Services import employee_services as employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeResponse)
def create(emp: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, emp.name, emp.email, emp.field, emp.salary)

@router.get("/", response_model=list[EmployeeResponse])
def get_all(db: Session = Depends(get_db)):
    return employee_service.get_all_employees(db)

@router.get("/{emp_id}", response_model=EmployeeResponse)
def get_one(emp_id: int, db: Session = Depends(get_db)):
    result = employee_service.get_employee(db, emp_id)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result

@router.put("/{emp_id}", response_model=EmployeeResponse)
def update(emp_id: int, emp: EmployeeCreate, db: Session = Depends(get_db)):
    result = employee_service.update_employee(db, emp_id, emp.name, emp.email, emp.field, emp.salary)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result

@router.delete("/{emp_id}")
def delete(emp_id: int, db: Session = Depends(get_db)):
    result = employee_service.delete_employee(db, emp_id)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}