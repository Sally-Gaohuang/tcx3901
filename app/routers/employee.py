from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.database.database import engine
from app.models.models import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter()


# ------------------------------
# CREATE EMPLOYEE
# ------------------------------
@router.post("/")
def create_employee(data: EmployeeCreate):
    employee = Employee(**data.dict())

    with Session(engine) as session:
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


# ------------------------------
# READ ALL EMPLOYEES
# ------------------------------
@router.get("/")
def list_employees():
    with Session(engine) as session:
        employees = session.exec(select(Employee)).all()
        return employees


# ------------------------------
# READ ONE EMPLOYEE
# ------------------------------
@router.get("/{employee_id}")
def get_employee(employee_id: int):
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(404, "Employee not found")
        return employee


# ------------------------------
# UPDATE EMPLOYEE
# ------------------------------
@router.put("/{employee_id}")
def update_employee(employee_id: int, data: EmployeeUpdate):
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(404, "Employee not found")

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(employee, key, value)

        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


# ------------------------------
# DELETE EMPLOYEE
# ------------------------------
@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(404, "Employee not found")

        session.delete(employee)
        session.commit()
        return {"message": "Employee deleted"}
