# file: api/routers/employee.py

from fastapi import APIRouter, Depends
from api.auth.auth_service import get_current_user
from api.services.employee_service import (
    get_employee_coverage,
    get_ward_class_and_limits
)

router = APIRouter()

# GET /employee/me/coverage
@router.get("/me/coverage")
def my_coverage(current_user = Depends(get_current_user)):
    return get_employee_coverage(current_user.username)

# GET /employee/me/ward-info
@router.get("/me/ward-info")
def my_ward_info(current_user = Depends(get_current_user)):
    return get_ward_class_and_limits(current_user.username)
