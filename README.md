# TCX3901 Insurance Checking Portal
1. Project Description
bash```
The Insurance Checking Portal is a backend-driven web system designed to automate the insurance management workflow at Kurihara Kogyo Co. Ltd. The system provides:
Daily-use features such as employee insurance self-checking
HR operational tools for plan assignment and compliance checking
Annual bidding functions for insurers to submit quotes
This platform replaces Excel-based manual processes with a modern FastAPI–MySQL solution deployed on the NUS SoC VM using Docker.```
2. Setup
Step 1 — Clone the repository
bash```
git clone https://github.com/<your-repo>.git
cd insurance-checking-portal```

Step 2 — Start the system with Docker
bash```
docker-compose up -d```


This starts:
bash```
FastAPI backend (port 8000)
MySQL database (port 3306)
```
Step 3 — Access API docs
bash```
http://<vm-hostname>:8000/docs```

3. Code Structure
bash```
insurance-checking-portal/
│
├── api/                  # FastAPI backend
│   ├── main.py           # main entry point
│   ├── auth/             # JWT authentication
│   ├── models/           # SQLModel ORM models
│   ├── routers/          # API endpoints
│   ├── services/         # business logic (plan assignment, compliance)
│   ├── database.py       # DB connection
│   ├── seed.py           # initial coverage & plan seeds
│
├── sql/                  # SQL migration / seed scripts
│
├── web/                  # (Optional) Frontend files
│
├── docker-compose.yml    # containers (backend + mysql)
├── requirements.txt      # Python dependencies
└── README.md             # documentation
```

4. User Stories

4.1 Employee User Stories

bash```
As an employee, I want to view my insurance coverage so that I know my entitlements (GTL, GCI, GPA, GHS, GMM, FWMI).
As an employee, I want to see claim document requirements so that I can prepare claims properly.
As a WP/S-Pass holder, I want to check FWMI compliance so that I feel secure about my coverage.
As an employee, I want to verify my ward class and limits before hospital visits so I can inform hospitals accurately.
```

4.2 HR Admin User Stories

bash```
As an HR admin, I want to manage employee records so that insurance headcount remains accurate.
As an HR admin, I want automatic plan assignment based on designation so that coverage allocation follows AIA plans.
As an HR admin, I want to check FWMI non-compliance so that I avoid MOM penalties.
As an HR admin, I want to compare insurer bids side-by-side so that I can choose the most cost-effective insurer.
As an HR admin, I want to generate coverage reports so that I can submit them to management.
```

4.3 Insurer User Stories

bash```
As an insurer, I want to view required categories so that I can prepare accurate quotations.
As an insurer, I want to submit premiums for each policy type so that HR can evaluate my bids.
As an insurer, I want to revise my bids before submission deadlines so that I can correct mistakes.
```

5. System Architecture

bash```
+-----------------------------------------------------------+
|                   Frontend / Web Layer                    |
|   - Employee Dashboard                                    |
|   - Admin Dashboard                                       |
|   - Insurer Bid Portal                                    |
+-----------------------------------------------------------+
```
bash```
                    ⬇ HTTPS (JWT Protected)

+-----------------------------------------------------------+
|                    FastAPI Application Layer              |
|   - Authentication (JWT)                                  |
|   - Employee Coverage API                                 |
|   - Admin CRUD & Compliance API                           |
|   - Insurer Bidding API                                   |
|   - Reporting/Export                                      |
|   - Plan Assignment Engine                                |
+-----------------------------------------------------------+
```
bash```
                    ⬇ SQLModel ORM

+-----------------------------------------------------------+
|                        MySQL Database                     |
|   Tables: users, employees, plans, policy_categories,     |
|   plan_tiers, employee_coverage, insurers, bids,          |
|   bidding_rounds                                          |
+-----------------------------------------------------------+
```

6. API Summary

- Authentication

bash```
POST /login — JWT login
```

- Employee

bash```
GET /employees/{id}/coverage — View personal coverage
GET /employees/{id}/claims — View required documents
```

- Admin

bash```
POST /employees
PUT /employees/{id}
GET /coverage/compliance/fwmi
GET /bidding/summary

- Insurer
POST /bids
PUT /bids/{id}
GET /bidding_rounds/current
```

- OpenAPI documentation:

bash```
<vm-host>:8000/docs
```

7. Database Schema

- Key Tables

bash```
employees — Name, designation, category, project code
plans — Plan 1/2/3/4 definitions (extracted from AIA document)
policy_categories — GTL, GCI, GPA, GHS, GMM, FWMI
plan_tiers — mapping of plan → policy → coverage value
employee_coverage — auto-assigned coverage
insurers, bids, bidding_rounds — annual bidding logic
```

Full coverage values are sourced from the AIA Group Insurance Coverage 2025/2026 letter (Page 1).

8. Diagrams
(Insert screenshots when ready)--- TO BE UPDATED

bash```
System Architecture Diagram
ERD
Sequence Diagrams (Login, Plan Assignment, Bid Submission)
Deployment Diagram (Docker + SoC VM)
```

9. Testing

Testing includes:

bash```
9.1 Authentication testing (JWT validation, invalid login)
9.2 Employee coverage retrieval tests
9.3 Plan assignment logic (Designation → Plan → Coverage)
9.4 FWMI compliance tests
9.5 Bid submission & validation tests
9.6 MySQL integration tests
```
Screenshots of testing logs and Postman results should be added here later.

10. Non-Functional Requirements (NFRs)

bash```
10.1 All API responses must return within 2 seconds.
10.2 JWT must secure all protected endpoints.
10.3 Coverage data must match AIA coverage values exactly.
10.4 The system must be runnable fully on SoC VM using Docker.
10.5 Data must be stored using correct numeric types (no float rounding issues).
```

11. Deployment Instructions
    
11.1 To deploy on SoC VM:

bash```
git pull
docker-compose down
docker-compose up -d
```
11.2 Backend available at:

bash```
http://<vm-hostname>:8000
```

11.3 API Documentation:

bash```
http://<vm-hostname>:8000/docs
```

12. References

- AIA Group Insurance Coverage Letter (29 Sept 2025) — Plan benefits & coverage values
- FastAPI Documentation
- SQLModel Documentation
- Docker & Docker Compose Documentation
- BIT TCX3901 Module Guide
