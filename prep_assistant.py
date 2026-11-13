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
