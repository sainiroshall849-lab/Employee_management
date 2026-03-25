from sqlalchemy.orm import Session
from Models.employee_models import Employee

def create_employee(db: Session, name: str, email: str, field: str, salary: int):
    emp = Employee(name=name, email=email, field=field, salary=salary)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def get_all_employees(db: Session):
    return db.query(Employee).all()

def get_employee(db: Session, emp_id: int):
    return db.query(Employee).filter(Employee.id == emp_id).first()

def update_employee(db: Session, emp_id: int, name: str, email: str, field: str, salary: int):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if emp:
        emp.name = name
        emp.email = email
        emp.field = field
        emp.salary = salary
        db.commit()
        db.refresh(emp)
    return emp

def delete_employee(db: Session, emp_id: int):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if emp:
        db.delete(emp)
        db.commit()
    return emp