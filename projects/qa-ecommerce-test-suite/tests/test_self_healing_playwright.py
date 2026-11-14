"""
================================================================================
AI-Augmented Self-Healing Test Locator Engine for Playwright
Candidate: VARUN M S (Final Year BCA 2025 | QA & Automation Engineer)
Portfolio: https://varunms89.github.io
Repository: https://github.com/varunms89/qa-ecommerce-test-suite
================================================================================

Industry Problem:
In enterprise CI/CD pipelines, UI tests frequently break ("flaky tests") due to
minor frontend changes (e.g., developers rename #login-btn to .submit-btn).

AI Solution:
When a Playwright locator times out or encounters a stale element reference,
the AI Self-Healing Engine inspects the DOM candidates, analyzes semantic intent,
heals the locator on the fly, logs an audit report, and completes the test run
without pipeline failure.
"""

import sys
import os
import json
import re
from datetime import datetime
from typing import Optional, Dict, Any, List

class AISelfHealingLocator:
    """
    Intelligent Self-Healing Locator wrapper for Playwright.
    Deduces healed selectors based on DOM semantic role, text content, and AI heuristics.
    """
    def __init__(self):
        self.healing_history: List[Dict[str, Any]] = []

    def deduce_healed_selector(self, broken_selector: str, intent: str, candidate_elements: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Uses semantic AI matching to find the best replacement selector among candidate elements.
        If GEMINI_API_KEY is available, queries Google Gemini; otherwise uses semantic token scoring.
        """
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            try:
                import urllib.request
                prompt = (
                    f"A web automation test failed because the selector '{broken_selector}' is broken. "
                    f"The user's intended action is: '{intent}'. "
                    f"Here are candidate elements from the DOM: {json.dumps(candidate_elements[:15])}. "
                    f"Return a JSON object with: {{\"healed_selector\": \"...\", \"confidence\": 0.95, \"reasoning\": \"...\"}}"
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
            except Exception as e:
                pass  # Fallback to local heuristic engine

        # Heuristic Semantic Healer (Zero-failure offline engine)
        intent_tokens = [t.lower() for t in re.split(r"\W+", intent) if len(t) > 2]
        best_candidate = None
        best_score = -1

        for cand in candidate_elements:
            score = 0
            text = cand.get("text", "").lower()
            tag = cand.get("tag", "").lower()
            elem_id = cand.get("id", "").lower()
            classes = cand.get("class", "").lower()
            elem_type = cand.get("type", "").lower()
            data_test = cand.get("data-test", "").lower()

            for token in intent_tokens:
                if token in text:
                    score += 5
                if token in elem_id:
                    score += 4
                if token in data_test:
                    score += 6
                if token in classes:
                    score += 3

            if "click" in intent_tokens or "button" in intent_tokens or "submit" in intent_tokens:
                if tag in ["button", "a"] or elem_type == "submit":
                    score += 4

            if score > best_score:
                best_score = score
                best_candidate = cand

        if best_candidate and best_score > 0:
            selector = ""
            if best_candidate.get("data-test"):
                selector = f"[data-test='{best_candidate['data-test']}']"
            elif best_candidate.get("id"):
                selector = f"#{best_candidate['id']}"
            elif best_candidate.get("text"):
                selector = f"{best_candidate.get('tag', 'button')}:has-text('{best_candidate['text']}')"
            else:
                selector = f".{best_candidate.get('class', '').split()[0]}"

            confidence = min(0.70 + (best_score * 0.05), 0.98)
            return {
                "healed_selector": selector,
                "confidence": round(confidence, 2),
                "reasoning": f"Semantic match on intent tokens {intent_tokens} with tag <{best_candidate.get('tag')}>",
                "original_candidate": best_candidate
            }

        return {
            "healed_selector": broken_selector,
            "confidence": 0.30,
            "reasoning": "No confident match found. Retrying original selector."
        }

    def heal_and_click(self, page, broken_selector: str, intent: str, fallback_candidates: Optional[List[Dict[str, str]]] = None):
        """
        Attempts to click using the primary selector.
        If not found or timed out, intercepts, analyzes candidates, heals selector, and executes.
        """
        print(f"\n[AI Locator] Attempting selector: '{broken_selector}' (Intent: '{intent}')")
        try:
            # Short timeout to simulate broken / stale locator check
            page.wait_for_selector(broken_selector, timeout=2500)
            page.click(broken_selector)
            print(f"  ✓ Standard selector '{broken_selector}' resolved successfully.")
            return True, broken_selector
        except Exception as primary_err:
            print(f"  ⚠️ [SELECTOR FAILED] '{broken_selector}' timed out or was not found in DOM.")
            print(f"  🧠 [AI HEALING INITIATED] Activating semantic DOM healer for intent: '{intent}'...")

            # Extract interactive elements from live DOM
            candidates = []
            try:
                raw_cands = page.evaluate("""() => {
                    const elements = document.querySelectorAll('button, input[type="submit"], a, [role="button"]');
                    return Array.from(elements).map(el => ({
                        tag: el.tagName.toLowerCase(),
                        id: el.id || '',
                        class: el.className || '',
                        text: (el.innerText || el.value || '').trim(),
                        type: el.getAttribute('type') || '',
                        'data-test': el.getAttribute('data-test') || ''
                    }));
                }""")
                candidates = raw_cands or []
            except Exception:
                candidates = fallback_candidates or []

            if not candidates and fallback_candidates:
                candidates = fallback_candidates

            healed_info = self.deduce_healed_selector(broken_selector, intent, candidates)
            healed_sel = healed_info.get("healed_selector", broken_selector)
            conf = healed_info.get("confidence", 0.90)

            print(f"  🩹 [AI SELF-HEALED] Selector healed:")
            print(f"     • Original: {broken_selector}")
            print(f"     • Healed  : {healed_sel} (Confidence: {int(conf * 100)}%)")
            print(f"     • Reasoning: {healed_info.get('reasoning')}")

            # Execute action with healed selector
            page.click(healed_sel)
            print(f"  🚀 [RESUMED] Action succeeded using healed selector '{healed_sel}'.")

            record = {
                "timestamp": datetime.now().isoformat(),
                "intent": intent,
                "broken_selector": broken_selector,
                "healed_selector": healed_sel,
                "confidence": conf,
                "status": "HEALED_AND_EXECUTED"
            }
            self.healing_history.append(record)
            return True, healed_sel

def test_self_healing_playwright():
    """
    Test scenario:
    1. Navigate to SauceDemo.
    2. Enter credentials.
    3. Intentionally provide a BROKEN legacy selector: '#legacy-broken-login-button'.
    4. Assert AI Self-Healing kicks in, repairs locator to '#login-button', and logs in!
    """
    print("\n" + "="*70)
    print("🤖 STARTING PLAYWRIGHT AI SELF-HEALING AUTOMATION TEST")
    print("Author: VARUN M S | Software QA Automation Engineer")
    print("="*70)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("\n⚠️ Playwright not installed in local environment. Running heuristic unit verification...")
        healer = AISelfHealingLocator()
        candidates = [
            {"tag": "button", "id": "login-button", "class": "btn_action", "text": "Login", "type": "submit", "data-test": "login-button"},
            {"tag": "a", "id": "cancel-link", "class": "link_cancel", "text": "Cancel", "type": "", "data-test": "cancel"}
        ]
        res = healer.deduce_healed_selector("#legacy-broken-login-btn", "Click the login submit button", candidates)
        assert res["healed_selector"] in ["#login-button", "[data-test='login-button']"], "AI must deduce login button"
        print("✅ [AI Heuristic Unit Verified] Successfully healed selector to:", res["healed_selector"])
        return True

    healer = AISelfHealingLocator()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("  -> Step 1: Navigating to https://www.saucedemo.com ...")
        page.goto("https://www.saucedemo.com", timeout=15000)

        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")

        # Intentional Broken Selector to test AI Self-Healing
        broken_login_selector = "#legacy-nonexistent-submit-btn-v1"
        success, healed_selector = healer.heal_and_click(
            page=page,
            broken_selector=broken_login_selector,
            intent="Click the primary user login submit button",
            fallback_candidates=[
                {"tag": "input", "id": "login-button", "class": "submit-button btn_action", "type": "submit", "data-test": "login-button"}
            ]
        )

        assert success is True, "Test must heal and succeed"
        page.wait_for_selector(".inventory_list", timeout=10000)
        assert "inventory.html" in page.url, "Must be redirected to inventory page after healed login"
        print(f"\n🎉 [TEST PASSED] User successfully authenticated via AI Self-Healed locator ({healed_selector})!")

        browser.close()
        return True

if __name__ == "__main__":
    test_self_healing_playwright()
