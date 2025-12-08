# app/routers/importer.py

import pandas as pd
import io
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.database.database import get_session
from app.models.models import Employee
from app.models.employee_plan import EmployeePlan

router = APIRouter(prefix="/import", tags=["Import"])


@router.post("/employees")
async def import_employees(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """
    Import employees from Excel file.
    Supports multi-plan via 'Plan IDs' column (comma separated).
    """

    # 1️⃣ Read Excel safely
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), sheet_name="General")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Excel read error: {str(e)}")

    # 2️⃣ Check required columns
    required_cols = ["Employee Code", "Name", "Department", "Age", "Gender"]
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing}"
        )

    created_count = 0

    # 3️⃣ Process each row
    for _, row in df.iterrows():

        # Create employee record
        employee = Employee(
            employee_code=row["Employee Code"],
            name=row["Name"],
            department=row.get("Department"),
            age=int(row["Age"]) if not pd.isna(row["Age"]) else None,
            gender=row.get("Gender"),
            user_id=1  # TODO: assign appropriate user later
        )

        session.add(employee)
        session.commit()
        session.refresh(employee)

        # 4️⃣ Handle multiple plan IDs
        if "Plan IDs" in df.columns:
            if not pd.isna(row["Plan IDs"]):

                # Split (case: "1,2, 3")
                raw_values = str(row["Plan IDs"]).split(",")

                plan_ids: List[int] = []
                for value in raw_values:
                    value = value.strip()

                    # Convert from str/float to int
                    try:
                        plan_ids.append(int(float(value)))
                    except:
                        continue  # skip invalid values

                # Create EmployeePlan links
                for pid in plan_ids:
                    link = EmployeePlan(
                        employee_id=employee.employee_id,
                        plan_id=pid
                    )
                    session.add(link)

                session.commit()

        created_count += 1

    return {
        "message": "Excel import completed successfully",
        "employees_created": created_count
    }
