from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


# ---------- USER ----------
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    role: str  # employee, admin, insurer

    employee: Optional["Employee"] = Relationship(back_populates="user")
    insurer_plans: List["Plan"] = Relationship(back_populates="insurer")
    bids: List["Bid"] = Relationship(back_populates="insurer")


# ---------- EMPLOYEE ----------
class Employee(SQLModel, table=True):
    employee_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    employee_code: str
    name: Optional[str] = None
    department: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    plan_id: Optional[int] = Field(default=None, foreign_key="plan.plan_id")

    user: Optional[User] = Relationship(back_populates="employee")
    plan: Optional["Plan"] = Relationship(back_populates="employees")


# ---------- POLICY CATEGORY ----------
class PolicyCategory(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, primary_key=True)
    category_name: str

    plan_tiers: List["PlanTier"] = Relationship(back_populates="category")
    bids: List["Bid"] = Relationship(back_populates="category")


# ---------- PLAN ----------
class Plan(SQLModel, table=True):
    plan_id: Optional[int] = Field(default=None, primary_key=True)
    plan_name: str
    insurer_id: Optional[int] = Field(default=None, foreign_key="user.user_id")

    insurer: Optional[User] = Relationship(back_populates="insurer_plans")
    plan_tiers: List["PlanTier"] = Relationship(back_populates="plan")
    employees: List[Employee] = Relationship(back_populates="plan")


# ---------- PLAN TIERS ----------
class PlanTier(SQLModel, table=True):
    tier_id: Optional[int] = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.plan_id")
    category_id: int = Field(foreign_key="policycategory.category_id")
    sum_insured: Optional[float] = None

    plan: Plan = Relationship(back_populates="plan_tiers")
    category: PolicyCategory = Relationship(back_populates="plan_tiers")


# ---------- BIDDING ROUND ----------
class BiddingRound(SQLModel, table=True):
    round_id: Optional[int] = Field(default=None, primary_key=True)
    round_name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    bids: List["Bid"] = Relationship(back_populates="round")


# ---------- BID ----------
class Bid(SQLModel, table=True):
    bid_id: Optional[int] = Field(default=None, primary_key=True)
    round_id: int = Field(foreign_key="biddinground.round_id")
    insurer_id: int = Field(foreign_key="user.user_id")
    category_id: int = Field(foreign_key="policycategory.category_id")
    premium: float

    round: BiddingRound = Relationship(back_populates="bids")
    insurer: User = Relationship(back_populates="bids")
    category: PolicyCategory = Relationship(back_populates="bids")
