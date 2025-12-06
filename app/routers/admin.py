# file: api/routers/admin.py

from fastapi import APIRouter, Depends
from app.auth.auth_service import get_current_user
from app.services.admin_service import (
    create_employee,
    update_employee,
    deactivate_employee,
    get_fwmi_non_compliant,
    generate_coverage_report
)

router = APIRouter()

# Only ADMIN should access this:
def verify_admin(current_user):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

# POST /admin/employee
@router.post("/employee")
def create_employee_endpoint(
    data: dict,
    current_user = Depends(get_current_user)
):
    verify_admin(current_user)
    return create_employee(data)

# PUT
@router.put("/employee/{emp_id}")
def update_employee_endpoint(
    emp_id: int,
    data: dict,
    current_user = Depends(get_current_user)
):
    verify_admin(current_user)
    return update_employee(emp_id, data)

# DELETE
@router.delete("/employee/{emp_id}")
def deactivate_employee_endpoint(
    emp_id: int,
    current_user = Depends(get_current_user)
):
    verify_admin(current_user)
    return deactivate_employee(emp_id)

# GET non-compliance
@router.get("/fwmi/non-compliant")
def fwmi_non_compliant(
    current_user = Depends(get_current_user)
):
    verify_admin(current_user)
    return get_fwmi_non_compliant()

# Coverage report
@router.get("/coverage/report")
def coverage_report(
    current_user = Depends(get_current_user)
):
    verify_admin(current_user)
    return generate_coverage_report()
