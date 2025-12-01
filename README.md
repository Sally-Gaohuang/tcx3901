# TCX3901
TCX3901 Insurance Checking System
##1. Overview of Coverage Packages

According to the AIA Group Insurance Coverage letter (Page 1), the policyholder is covered under the following benefit categories:

###1.1 Group Life & TPD (GTL)

Plan 1: Assistant Managers & Above — $100,000

Plan 2: All Other Employees — $70,000

###1.2 Group Critical Illness (GCI)

Plan 1: Assistant Managers & Above — $40,000

Plan 2: All Other Employees — $28,000

###1.3 Group Accidental Death & Dismemberment (GPA)

Plan 1: Assistant Managers & Above — $150,000

Plan 2: All Other Employees (including SP & WP) — $100,000

###1.4 Group Hospitalisation & Surgical (GHS)

Plan 1: Assistant Managers & Above — 2-Bed Private

Plan 2: Engineers, Secretaries & Executives — 4-Bed Private

Plan 3: Assistant Engineers & Below — 4-Bed Government/Rest

###1.5 Group H&S – Foreign Worker (FWMI)

Applies only to S-Pass & Work Permit Holders

Up to $60,000 per policy year

Co-insurance 25% for claims over $15,000

###1.6 Group Supplementary Major Medical (GMM)

Plan 1: Assistant Managers & Above — Overall Max $100,000

Plan 2: Executives, Secretaries — Overall Max $65,000

Plan 3: Engineers & Below — Overall Max $40,000

###2. User Story Mapping to Packages

This section explains how each user interacts with the system and what benefits they see.

##2.1 Employee User Stories
E1 — View My Insurance Coverage

As an employee, I want to check my assigned insurance packages so that I always know what I am entitled to and can provide correct information to hospitals.

What the employee sees (auto-generated based on grade/category):

GTL (Life & TPD)
GCI (Critical Illness)
GPA (Accident) — staff only
GHS (Hospital & Surgical)
GMM (Major Medical)
FWMI (only for WP/S-Pass employees)

Example:

If user is Assistant Engineer (Plan 3)

GTL: $70,000  
GCI: $28,000  
GPA: $100,000  
GHS: 4-Bed Govt  
GMM: $40,000  
FWMI: — (Not a Work Permit holder)

###E2 — Check My Claim Documents

The system displays:

Hospitalisation claim requirements

Critical illness claim documents

Accident claim documents

FWMI claim steps (for WP/SP holders)

###E3 — FWMI Compliance (WP/S-Pass Only)

As a foreign worker, I want to see if my FWMI meets MOM requirements.

System shows:

FWMI Coverage: $60,000  
Required Minimum: $60,000  
Status: ✓ Compliant

##2.2 HR Admin User Stories
###A1 — Add/Edit Employee Records

The admin enters:

Name

Category (Staff vs WP/S Pass)

Designation

Project code

The system automatically assigns the correct plan number and coverage values based on the AIA document.
Example:

Assistant Manager → Plan 1

Engineers → Plan 2 / Plan 3

WP/S Pass → FWMI + Plan 3 equivalents

###A2 — Automatic Plan Assignment (Key System Logic)
Employee Type	Assigned Packages
Assistant Managers & Above	GTL 100K, GCI 40K, GPA 150K, GHS Plan 1, GMM 100K
Engineers / Secretaries / Executives	GTL 70K, GCI 28K, GPA 100K, GHS Plan 2, GMM 65K
Assistant Engineers & Below	GTL 70K, GCI 28K, GPA 100K, GHS Plan 3, GMM 40K
S-Pass & Work Permit	FWMI 60K + GHS (FW Plan), GMM (40K), GCI 28K, GTL 70K

(All values extracted from AIA coverage letter – Page 1)

###A3 — View Full Employee Coverage

Admin can see:

Plan type

Sum insured

Ward entitlement

Accident & CI limits

FWMI status (for WP/SP)

###A4 — Compare Insurer Quotations

The admin compares:

FWMI premiums

GHS premiums

GMM premiums

GPA / GTL / GCI rates

Total cost per insurer

###A5 — FWMI Compliance Dashboard

Admin receives alerts for:

Employee: [Name]
Coverage: FWMI $30,000
Required: $60,000
Status: ❌ Non-Compliant

###2.3 Insurer User Stories
I1 — Submit Bids

Insurer submits:

Policy	Premium
GTL	$XX
GCI	$XX
GHS	$XX
GMM	$XX
GPA	$XX
FWMI	$XX

System validates completeness.

###I2 — Edit Before Deadline

Round status = “Open” → allow editing
Round status = “Closed” → view only

###I3 — View Required Coverages

Insurer sees policy categories extracted from AIA document:

GTL
GCI
GPA
GHS
FWMI
GMM

(This ensures insurers quote for the correct benefits.)

3. System Mapping Summary (One-Glance Table)
Module	Who Uses It	Coverage Loaded From AIA Document
Employee Self-Check	Employees	GTL, GCI, GPA, GHS, GMM, FWMI
Admin Employee CRUD	HR Admin	All packages, plan assignment rules
Plan Assignment Engine	System	All Plans 1–4 mapping
Insurer Bidding	Insurers	Same categories as AIA policies
Comparison Dashboard	HR Admin	All premiums mapped to same categories

##User Story Statements (Final)
###Employee User Stories
bash```
As an employee, I want to view my full insurance coverage (GTL, GCI, GPA, GHS, GMM, FWMI) so that I know exactly what benefits I am entitled to.

As an employee, I want to access the list of required claim documents so that I can submit claims correctly without confusion.

As a Work Permit or S-Pass holder, I want to check whether my FWMI coverage meets MOM’s minimum requirement of $60,000 so that I feel secure about my medical protection.

As an employee, I want to verify my ward entitlement and sum insured before hospital admission so that I can inform the hospital accurately.```

###HR Admin User Stories
```
As an HR admin, I want to add, update, or deactivate employee records so that the insurance headcount remains accurate.

As an HR admin, I want the system to automatically assign the correct insurance plan based on employee designation and category so that coverage is consistent and error-free.

As an HR admin, I want to view an employee’s complete insurance coverage in a single page so that I can quickly verify correctness when enquiries arise.

As an HR admin, I want the system to detect FWMI non-compliance automatically so that I can address issues before MOM audits.

As an HR admin, I want to generate insurance coverage reports so that I can share data with management or insurers easily.

As an HR admin, I want to compare insurers’ quotations side-by-side so that I can choose the most cost-effective package for the company.

As an HR admin, I want each employee to have one active project code so that insurance costs can be allocated to the correct project.```

###Insurer User Stories
```
As an insurer, I want to view the required coverage categories (GTL, GCI, GPA, GHS, GMM, FWMI) so that I can prepare accurate quotations.

As an insurer, I want to submit premiums for each insurance category so that HR can evaluate my quotation during the bidding round.

As an insurer, I want to revise my submitted bid before the round closes so that I can correct any mistakes or improve my offer.

As an insurer, I want to review my previous bids so that I can maintain consistency in multi-round submissions.```
