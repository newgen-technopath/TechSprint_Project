import google.generativeai as genai
import json
import os

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY: genai.configure(api_key=API_KEY)

def test_dual_scenario():
    if not API_KEY: return "No API Key"
    
    # Test Data: User with ₹50k surplus
    income = 100000
    expenses = 30000
    emi = 20000
    surplus = income - (expenses + emi) # 50,000
    
    print(f"Testing with Surplus: ₹{surplus}")
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Act as a Financial Advisor.
    User Surplus: ₹{surplus}. Total Debt: ₹5,00,000.
    
    Generate JSON with TWO plans:
    1. "aggressive" (90% surplus to debt)
    2. "balanced" (50% surplus to debt, 50% to invest)
    
    Output JSON keys: "aggressive", "balanced".
    Inside each, include "allocation" object with "extra_debt" and "invest" amounts (integers).
    """
    
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        data = json.loads(response.text)
        
        print("\n=== AGGRESSIVE PLAN ===")
        print(f"Title: {data['aggressive'].get('title')}")
        print(f"Extra Debt Payoff: ₹{data['aggressive']['allocation']['extra_debt']}")
        
        print("\n=== BALANCED PLAN ===")
        print(f"Title: {data['balanced'].get('title')}")
        print(f"Extra Debt Payoff: ₹{data['balanced']['allocation']['extra_debt']}")
        print(f"Investment: ₹{data['balanced']['allocation']['invest']}")
        
        return "✅ Test Passed: Dual scenarios generated."
        
    except Exception as e:
        return f"❌ Test Failed: {e}"

if __name__ == "__main__":
    print(test_dual_scenario())