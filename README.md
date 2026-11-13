# E-Commerce Web & API Comprehensive Test Suite

[![Playwright E2E Tests](https://github.com/varunms89/qa-ecommerce-test-suite/actions/workflows/run-tests.yml/badge.svg)](https://github.com/varunms89/qa-ecommerce-test-suite/actions)
![Playwright](https://img.shields.io/badge/Playwright-E2E%20Automated-2ea44f?logo=playwright&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-API%20Test%20Suite-FF6C37?logo=postman&logoColor=white)
![Test Cases](https://img.shields.io/badge/Test%20Cases-50%2B%20Covered-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)

**Author:** VARUN M S (Final Year BCA 2025 | QA & Automation Engineer)  
**Portfolio:** [varunms89.github.io](https://varunms89.github.io)  
**Repository:** [github.com/varunms89/qa-ecommerce-test-suite](https://github.com/varunms89/qa-ecommerce-test-suite)  

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
├── Varun_MS_Ecommerce_API_Tests.postman_collection.json # Ready-to-import Postman REST API test collection
├── requirements.txt                                   # Python Playwright & pytest dependencies
└── tests/
    └── test_ecommerce_checkout.py                     # Python Playwright E2E UI automation test script
```

---

## 🤖 Python Playwright End-to-End Automation

An automated browser test suite implemented in **Python & Playwright** (`tests/test_ecommerce_checkout.py`) validating the entire customer purchase journey:

### Test Scenarios Automated:
1. **User Authentication:** Enters test credentials and verifies successful login.
2. **Catalog Integrity:** Validates all products loaded with prices and images.
3. **Add to Cart:** Selects item, clicks add-to-cart, and asserts cart badge increment.
4. **Checkout Form:** Enters shipping info and verifies field validations.
5. **Arithmetic Assertions:** Validates `Subtotal + Tax == Total Price` with floating-point precision.
6. **Order Placement:** Confirms final order dispatch and captures `checkout_verified.png`.

### How to Run:
```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Run via pytest
pytest tests/ -v

# Or run directly with Python
python tests/test_ecommerce_checkout.py
```

---

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

### How to Run in Postman or Newman:

#### Option A: 1-Click Import into Postman (Pre-configured with Live Cloud API)
1. Open Postman -> Click **Import** (top left).
2. Select or drag & drop `Varun_MS_Ecommerce_API_Tests.postman_collection.json`.
3. The collection is already pre-configured to hit the 24/7 live mock server at `https://job-auto-apply-bot.onrender.com`.
4. Click **Run Collection** -> Watch all status, latency, and schema assertions pass with green checkmarks!

#### Option B: Run Headless via Newman CLI
```bash
# Execute against the live cloud mock server:
npx newman run Varun_MS_Ecommerce_API_Tests.postman_collection.json --env-var base_url=https://job-auto-apply-bot.onrender.com
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
