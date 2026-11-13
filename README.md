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
├── README.md                          # Project documentation and summary
├── TEST_PLAN.md                       # Comprehensive IEEE 829 Test Plan
├── TEST_CASES.md                      # Detailed test cases (Auth, Catalog, Cart, Checkout, Payment)
├── BUG_REPORTS.md                     # Defect reports with severity/priority classification
└── api_test_postman_collection.json   # Importable Postman REST API test collection
```

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
