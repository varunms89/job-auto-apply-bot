# Detailed Manual & Functional Test Cases

**System Under Test (SUT):** E-Commerce Web Application (v2.4)  
**QA Tester:** VARUN M S  

---

## 1. Authentication & User Profile Module

| Test Case ID | Test Scenario | Preconditions | Test Steps | Test Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_AUTH_01** | Verify login with valid credentials | User is registered & active in DB | 1. Navigate to `/login`<br>2. Enter email & password<br>3. Click 'Sign In' | Email: `test@domain.com`<br>Pass: `ValidPass123!` | Successfully redirected to `/dashboard` with greeting message | Redirected to dashboard | **PASS** |
| **TC_AUTH_02** | Verify login with incorrect password | User is registered | 1. Navigate to `/login`<br>2. Enter correct email & wrong pass<br>3. Click 'Sign In' | Email: `test@domain.com`<br>Pass: `WrongPass999` | Displays error alert: *"Invalid email or password"*; password field cleared | Error displayed as expected | **PASS** |
| **TC_AUTH_03** | Verify password masking on login page | User on `/login` | 1. Enter password string<br>2. Click 'Show Password' eye icon | Pass: `Secret123` | Characters initially masked as dots, revealed on toggle | Functions correctly | **PASS** |
| **TC_AUTH_04** | Verify SQL Injection resilience in login | User on `/login` | 1. Enter SQL injection payload in email field<br>2. Enter arbitrary password<br>3. Submit | Payload: `' OR '1'='1` | Input validation rejects format; no unauthorized access or 500 error | 400 Bad Request returned | **PASS** |

---

## 2. Product Search & Catalog Filter Module

| Test Case ID | Test Scenario | Preconditions | Test Steps | Test Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_SEARCH_01** | Search by exact product name | Products exist in DB | 1. Click search bar<br>2. Type 'Wireless Headphones'<br>3. Press Enter | Query: `Wireless Headphones` | Returns matching product cards with price and thumbnail | Correct results displayed | **PASS** |
| **TC_SEARCH_02** | Search with special characters | Catalog loaded | 1. Type special characters in search box<br>2. Submit | Query: `<script>alert(1)</script>` | Handled cleanly; displays *"No products found"*; script not executed | XSS prevented | **PASS** |
| **TC_SEARCH_03** | Price filter Boundary Value Analysis | Catalog loaded | 1. Set Min price = 500, Max price = 1000<br>2. Apply filter | Range: ₹500 to ₹1000 | Only products priced between 500.00 and 1000.00 inclusive are shown | Products ₹499 shown erroneously | **FAIL (BUG-02)** |

---

## 3. Shopping Cart & Checkout Module

| Test Case ID | Test Scenario | Preconditions | Test Steps | Test Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_CART_01** | Add single item to cart | User is logged in | 1. Open product details page<br>2. Click 'Add to Cart' | Product ID: `P-101` | Cart badge counter increments by 1; subtotal updates | Counter incremented | **PASS** |
| **TC_CART_02** | Quantity Boundary Value Analysis | Item in cart | 1. Increase quantity to maximum allowable limit (99)<br>2. Attempt to increase to 100 | Qty: `99` -> `100` | System disables '+' button at 99 with message *"Max limit reached"* | Button disabled | **PASS** |
| **TC_CART_03** | Apply promo code discount | Cart has ₹2,000 items | 1. Enter valid promo code<br>2. Click 'Apply' | Promo: `SAVE10` (10% off) | Total updates from ₹2,000 to ₹1,800 (-₹200) | Calculated correctly | **PASS** |
| **TC_CHECK_01** | Order total calculation with GST/Tax | Cart has 2 items | 1. Proceed to checkout<br>2. Verify items total + 18% GST + shipping | Item 1: ₹500, Item 2: ₹500, Shipping: ₹50 | Subtotal: ₹1,000 + GST: ₹180 + Ship: ₹50 = ₹1,230 | Displays ₹1,230 | **PASS** |
