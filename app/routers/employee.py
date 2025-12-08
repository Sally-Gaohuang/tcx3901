# file: app/routers/employee.py

from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, delete

from app.database.database import engine
from app.models.models import (
    Employee,
    EmployeeCreate,
    EmployeeUpdate,
)
from app.models.employee_plan import EmployeePlan

router = APIRouter()


# =========================
#  CREATE EMPLOYEE
# =========================
@router.post("/", response_model=Employee)
def create_employee(data: EmployeeCreate):
    """
    Create a new employee and link to one or more plans.
    """
    with Session(engine) as session:
        # 1) Create Employee row
        employee = Employee(
            user_id=data.user_id,
            employee_code=data.employee_code,
            name=data.name,
            department=data.department,
            age=data.age,
            gender=data.gender,
        )
        session.add(employee)
        session.commit()
        session.refresh(employee)

        # 2) Link Employee to Plans via EmployeePlan
        for plan_id in data.plan_ids or []:
            link = EmployeePlan(
                employee_id=employee.employee_id,
                plan_id=plan_id,
            )
            session.add(link)

        session.commit()
        session.refresh(employee)
        return employee


# =========================
#  LIST ALL EMPLOYEES
# =========================
@router.get("/", response_model=List[Employee])
def list_employees():
    """
    Return all employees.
    Note: each Employee will include its related Plans.
    """
    with Session(engine) as session:
        employees = session.exec(select(Employee)).all()
        return employees


# =========================
#  GET SINGLE EMPLOYEE
# =========================
@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    """
    Return one employee by ID, including its Plans.
    """
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee


# =========================
#  UPDATE EMPLOYEE
# =========================
@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, data: EmployeeUpdate):
    """
    Update basic employee info and optionally replace their plan list.
    """
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        update_data = data.dict(exclude_unset=True)

        # 1) Update simple fields
        simple_fields = ["name", "department", "age", "gender"]
        for field in simple_fields:
            if field in update_data:
                setattr(employee, field, update_data[field])

        # 2) Replace plan links if plan_ids provided
        if "plan_ids" in update_data and update_data["plan_ids"] is not None:
            new_plan_ids = update_data["plan_ids"]

            # Delete existing links
            session.exec(
                delete(EmployeePlan).where(
                    EmployeePlan.employee_id == employee.employee_id
                )
            )

            # Insert new links
            for pid in new_plan_ids:
                link = EmployeePlan(
                    employee_id=employee.employee_id,
                    plan_id=pid,
                )
                session.add(link)

        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


# =========================
#  DELETE EMPLOYEE
# =========================
@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    """
    Delete an employee and all their plan links.
    """
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Remove links first
        session.exec(
            delete(EmployeePlan).where(EmployeePlan.employee_id == employee_id)
        )

        # Delete employee row
        session.delete(employee)
        session.commit()

        return {"message": "Employee deleted"}
