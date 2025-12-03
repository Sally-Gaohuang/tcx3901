from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import auth as auth_router
from api.database.database import init_db
from api.routers import employee, admin, insurer, bidding, coverage
from api.routers import test_auth



app = FastAPI(
    title="TCX3901 Insurance Checking Portal",
    version="1.0.0",
    description="Insurance coverage evaluation and bidding platform",
)

# -------------------------------
# CORS (allow frontend)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Database Initialization
# -------------------------------
@app.on_event("startup")
def on_startup():
    init_db()


# -------------------------------
# Router Registration
# -------------------------------
app.include_router(test_auth.router, prefix="/test-auth", tags=["Test Auth"])
app.include_router(employee.router, prefix="/employee", tags=["Employee"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(insurer.router, prefix="/insurer", tags=["Insurer"])
app.include_router(bidding.router, prefix="/bidding", tags=["Bidding"])
app.include_router(coverage.router, prefix="/coverage", tags=["Coverage"])
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])



# -------------------------------
# Root test endpoint
# -------------------------------
@app.get("/")
def root():
    return {"message": "Insurance Checking API Running"}
