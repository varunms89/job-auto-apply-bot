# E-Commerce Web & API Comprehensive Test Suite

**Author:** VARUN M S  
**Role:** QA / Software Tester  
**Repository:** [github.com/varunms89/qa-ecommerce-test-suite](https://github.com/varunms89)

---

## 📌 Project Overview
This repository contains an industry-standard Quality Assurance (QA) test documentation and automation testing suite for a modern web and mobile e-commerce platform. It demonstrates practical competency in:
- **Software Testing Life Cycle (STLC)** implementation
- **Black-Box Test Design** (Equivalence Partitioning, Boundary Value Analysis)
- **Manual Test Case Authoring** (Functional, Negative, Boundary, UI/UX)
- **Defect Lifecycle Management & Reporting**
- **API Testing** using Postman and REST status code assertions

---

## 📂 Repository Structure
```
├── README.md                                          # Project documentation and summary
├── TEST_PLAN.md                                       # Comprehensive IEEE 829 Test Plan
├── TEST_CASES.md                                      # Detailed test cases (Auth, Catalog, Cart, Checkout, Payment)
├── BUG_REPORTS.md                                     # Defect reports with severity/priority classification
└── Varun_MS_Ecommerce_API_Tests.postman_collection.json # Ready-to-import Postman REST API test collection
```

---

## 📮 Postman Automated API Test Collection

This suite includes an exportable, industry-standard Postman Collection format (v2.1.0) inside:
👉 `Varun_MS_Ecommerce_API_Tests.postman_collection.json`

### Automated Checks & Test Scripts Included:
1. **Authentication Tests (`POST /api/v1/auth/login`)**:
   - Status 200 OK verification.
   - Response latency SLA assertion (`< 500ms`).
   - JWT Auth Token extraction & automatic environment variable storage.
   - Negative boundary test: Invalid credentials return `401 Unauthorized` and descriptive error message.
2. **Product Catalog Validation (`GET /api/v1/products`)**:
   - Status 200 OK check and fast latency benchmark (`< 400ms`).
   - JSON array integrity and non-zero pagination count.
   - Price validation (`price > 0`).
3. **Order Placement & Cancellation Workflow (`POST & DELETE /api/v1/orders`)**:
   - Status `201 Created` assertion.
   - `order_id` generation verification.
   - Bearer token authorization header validation.
   - Clean order deletion / cancellation validation (`200 OK` / `204 No Content`).

### How to Run in Postman:
1. Open Postman -> Click **Import** (top left).
2. Drag and drop `Varun_MS_Ecommerce_API_Tests.postman_collection.json`.
3. Click **Run Collection** to execute all automated test assertions!

---

## 🧪 Test Coverage Summary
- **Total Test Cases Executed:** 52
- **Passed:** 46
- **Failed / Defects Logged:** 6
- **Defect Distribution:**
  - Critical / High: 2 (Checkout total rounding error, Payment gateway 500 error on timeout)
  - Medium: 3 (Search pagination offset bug, cart item count mismatch, invalid email regex bypass)
  - Low: 1 (Truncated discount badge on mobile viewport)

---

## 🛠️ Tools & Methodologies Used
- **Testing Types:** Manual Testing, Smoke Testing, Functional Testing, Regression Testing, API Testing.
- **Tools:** Postman, Chrome DevTools, GitHub, Markdown/Spreadsheet Test Trackers.
- **Techniques:** Boundary Value Analysis (BVA), Equivalence Class Partitioning (ECP), Error Guessing.
