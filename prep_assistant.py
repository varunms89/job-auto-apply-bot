"""
Preparation & Practice Assistant for Varun M S
Covers:
1. Software Testing / QA
2. Python & Programming
3. Artificial Intelligence & Machine Learning
"""

from typing import Dict, List, Any

PREP_MODULES = {
    "qa": {
        "title": "Software Testing & QA Master Guide",
        "badge": "Testing / QA",
        "description": "Essential manual testing principles, test case writing, bug life cycles, API verification, and automation basics.",
        "sections": [
            {
                "heading": "1. SDLC vs STLC Fundamentals",
                "content": """
<b>Software Development Life Cycle (SDLC)</b> covers the entire software creation process (Planning → Design → Coding → Testing → Deployment → Maintenance).<br>
<b>Software Testing Life Cycle (STLC)</b> focuses specifically on quality assurance phases:
<ol>
  <li><b>Requirement Analysis:</b> Identify testable requirements and identify gaps.</li>
  <li><b>Test Planning:</b> Estimate effort, define scope, test environment, and tools.</li>
  <li><b>Test Case Development:</b> Write detailed test scenarios, test cases, and test data.</li>
  <li><b>Environment Setup:</b> Configure test servers, databases, and network conditions.</li>
  <li><b>Test Execution:</b> Run test cases, log defects, and verify fixes.</li>
  <li><b>Test Closure:</b> Analyze bug metrics, test coverage, and sign-off report.</li>
</ol>
"""
            },
            {
                "heading": "2. Black-Box Test Design Techniques",
                "content": """
<ul>
  <li><b>Equivalence Partitioning (EP):</b> Divide input data into valid and invalid partitions. Test one value from each partition.<br>
      <i>Example:</i> Age input for 18–60 years. Valid partition: 25. Invalid partitions: 10, 75.</li>
  <li><b>Boundary Value Analysis (BVA):</b> Bugs frequently cluster at boundaries. Test Minimum, Minimum-1, Minimum+1, Maximum, Maximum-1, Maximum+1.<br>
      <i>Example:</i> For range 18 to 60, test: 17, 18, 19, 59, 60, 61.</li>
  <li><b>Decision Table Testing:</b> Ideal for complex business rules with multiple condition combinations (e.g., login credentials matching + 2FA token).</li>
</ul>
"""
            },
            {
                "heading": "3. How to Write a Professional Test Case",
                "content": """
Every industry test case should include:
<table style="width:100%; border-collapse:collapse; margin-top:8px;" border="1">
  <tr style="background:#f1f5f9;"><th>Field</th><th>Description</th><th>Example</th></tr>
  <tr><td><b>Test Case ID</b></td><td>Unique identifier</td><td>TC_AUTH_001</td></tr>
  <tr><td><b>Description</b></td><td>Objective of the test</td><td>Verify login with valid registered credentials</td></tr>
  <tr><td><b>Pre-conditions</b></td><td>System state before test</td><td>User account is active in database</td></tr>
  <tr><td><b>Steps to Execute</b></td><td>Numbered actions</td><td>1. Go to /login<br>2. Enter email & password<br>3. Click 'Sign In'</td></tr>
  <tr><td><b>Expected Result</b></td><td>What should happen</td><td>User redirected to dashboard with welcome banner</td></tr>
  <tr><td><b>Actual Result</b></td><td>What actually happened</td><td>User redirected to dashboard (PASS)</td></tr>
  <tr><td><b>Status</b></td><td>Pass / Fail / Blocked</td><td>PASS</td></tr>
</table>
"""
            },
            {
                "heading": "4. Defect / Bug Life Cycle & Severity vs Priority",
                "content": """
<b>Bug Life Cycle:</b> <code>NEW → ASSIGNED → OPEN → FIXED → PENDING RETEST → RE-TEST → CLOSED</code> (or <code>RE-OPENED</code>).<br><br>
<b>Severity vs Priority:</b>
<ul>
  <li><b>Severity:</b> Technical impact on system functionality (Critical, Major, Medium, Low).</li>
  <li><b>Priority:</b> Urgency of fixing from a business perspective (High, Medium, Low).</li>
  <li><i>High Severity, Low Priority:</i> App crashes when clicking an obsolete 10-year archive report that nobody visits.</li>
  <li><i>Low Severity, High Priority:</i> Company logo is misspelled on the public homepage. Functionality works, but business urgency is urgent.</li>
</ul>
"""
            },
            {
                "heading": "5. API Testing Essentials (Postman & REST)",
                "content": """
<ul>
  <li><b>HTTP Status Codes:</b>
    <ul>
      <li><code>200 OK</code>: Request succeeded.</li>
      <li><code>201 Created</code>: Resource created (e.g., POST user).</li>
      <li><code>400 Bad Request</code>: Malformed client payload.</li>
      <li><code>401 Unauthorized</code>: Missing or invalid authentication token.</li>
      <li><code>403 Forbidden</code>: Authenticated, but user lacks permission.</li>
      <li><code>404 Not Found</code>: Endpoint or resource does not exist.</li>
      <li><code>500 Internal Server Error</code>: Unhandled exception on server backend.</li>
    </ul>
  </li>
  <li><b>Key Verification Checkpoints:</b> Response Status Code, Response Body JSON Schema, Response Time (&lt; 500ms), and Header Content-Type.</li>
</ul>
"""
            }
        ]
    },
    "python": {
        "title": "Python & Coding Assessment Master Guide",
        "badge": "Python / Coding",
        "description": "Essential data structures, Big-O complexity, and top 10 solved coding assessment interview problems.",
        "sections": [
            {
                "heading": "1. Big-O Complexity & Core Structures",
                "content": """
<ul>
  <li><b>List / Array:</b> Lookup: <code>O(1)</code>, Append: <code>O(1)</code>, Insert/Delete at start: <code>O(n)</code>.</li>
  <li><b>Dictionary (Hash Map):</b> Lookup: <code>O(1)</code> avg, Insert: <code>O(1)</code> avg, Delete: <code>O(1)</code> avg.</li>
  <li><b>Set (Hash Set):</b> Lookup/Add/Remove: <code>O(1)</code> avg. Ideal for uniqueness and deduplication.</li>
  <li><b>Deque (from collections):</b> Fast append/pop from both left and right: <code>O(1)</code>.</li>
</ul>
"""
            },
            {
                "heading": "2. Top 10 Coding Assessment Questions (Solved in Python)",
                "content": """
<div style="background:#0f172a; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; margin-bottom:15px;">
# 1. Two Sum (Target Pair) - O(n) Time, O(n) Space
def two_sum(nums, target):
    seen = {} # val -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# 2. Valid Anagram - O(n) Time
from collections import Counter
def is_anagram(s, t):
    return Counter(s) == Counter(t)

# 3. Valid Parentheses (Stack) - O(n) Time
def is_valid_parentheses(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack

# 4. Binary Search - O(log n) Time
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# 5. Reverse String / Palindrome Check
def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]

# 6. Maximum Subarray Sum (Kadane's Algorithm) - O(n) Time
def max_sub_array(nums):
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
</div>
"""
            }
        ]
    },
    "ai": {
        "title": "Artificial Intelligence & ML Master Guide",
        "badge": "AI & Machine Learning",
        "description": "Core machine learning workflows, Pandas & NumPy data operations, Scikit-learn models, Generative AI & Prompt Engineering.",
        "sections": [
            {
                "heading": "1. Core Machine Learning Types & Concepts",
                "content": """
<ul>
  <li><b>Supervised Learning:</b> Labeled data (Input X → Output Y). Classification (predict category) and Regression (predict continuous numeric value).</li>
  <li><b>Unsupervised Learning:</b> Unlabeled data. Clustering (K-Means), Dimensionality Reduction (PCA), Anomaly Detection.</li>
  <li><b>Overfitting:</b> Model performs exceptionally on training data but poorly on test data (high variance). Fixes: Regularization (L1/L2), Dropout, Early Stopping, Cross-validation.</li>
  <li><b>Underfitting:</b> Model is too simple to capture underlying patterns (high bias). Fixes: More complex model, feature engineering.</li>
</ul>
"""
            },
            {
                "heading": "2. Essential Python Libraries: Pandas, NumPy, Scikit-learn",
                "content": """
<div style="background:#0f172a; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; margin-bottom:15px;">
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load and Clean Dataset
df = pd.DataFrame({
    'feature1': [10, 20, 15, 35, 40],
    'feature2': [1.2, 2.5, 1.8, 3.9, 4.1],
    'target': [0, 0, 0, 1, 1]
})
X = df[['feature1', 'feature2']]
y = df['target']

# 2. Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Model Training & Evaluation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train_scaled, y_train)
preds = model.predict(X_test_scaled)
print("Accuracy:", accuracy_score(y_test, preds))
</div>
"""
            },
            {
                "heading": "3. Generative AI & Prompt Engineering Essentials",
                "content": """
<ul>
  <li><b>Zero-Shot vs Few-Shot:</b> Zero-shot gives instructions with no examples; Few-shot provides 2–3 exemplar input-output pairs to steer formatting and reasoning.</li>
  <li><b>Chain-of-Thought (CoT):</b> "Think step-by-step before answering." Drastically increases math and logic reasoning accuracy in LLMs.</li>
  <li><b>Retrieval-Augmented Generation (RAG):</b>
    <ol>
      <li>Chunk document knowledge base.</li>
      <li>Compute vector embeddings (e.g., text-embedding-004).</li>
      <li>Store in Vector Database (Chroma, Pinecone, pgvector).</li>
      <li>Retrieve top-k relevant chunks based on cosine similarity of user query.</li>
      <li>Inject retrieved context into LLM prompt for factual, hallucination-free answers.</li>
    </ol>
  </li>
  <li><b>Hallucination Mitigation:</b> Strict system instructions ("Only answer using provided context; if unknown, state 'Not available'"), temperature set between 0.0 and 0.2 for deterministic QA.</li>
</ul>
"""
            }
        ]
    }
}

def get_prep_module(topic_key: str) -> Dict[str, Any]:
    return PREP_MODULES.get(topic_key.lower(), PREP_MODULES["qa"])

QA_PRACTICE_QUESTIONS = [
    {
        "id": 1,
        "question": "The company logo on the public login page is misspelled as 'Amezon' instead of 'Amazon'. How should this bug be categorized?",
        "options": [
            "High Severity, High Priority",
            "Low Severity, High Priority",
            "High Severity, Low Priority",
            "Low Severity, Low Priority"
        ],
        "answer": 1,
        "explanation": "Low Severity because the core application functionality (login) still works completely, but High Priority because the brand image is immediately visible to public users."
    },
    {
        "id": 2,
        "question": "An input field accepts user age between 18 and 60 years. Using 2-value Boundary Value Analysis (BVA), which boundary test cases should be tested?",
        "options": [
            "10, 25, 75",
            "18, 30, 60",
            "17, 18, 19, 59, 60, 61",
            "0, 18, 60, 100"
        ],
        "answer": 2,
        "explanation": "BVA focuses on values directly on and just around the borders: Min-1 (17), Min (18), Min+1 (19), Max-1 (59), Max (60), Max+1 (61)."
    },
    {
        "id": 3,
        "question": "In which phase of the Software Testing Life Cycle (STLC) are test cases, test data, and preconditions authored?",
        "options": [
            "Requirement Analysis",
            "Test Planning",
            "Test Case Development",
            "Test Execution"
        ],
        "answer": 2,
        "explanation": "Test Case Development is the STLC phase where QA engineers create, review, and rework detailed test cases and test data."
    },
    {
        "id": 4,
        "question": "A developer fixes a reported defect and marks it as FIXED. What is the immediate next state for the QA tester to execute?",
        "options": [
            "Close Defect",
            "Retest / Pending Retest",
            "Assign to Manager",
            "Deferred"
        ],
        "answer": 1,
        "explanation": "Once a defect is marked FIXED, it moves to 'Pending Retest' where QA verifies the fix in the test environment before closing it."
    },
    {
        "id": 5,
        "question": "When an API endpoint successfully creates a new user record via POST, which HTTP status code should the server return?",
        "options": [
            "200 OK",
            "201 Created",
            "204 No Content",
            "302 Redirect"
        ],
        "answer": 1,
        "explanation": "HTTP 201 Created indicates that the request has succeeded and a new resource has been created on the server."
    },
    {
        "id": 6,
        "question": "What is the key technical difference between HTTP status code 401 Unauthorized and 403 Forbidden?",
        "options": [
            "401 means server error; 403 means client error",
            "401 is for GET requests; 403 is for POST requests",
            "401 means authentication is missing/invalid; 403 means authenticated but user lacks authorization permission",
            "There is no difference; they are interchangeable"
        ],
        "answer": 2,
        "explanation": "401 means you are not logged in or your token is invalid. 403 means the server knows who you are, but you do not have permission to view that resource."
    },
    {
        "id": 7,
        "question": "What is the primary objective of Regression Testing?",
        "options": [
            "Test if the system handles extreme high user load",
            "Verify that recent code modifications or bug fixes have not broken existing functionality",
            "Ensure the UI looks pretty on mobile screens",
            "Check security against SQL injection attacks"
        ],
        "answer": 1,
        "explanation": "Regression testing ensures that new changes or bug fixes have not introduced side effects or broken previously working modules."
    },
    {
        "id": 8,
        "question": "A coupon discount applies only to cart purchases between ₹1,000 and ₹5,000. How many equivalence partitions should be identified?",
        "options": [
            "1 partition",
            "2 partitions",
            "3 partitions (Less than ₹1000, ₹1000-₹5000, Greater than ₹5000)",
            "5 partitions"
        ],
        "answer": 2,
        "explanation": "Equivalence partitioning requires: Invalid partition (<1000), Valid partition (1000-5000), and Invalid partition (>5000) = 3 total."
    },
    {
        "id": 9,
        "question": "Which software testing type evaluates internal code logic, branches, loops, and conditions without using the graphical user interface?",
        "options": [
            "Black-Box Testing",
            "White-Box Testing",
            "Usability Testing",
            "Beta Testing"
        ],
        "answer": 1,
        "explanation": "White-Box Testing (structural testing) examines internal program code, data structures, and conditional branches."
    },
    {
        "id": 10,
        "question": "What is the defining characteristic of Smoke Testing?",
        "options": [
            "Deep regression testing lasting several days",
            "Testing performed only after product launch",
            "Initial build verification testing on critical core workflows to confirm build stability",
            "Testing network connectivity under physical fire/heat conditions"
        ],
        "answer": 2,
        "explanation": "Smoke Testing (Build Verification Testing) quickly validates that the core basic functionality works before initiating comprehensive testing."
    }
]

HR_SCREENING_QUESTIONS = [
    {
        "question": "1. Tell me about yourself and your background.",
        "intent": "Recruiters want a concise, structured 60-second summary of your degree, technical focus, projects, and goals.",
        "script": "Hi, my name is Varun M S. I am currently in my final year of Bachelor of Computer Applications (BCA) at Government Science College, Hassan, graduating in May 2025. Throughout my academics, I have specialized in software quality assurance, test case authoring, boundary value analysis, API testing using Postman, and Python scripting. I have built practical projects including an e-commerce QA test suite with 50+ test cases and an AI resume screening tool published on my GitHub. I am passionate about finding defects early and delivering reliable software, and I am actively seeking an entry-level Software Tester / QA role or AI/Python internship where I can contribute to your sprint cycles."
    },
    {
        "question": "2. Why are you interested in Software Testing & QA?",
        "intent": "Shows whether you chose testing deliberately or just by chance.",
        "script": "I enjoy the analytical mindset required in QA. It's not just about finding what works, but actively thinking like an end-user to uncover where edge cases and workflows break before customers see them. Working with Postman for API validation, designing boundary test cases, and tracking bugs through their lifecycle gives me great satisfaction because QA directly protects the company's reputation and product reliability."
    },
    {
        "question": "3. What is your graduation year, college, and when can you join?",
        "intent": "Confirms graduation timeline and immediate availability for work/internship.",
        "script": "I am graduating in May 2025 from Government Science College (GSC), Hassan, Karnataka. My academic schedule allows for immediate joining for full-time or part-time internships (both Remote/WFH or Bangalore hybrid), and I will transition seamlessly to full-time employment post-graduation."
    },
    {
        "question": "4. What are your salary / stipend expectations?",
        "intent": "Assesses budget alignment without sounding inflexible.",
        "script": "As a fresher entering the industry, my primary priority is joining a strong engineering team where I can contribute hands-on testing, learn production best practices, and deliver immediate value. I am comfortable with standard industry stipend bands for interns (e.g., ₹15,000 to ₹35,000/month) or entry-level packages (3 to 5 LPA) and am happy to follow your company's established compensation structure."
    },
    {
        "question": "5. Do you have any questions for us?",
        "intent": "Demonstrates genuine curiosity, initiative, and engagement with the team.",
        "script": "Yes, thank you! I'd love to ask: 1) What does a typical day look like for a QA intern or junior tester on your team? 2) Which defect tracking and automation tools does your team use during sprint releases? 3) What are the key qualities of someone who exceeds expectations in this role over their first 90 days?"
    }
]

def generate_test_cases(feature: str) -> List[Dict[str, str]]:
    """
    Intelligently generates an IEEE-standard test case suite for any given feature or scenario.
    Specialized rules for Coupons, Payments, Auth/OTP, Search, and arbitrary features.
    """
    f = feature.strip().lower()

    if any(k in f for k in ["coupon", "discount", "promo", "voucher"]):
        return [
            {
                "id": "TC_CPN_001",
                "scenario": "Verify valid coupon code applies correct discount percentage",
                "type": "Positive / Functional",
                "preconditions": "Cart total meets minimum order criteria ($50)",
                "steps": "1. Navigate to checkout\n2. Enter valid code 'SAVE20'\n3. Click 'Apply Coupon'",
                "test_data": "Code: 'SAVE20' (20% off), Cart: $100",
                "expected": "Discount of $20 subtracted from subtotal; final price updates to $80; success message displayed",
                "severity": "High"
            },
            {
                "id": "TC_CPN_002",
                "scenario": "Boundary Value Analysis: Apply coupon on exact minimum order amount",
                "type": "Boundary Value (Min-1, Min, Min+1)",
                "preconditions": "Minimum spend coupon configured at $50",
                "steps": "1. Add items totaling $49.99 (Min-1) -> Click apply\n2. Add item to make $50.00 (Min) -> Click apply\n3. Add item to make $50.01 (Min+1) -> Click apply",
                "test_data": "Cart totals: $49.99, $50.00, $50.01",
                "expected": "$49.99 fails with 'Min $50 required'; $50.00 and $50.01 apply successfully",
                "severity": "High"
            },
            {
                "id": "TC_CPN_003",
                "scenario": "Negative: Apply expired coupon code",
                "type": "Negative / Business Logic",
                "preconditions": "Coupon expiration date has elapsed",
                "steps": "1. Enter expired code 'EXPIRED2024'\n2. Click 'Apply Coupon'",
                "test_data": "Code: 'EXPIRED2024'",
                "expected": "Validation error: 'This coupon code has expired'; cart total remains unchanged",
                "severity": "Medium"
            },
            {
                "id": "TC_CPN_004",
                "scenario": "Negative: Re-apply single-use coupon code by the same user account",
                "type": "Negative / Fraud Prevention",
                "preconditions": "Coupon is limited to 1 use per customer and already redeemed",
                "steps": "1. Enter redeemed coupon 'WELCOME10'\n2. Click 'Apply'",
                "test_data": "Code: 'WELCOME10'",
                "expected": "Error: 'Coupon code has already been redeemed for this account'",
                "severity": "High"
            },
            {
                "id": "TC_CPN_005",
                "scenario": "Security: SQL Injection and XSS payload in coupon input field",
                "type": "Security / Input Sanitization",
                "preconditions": "User is on coupon input box",
                "steps": "1. Enter \"' OR '1'='1\" and \"<script>alert('XSS')</script>\"\n2. Click 'Apply'",
                "test_data": "Payload: \"<script>alert(1)</script>\"",
                "expected": "Input sanitized safely; handled as invalid code error without script execution or database error",
                "severity": "Critical"
            },
            {
                "id": "TC_CPN_006",
                "scenario": "Concurrency: Rapid double-click on 'Apply Coupon' button",
                "type": "Concurrency / Edge Case",
                "preconditions": "Network latency simulated to 500ms",
                "steps": "1. Enter coupon 'FLAT100'\n2. Double-click apply button rapidly in <100ms",
                "test_data": "Code: 'FLAT100'",
                "expected": "Button disabled after first click; discount applied exactly once without duplicate deductions",
                "severity": "High"
            }
        ]

    elif any(k in f for k in ["upi", "payment", "gpay", "phonepe", "paytm", "checkout", "card", "razorpay"]):
        return [
            {
                "id": "TC_PAY_001",
                "scenario": "Verify successful UPI payment via Valid Virtual Payment Address (VPA)",
                "type": "Positive / Functional",
                "preconditions": "User has order in cart with valid shipping address",
                "steps": "1. Select UPI payment option\n2. Enter valid VPA (e.g. user@okhdfcbank)\n3. Click 'Pay Now'\n4. Approve prompt on mobile banking app",
                "test_data": "VPA: 'tester@okaxis', Amount: $49.00",
                "expected": "Payment gateway confirms transaction; webhook triggers order status 'CONFIRMED'; SMS/Email sent",
                "severity": "Critical"
            },
            {
                "id": "TC_PAY_002",
                "scenario": "Negative: Invalid UPI ID format validation",
                "type": "Negative / Input Validation",
                "preconditions": "User is on UPI checkout step",
                "steps": "1. Enter VPA without handle (e.g. 'invalidvpa')\n2. Click 'Verify & Pay'",
                "test_data": "Input: 'invalidvpa', 'test@', '@bank'",
                "expected": "Inline validation error: 'Please enter a valid UPI ID (e.g. name@bank)'",
                "severity": "High"
            },
            {
                "id": "TC_PAY_003",
                "scenario": "Edge Case: Payment timeout / User drops before entering MPIN",
                "type": "Edge Case / Timeout Handling",
                "preconditions": "Payment request initiated with 5-minute timeout window",
                "steps": "1. Request sent to UPI app\n2. User does not respond for 5 minutes",
                "test_data": "Timeout: 300 seconds",
                "expected": "App gracefully displays 'Transaction Timed Out'; order reverts to 'PENDING_PAYMENT'; stock not deducted permanently",
                "severity": "High"
            },
            {
                "id": "TC_PAY_004",
                "scenario": "Negative: Bank server downtime or insufficient funds response",
                "type": "Negative / External Gateway Failure",
                "preconditions": "Mock payment gateway returns error code 402 / Insufficient Funds",
                "steps": "1. Trigger payment with mock declined card/UPI\n2. Observe response handling",
                "test_data": "Declined Code: 'ERR_INSUFFICIENT_FUNDS'",
                "expected": "Clear user message: 'Payment declined by bank due to insufficient funds. Please try another method.'",
                "severity": "High"
            },
            {
                "id": "TC_PAY_005",
                "scenario": "Security: Replay attack prevention on payment callback webhook",
                "type": "Security / Transaction Integrity",
                "preconditions": "Payment callback received from gateway",
                "steps": "1. Re-send identical payment callback payload with same transaction ID",
                "test_data": "TxnId: 'TXN_99882233'",
                "expected": "Idempotency check detects duplicate callback; returns 200 OK without crediting double orders",
                "severity": "Critical"
            }
        ]

    elif any(k in f for k in ["login", "otp", "auth", "signin", "signup", "password"]):
        return [
            {
                "id": "TC_AUTH_001",
                "scenario": "Verify valid 6-digit OTP login within expiry window",
                "type": "Positive / Functional",
                "preconditions": "Mobile number is registered in user database",
                "steps": "1. Enter valid 10-digit phone number\n2. Click 'Request OTP'\n3. Enter valid 6-digit OTP received\n4. Click 'Verify'",
                "test_data": "Phone: '9876543210', OTP: '123456'",
                "expected": "JWT token issued; user redirected to dashboard; session created",
                "severity": "Critical"
            },
            {
                "id": "TC_AUTH_002",
                "scenario": "Negative: Enter incorrect 6-digit OTP",
                "type": "Negative / Boundary",
                "preconditions": "OTP has been generated",
                "steps": "1. Enter wrong OTP '000000'\n2. Click 'Verify'",
                "test_data": "OTP: '000000'",
                "expected": "Error message: 'Invalid OTP. 2 attempts remaining'; user remains on verification screen",
                "severity": "High"
            },
            {
                "id": "TC_AUTH_003",
                "scenario": "Security & Rate Limiting: Exceed maximum OTP retry attempts (3 max)",
                "type": "Security / Brute Force Prevention",
                "preconditions": "OTP attempt counter initialized to 0",
                "steps": "1. Enter incorrect OTP 3 consecutive times",
                "test_data": "3 wrong attempts",
                "expected": "Account temporarily locked for 15 minutes; message: 'Too many failed attempts. Try again in 15 minutes.'",
                "severity": "Critical"
            },
            {
                "id": "TC_AUTH_004",
                "scenario": "Edge Case: OTP input after expiry (60 seconds limit)",
                "type": "Edge Case / Expiration",
                "preconditions": "OTP timer elapsed > 60 seconds",
                "steps": "1. Wait 61 seconds\n2. Enter original OTP\n3. Click 'Verify'",
                "test_data": "Time: 65s",
                "expected": "Error: 'OTP has expired. Please click Resend OTP'; 'Resend OTP' button enabled",
                "severity": "Medium"
            },
            {
                "id": "TC_AUTH_005",
                "scenario": "Boundary Value Analysis: Mobile number length validation",
                "type": "Boundary Value (9, 10, 11 digits)",
                "preconditions": "On registration phone number field",
                "steps": "1. Enter 9 digits -> check error\n2. Enter 10 digits -> check valid\n3. Enter 11 digits -> check blocked",
                "test_data": "987654321 (9), 9876543210 (10), 98765432101 (11)",
                "expected": "Field prevents input beyond 10 digits and validates standard country regex",
                "severity": "High"
            }
        ]

    # Default Generic Generator for Any Arbitrary Feature (e.g. Flight booking, Cart, Search, Profile)
    cap_feature = feature.title()
    return [
        {
            "id": "TC_GEN_001",
            "scenario": f"Verify standard positive execution of {cap_feature} with valid data",
            "type": "Positive / Functional",
            "preconditions": "User is authenticated and system services are operational",
            "steps": f"1. Navigate to {cap_feature} interface\n2. Enter valid test parameters\n3. Click submit / confirm",
            "test_data": "Valid standard inputs",
            "expected": f"{cap_feature} successfully processed; database state updated; confirmation displayed",
            "severity": "Critical"
        },
        {
            "id": "TC_GEN_002",
            "scenario": f"Boundary Value Analysis: Minimum and Maximum allowed limits for {cap_feature}",
            "type": "Boundary Value Analysis",
            "preconditions": "Field has documented min and max constraints",
            "steps": "1. Test Lower Boundary (Min-1, Min, Min+1)\n2. Test Upper Boundary (Max-1, Max, Max+1)",
            "test_data": "Boundary threshold values",
            "expected": "Values within [Min, Max] succeed; boundary violations reject gracefully with validation errors",
            "severity": "High"
        },
        {
            "id": "TC_GEN_003",
            "scenario": f"Negative: Empty required fields and whitespace injection in {cap_feature}",
            "type": "Negative / Validation",
            "preconditions": "User is on input form",
            "steps": "1. Leave mandatory inputs blank\n2. Enter space characters only\n3. Click submit",
            "test_data": "Empty string \"\", whitespace \"   \"",
            "expected": "Form submission blocked; fields highlighted in red with 'This field is required'",
            "severity": "Medium"
        },
        {
            "id": "TC_GEN_004",
            "scenario": f"Security: Cross-Site Scripting (XSS) and SQL Injection resilience in {cap_feature}",
            "type": "Security / Vulnerability",
            "preconditions": "Input fields accept user string values",
            "steps": "1. Enter <script>alert('XSS')</script> and ' OR '1'='1\n2. Submit and observe output",
            "test_data": "Payload: \"<svg onload=alert(1)>\"",
            "expected": "Input is sanitized / HTML encoded; executed safely without executing arbitrary JavaScript",
            "severity": "Critical"
        },
        {
            "id": "TC_GEN_005",
            "scenario": f"Performance & Network Degradation: {cap_feature} under Slow 3G / offline interruption",
            "type": "Network & Resilience",
            "preconditions": "Chrome DevTools Network throttled to 'Slow 3G'",
            "steps": f"1. Trigger {cap_feature}\n2. Disconnect network mid-flight\n3. Reconnect network",
            "test_data": "Throttle: Slow 3G (100ms latency, 400kbps)",
            "expected": "Loading spinner shown; network timeout triggers friendly 'Network unstable' retry banner without crash",
            "severity": "High"
        },
        {
            "id": "TC_GEN_006",
            "scenario": f"Responsive UI: {cap_feature} renders correctly on Mobile (375px) vs Desktop (1440px)",
            "type": "UI / Cross-Device UX",
            "preconditions": "Browser viewport adjusted across standard breakpoints",
            "steps": f"1. View on 375x812 (iPhone)\n2. View on 768x1024 (Tablet)\n3. View on 1440x900 (Desktop)",
            "test_data": "Viewports: 375px, 768px, 1440px",
            "expected": "Zero horizontal scroll; tap targets minimum 48x48px; all buttons fully visible and clickable",
            "severity": "Medium"
        }
    ]

# ==============================================================================
# AI FEATURE 2: ROOT CAUSE ANALYZER (RCA) & AUTOMATED JIRA DEFECT DRAFTER
# ==============================================================================
def analyze_error_and_draft_jira(error_log: str) -> Dict[str, Any]:
    """
    AI-Augmented Root Cause Analysis & JIRA Defect Ticket Generator.
    Analyzes raw stack traces, test assertion failures, and API status codes.
    """
    clean_log = (error_log or "").strip()
    log_lower = clean_log.lower()

    # Check for Gemini API Key if available
    import os
    import json
    import re
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and len(clean_log) > 10:
        try:
            import urllib.request
            prompt = (
                "You are a Senior SDET / QA Lead. Analyze this automated test / application error log:\n\n"
                f"```\n{clean_log[:1500]}\n```\n\n"
                "Return a JSON object with this exact structure:\n"
                "{\n"
                '  "error_category": "...",\n'
                '  "rca_summary": "1-2 sentence plain English root cause",\n'
                '  "rca_details": "Detailed technical explanation",\n'
                '  "jira_ticket": {\n'
                '    "key": "DEFECT-2026-QA",\n'
                '    "title": "Concise defect title",\n'
                '    "severity": "Blocker | Critical | Major | Medium",\n'
                '    "environment": "Staging / Automated Regression Suite",\n'
                '    "steps_to_reproduce": ["Step 1", "Step 2", "Step 3"],\n'
                '    "expected_result": "...",\n'
                '    "actual_result": "...",\n'
                '    "reporter": "Varun M S (QA Automation Engineer)"\n'
                "  },\n"
                '  "suggested_code_fix": "Code snippet or patch recommendations"\n'
                "}"
            )
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            req = urllib.request.Request(
                url,
                data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                text_out = res_data["candidates"][0]["content"]["parts"][0]["text"]
                cleaned = re.search(r"\{.*\}", text_out, re.DOTALL)
                if cleaned:
                    return json.loads(cleaned.group(0))
        except Exception:
            pass

    # Heuristic Semantic Engine (Zero-failure offline engine)
    category = "General Runtime / Test Execution Error"
    severity = "Major"
    title = "Automated Test Failure: Unexpected Exception in Execution"
    rca_summary = "An unexpected exception halted the automated test run. Review the error details below."
    rca_details = "The runtime system caught an unhandled exception during step execution."
    steps = [
        "1. Launch automated test runner against target environment",
        "2. Execute test workflow leading up to failure point",
        "3. Observe exception thrown in test console / network log"
    ]
    expected = "Operation executes within SLA thresholds and returns valid response"
    actual = clean_log[:150] or "Execution threw an unhandled error"
    suggested_fix = "# Add defensive validation check:\nif response and response.status_code == 200:\n    process_payload(response.json())\nelse:\n    logger.error('Invalid response received')"

    if any(k in log_lower for k in ["timeout", "timeouterror", "waiting for selector", "stale element", "locator"]):
        category = "UI Automation Locator / Latency Failure"
        severity = "Major"
        title = "UI Test Flakiness: Element locator timed out before becoming actionable"
        rca_summary = "The automation locator timed out or was not found before becoming actionable in the DOM."
        rca_details = "A Playwright/Selenium locator exceeded its timeout limit. This typically occurs when client-side JavaScript renders asynchronously, or when frontend developers modify DOM attributes (id, class, test-id)."
        steps = [
            "1. Navigate to target application URL",
            "2. Trigger preceding action (e.g., click login / navigate catalog)",
            "3. Attempt to interact with target selector within timeout threshold"
        ]
        expected = "Target element renders and enters clickable/actionable state within 5000ms"
        actual = "Locator timed out with TimeoutError waiting for element state"
        suggested_fix = "# 1. Use explicit auto-waiting assertions:\npage.locator(selector).wait_for(state='visible', timeout=10000)\n# 2. Or implement AI Self-Healing locator fallback"

    elif any(k in log_lower for k in ["500", "502", "503", "504", "internal server error", "bad gateway"]):
        category = "Backend Server / HTTP 5xx Gateway Failure"
        severity = "Blocker"
        title = "API Failure: Server returned 500 Internal Server Error during transaction"
        rca_summary = "The backend service crashed while processing the request due to an unhandled server-side exception or database timeout."
        rca_details = "An HTTP 5xx status indicates an unhandled server error. Common causes include unhandled database deadlocks, null pointer dereferences in controllers, or downstream microservice timeouts."
        steps = [
            "1. Send HTTP request with payload to target REST endpoint",
            "2. Observe HTTP response status code and headers",
            "3. Inspect server-side error response payload"
        ]
        expected = "API returns HTTP 200 OK / 201 Created with valid JSON schema"
        actual = "Server responded with HTTP 500 Internal Server Error"
        suggested_fix = "# Wrap controller endpoint in try/except block with structured JSON error:\ntry:\n    result = service.process_transaction(payload)\n    return jsonify(result), 200\nexcept DatabaseException as db_err:\n    logger.critical(f'DB Deadlock: {db_err}')\n    return jsonify({'error': 'Service temporarily degraded'}), 503"

    elif any(k in log_lower for k in ["401", "403", "unauthorized", "forbidden", "token expired", "jwt"]):
        category = "Security & Authentication Failure"
        severity = "Critical"
        title = "Security Assertion: Authentication token rejected with 401 Unauthorized"
        rca_summary = "The request failed authentication due to a missing, malformed, or expired Bearer JWT token."
        rca_details = "The authentication middleware intercepted the request and rejected credentials. Verify whether the token expired, header casing is correct ('Authorization: Bearer <token>'), or test user permissions were revoked."
        steps = [
            "1. Authenticate test user via POST /api/v1/auth/login",
            "2. Extract returned auth_token",
            "3. Send authenticated request with Authorization header"
        ]
        expected = "Valid JWT token grants access to protected resources"
        actual = "API rejected request with 401 Unauthorized / Token Expired"
        suggested_fix = "# Ensure token refresh logic handles expiration gracefully:\nif response.status_code == 401:\n    refreshed_token = auth_client.refresh_session()\n    headers['Authorization'] = f'Bearer {refreshed_token}'\n    return retry_request(headers=headers)"

    elif any(k in log_lower for k in ["assertionerror", "assert", "expected", "to equal", "mismatch"]):
        category = "Functional Test Assertion Mismatch"
        severity = "Major"
        title = "Regression Defect: Value assertion mismatch against business specification"
        rca_summary = "An assertion verified that the actual application output deviated from documented business requirements."
        rca_details = "The automated assertion evaluated expected vs actual states (e.g. math calculation, status string, or count) and detected an inconsistency indicative of a regression bug."
        steps = [
            "1. Initialize test dataset with predefined boundary values",
            "2. Trigger business logic workflow",
            "3. Assert expected state against actual returned value"
        ]
        expected = "Actual value strictly matches the expected acceptance criteria"
        actual = clean_log[:150]
        suggested_fix = "# Verify arithmetic rounding & floating-point precision:\nimport math\nassert math.isclose(actual_total, expected_total, rel_tol=1e-2), f'Total mismatch: {actual_total} vs {expected_total}'"

    elif any(k in log_lower for k in ["nullpointer", "cannot read property", "typeerror", "attributeerror", "keyerror"]):
        category = "Null Reference / Schema Parsing Defect"
        severity = "Major"
        title = "Schema Defect: Unhandled TypeError / Missing Key in response payload"
        rca_summary = "The application attempted to access an object property or dictionary key that was undefined or null."
        rca_details = "A data parsing routine attempted property access on a null/undefined reference, indicating an unexpected change in API response structure or missing optional field handling."
        steps = [
            "1. Parse API response payload into JSON object",
            "2. Access nested attribute without defensive presence verification",
            "3. Observe runtime exception thrown"
        ]
        expected = "API payload adheres to schema contract with all required attributes populated"
        actual = "Runtime threw TypeError / KeyError accessing undefined property"
        suggested_fix = "# Use defensive dictionary / optional chaining:\nvalue = data.get('nested_property', {}).get('target_field', default_value)"

    return {
        "error_category": category,
        "rca_summary": rca_summary,
        "rca_details": rca_details,
        "jira_ticket": {
            "key": "DEFECT-2026-QA",
            "title": title,
            "severity": severity,
            "environment": "Staging / Automated Regression Suite",
            "steps_to_reproduce": steps,
            "expected_result": expected,
            "actual_result": actual,
            "reporter": "Varun M S (QA Automation Engineer)"
        },
        "suggested_code_fix": suggested_fix
    }

# ==============================================================================
# AI FEATURE 3: ADAPTIVE MOCK INTERVIEW EVALUATOR (LLM SCORING)
# ==============================================================================
def evaluate_interview_answer_ai(question_id: int, user_answer: str) -> Dict[str, Any]:
    """
    Evaluates candidate's technical interview answer using LLM / semantic heuristics.
    Returns score (0-10), keyword analysis, and senior SDET model answer.
    """
    clean_ans = (user_answer or "").strip()
    ans_lower = clean_ans.lower()

    # Find base question
    from telegram_listener import INTERVIEW_QUESTIONS
    q_data = next((q for q in INTERVIEW_QUESTIONS if q.get("id") == question_id), INTERVIEW_QUESTIONS[0])

    keywords = q_data.get("keywords", [])
    model_answer = q_data.get("model_answer", "")
    tip = q_data.get("tip", "")

    # Check for Gemini API Key
    import os
    import json
    import re
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and len(clean_ans) > 10:
        try:
            import urllib.request
            prompt = (
                f"You are a Senior QA Manager conducting a technical interview. Evaluate this candidate response.\n"
                f"Question: {q_data['question']}\n"
                f"Model Answer: {model_answer}\n"
                f"Candidate's Answer: {clean_ans}\n\n"
                "Return a JSON object with this exact structure:\n"
                "{\n"
                '  "score": 8.5,\n'
                '  "matched_keywords": ["keyword1", "keyword2"],\n'
                '  "missing_keywords": ["keyword3"],\n'
                '  "feedback": "2-3 sentences evaluating technical depth and actionable improvement",\n'
                '  "model_answer": "..."\n'
                "}"
            )
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            req = urllib.request.Request(
                url,
                data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                text_out = res_data["candidates"][0]["content"]["parts"][0]["text"]
                cleaned = re.search(r"\{.*\}", text_out, re.DOTALL)
                if cleaned:
                    return json.loads(cleaned.group(0))
        except Exception:
            pass

    # Heuristic Semantic Evaluation
    hits = [kw for kw in keywords if kw.lower() in ans_lower]
    missed = [kw for kw in keywords if kw.lower() not in ans_lower]

    num_hits = len(hits)
    # Scale: 1 hit = 5.3, 3 hits = 6.9, 5 hits = 8.5, 7+ hits = 9.5
    base_score = 4.0 + min(num_hits * 0.8, 4.5)
    length_bonus = 1.0 if len(clean_ans.split()) >= 20 else (0.5 if len(clean_ans.split()) >= 10 else 0.0)
    score = min(round(base_score + length_bonus, 1), 10.0)

    if score >= 8.5:
        feedback = "Outstanding response! You demonstrated strong technical terminology, systematic debugging discipline, and clear understanding of the QA lifecycle."
    elif score >= 6.5:
        feedback = f"Solid answer. Good mention of core concepts, but ensure you also highlight: {', '.join(missed[:3])} to impress senior technical interviewers."
    else:
        feedback = f"Decent start. To elevate this answer to Senior SDET standards, incorporate: {', '.join(missed[:4])}."

    return {
        "score": score,
        "matched_keywords": hits,
        "missing_keywords": missed[:5],
        "feedback": feedback,
        "model_answer": model_answer,
        "tip": tip
    }

# ==============================================================================
# AI FEATURE 4: GHERKIN BDD FEATURE & PYTEST-BDD STEP GENERATOR
# ==============================================================================
def generate_bdd_feature(user_story_or_feature: str) -> Dict[str, Any]:
    """
    Converts a plain English feature requirement into:
    1. Pristine Gherkin .feature file (Feature, Scenario Outline, Given, When, Then, Examples).
    2. Matching Python pytest-bdd step definitions ready for automation.
    """
    clean_story = (user_story_or_feature or "E-Commerce Discount Coupon Checkout").strip()
    story_lower = clean_story.lower()

    # Deducing domain
    feature_name = clean_story.title()
    if "coupon" in story_lower or "discount" in story_lower:
        feature_name = "Discount Coupon Application and Validation"
        gherkin = f"""Feature: {feature_name}
  As an online shopper
  I want to apply discount coupon codes during checkout
  So that I can receive promotional savings on my purchase

  Scenario Outline: Applying promotional coupons with boundary validation
    Given the user has added items totaling "<subtotal>" to the shopping cart
    When the user enters coupon code "<coupon_code>"
    And the user clicks the "Apply Coupon" button
    Then the system should display the message "<expected_message>"
    And the final order total should be calculated as "<final_total>"

    Examples:
      | subtotal | coupon_code | expected_message         | final_total |
      | 1000.00  | SAVE10      | Coupon applied! 10% off  | 900.00      |
      | 2500.00  | FLAT500     | Coupon applied! ₹500 off | 2000.00     |
      | 500.00   | EXPIRED20   | Error: Coupon expired    | 500.00      |
      | 1500.00  | INVALID     | Error: Invalid coupon    | 1500.00     |
"""
        pytest_steps = """import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('coupon_checkout.feature')

@given(parsers.parse('the user has added items totaling "{subtotal}" to the shopping cart'))
def setup_cart(page, subtotal):
    page.goto('/cart')
    page.evaluate(f"window.setCartTotal({subtotal})")

@when(parsers.parse('the user enters coupon code "{coupon_code}"'))
def enter_coupon(page, coupon_code):
    page.fill('#coupon-input', coupon_code)

@when('the user clicks the "Apply Coupon" button')
def click_apply(page):
    page.click('#apply-coupon-btn')

@then(parsers.parse('the system should display the message "{expected_message}"'))
def verify_message(page, expected_message):
    banner = page.locator('.coupon-alert-banner')
    assert expected_message in banner.inner_text()

@then(parsers.parse('the final order total should be calculated as "{final_total}"'))
def verify_total(page, final_total):
    total_text = page.locator('#order-total').inner_text()
    assert final_total in total_text
"""
    elif "payment" in story_lower or "upi" in story_lower or "checkout" in story_lower:
        feature_name = "Secure Online Payment and UPI Checkout"
        gherkin = f"""Feature: {feature_name}
  As a registered customer
  I want to complete orders using UPI and Card payment methods
  So that my purchase is processed securely with instant confirmation

  Scenario Outline: Payment gateway status verification and idempotent processing
    Given the user is on the order checkout page with order amount "<amount>"
    When the user selects payment method "<method>"
    And submits payment details with "<credentials>"
    Then the transaction should result in status "<status>"
    And the user should see confirmation screen with order reference

    Examples:
      | amount  | method | credentials        | status    |
      | 1499.00 | UPI    | user@okaxis        | SUCCESS   |
      | 2999.00 | CARD   | 4111222233334444   | SUCCESS   |
      | 799.00  | UPI    | invalid_vpa_id     | FAILED    |
      | 5000.00 | NETBNK | timeout_bank_sim   | TIMEOUT   |
"""
        pytest_steps = """import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('payment_checkout.feature')

@given(parsers.parse('the user is on the order checkout page with order amount "{amount}"'))
def navigate_checkout(page, amount):
    page.goto(f'/checkout?amount={amount}')

@when(parsers.parse('the user selects payment method "{method}"'))
def select_method(page, method):
    page.click(f'input[value="{method}"]')

@when(parsers.parse('submits payment details with "{credentials}"'))
def submit_payment(page, credentials):
    page.fill('#payment-credential-input', credentials)
    page.click('#submit-payment-btn')

@then(parsers.parse('the transaction should result in status "{status}"'))
def verify_status(page, status):
    status_badge = page.locator('.payment-status-badge')
    assert status in status_badge.inner_text()
"""
    else:
        feature_name = f"{clean_story} Workflow Verification"
        gherkin = f"""Feature: {feature_name}
  As an authenticated user
  I want to interact with {clean_story}
  So that the feature delivers reliable performance conforming to IEEE standards

  Scenario: Positive end-to-end execution of {clean_story}
    Given the application is running in staging environment
    When the user triggers {clean_story} with valid parameters
    Then the system should return HTTP status 200 OK
    And the UI state should update within 500ms SLA
"""
        pytest_steps = f"""import pytest
from pytest_bdd import scenarios, given, when, then

scenarios('{clean_story.lower().replace(" ", "_")}.feature')

@given('the application is running in staging environment')
def verify_environment(client):
    res = client.get('/health')
    assert res.status_code == 200

@when('the user triggers {clean_story} with valid parameters')
def trigger_action(page):
    page.click('#trigger-{clean_story.lower().replace(" ", "-")}-btn')

@then('the system should return HTTP status 200 OK')
def verify_success(page):
    assert page.locator('.success-banner').is_visible()

@then('the UI state should update within 500ms SLA')
def verify_sla(page):
    assert page.evaluate("window.performance.timing.loadEventEnd - window.performance.timing.navigationStart < 500")
"""

    return {
        "feature_name": feature_name,
        "gherkin_file": gherkin,
        "pytest_steps": pytest_steps,
        "framework": "pytest-bdd + Playwright"
    }


