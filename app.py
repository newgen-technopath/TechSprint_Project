from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import json
import os

app = Flask(__name__)

# --- 1. CONFIGURATION ---
API_KEY = os.getenv("GOOGLE_API_KEY") 

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("❌ WARNING: API Key not found! Please set GOOGLE_API_KEY environment variable.")

# --- 2. HELPER FUNCTIONS ---
def determine_eligibility(income, expenses, total_debt, monthly_emi, savings):
    try:
        income, expenses = int(income), int(expenses)
        total_debt, monthly_emi, savings = int(total_debt), int(monthly_emi), int(savings)
    except:
        return "Invalid Data"
    
    monthly_surplus = income - (expenses + monthly_emi)
    dti_ratio = (monthly_emi / income) if income > 0 else 0
    
    if monthly_surplus <= 0: return "Deficit"
    if dti_ratio > 0.40: return "High Debt Stress"
    return "Stable"

# --- 3. ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report.html')
def report_page():
    return render_template('report.html')

# --- API: GET PLAN (CORE LOGIC WITH ZERO DEBT HANDLING) ---
@app.route('/api/get-plan', methods=['POST'])
def get_plan():
    data = request.json
    
    # Extract Data
    income = data.get('income', 0)
    expenses = data.get('expenses', 0)
    total_debt = data.get('total_debt', 0)
    monthly_emi = data.get('monthly_emi', 0)
    savings = data.get('savings', 0)
    
    status = determine_eligibility(income, expenses, total_debt, monthly_emi, savings)
    
    if status == "Invalid Data":
        return jsonify({"error": "Invalid input"}), 400

    try:
        if not API_KEY: raise ValueError("No API Key")
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        monthly_surplus = income - (expenses + monthly_emi)
        
        # --- CONDITIONAL LOGIC: DEBT vs. NO DEBT ---
        if total_debt > 0:
            # CASE A: DEBT EXISTS (Original Logic)
            prompt = f"""
            Act as a Strategic Financial Advisor. 
            User Data: Income: ₹{income}, Surplus: ₹{monthly_surplus}, Debt: ₹{total_debt}, EMI: ₹{monthly_emi}.
            
            MISSION: Generate TWO distinct strategic plans to CLEAR DEBT.
            
            SCENARIO A: "AGGRESSIVE" (Monk Mode)
            - Strategy: 90% of surplus goes to EXTRA Debt Payoff. 10% to Savings.
            - Goal: Become debt-free as fast as possible.
            - Title: "🔥 Monk Mode (Aggressive)"
            - Desc: "Live lean, kill debt fast."
            
            SCENARIO B: "BALANCED" (Smart Growth)
            - Strategy: 50% surplus to Debt, 50% to Investments (SIPs/Liquid Funds).
            - Goal: Build assets while managing debt.
            - Title: "🌱 Smart Balance (Growth)"
            - Desc: "Invest while you pay."
            
            REQUIRED JSON STRUCTURE:
            {{
                "aggressive": {{
                    "title": "String", "desc": "String",
                    "allocation": {{ "extra_debt": <int>, "invest": <int> }},
                    "steps": ["Step 1", "Step 2", "Step 3", "Step 4"]
                }},
                "balanced": {{
                    "title": "String", "desc": "String",
                    "allocation": {{ "extra_debt": <int>, "invest": <int> }},
                    "steps": ["Step 1", "Step 2", "Step 3", "Step 4"]
                }}
            }}
            """
        else:
            # CASE B: ZERO DEBT (Wealth Creation Logic)
            prompt = f"""
            Act as a Wealth Manager. User Surplus: ₹{monthly_surplus}. User is DEBT FREE.
            
            MISSION: Generate TWO wealth accumulation plans.
            
            SCENARIO A: "AGGRESSIVE" (Wealth Accelerator)
            - Strategy: High-Risk, High-Reward (e.g., Small Cap, Crypto, Direct Equity).
            - Allocation: Set "extra_debt" to 0. Put 90% surplus into "invest".
            - Title: "🚀 Wealth Accelerator"
            - Desc: "Aggressive compounding. High volatility, max returns."
            
            SCENARIO B: "BALANCED" (Wealth Fortress)
            - Strategy: Stability & Safety (e.g., Large Cap, Gold, Debt Funds).
            - Allocation: Set "extra_debt" to 0. Put 60% surplus into "invest" (keep rest as liquid cash).
            - Title: "🛡️ Wealth Fortress"
            - Desc: "Steady growth with capital protection."
            
            REQUIRED JSON STRUCTURE:
            {{
                "aggressive": {{
                    "title": "String", "desc": "String",
                    "allocation": {{ "extra_debt": 0, "invest": <int> }},
                    "steps": ["Step 1 (High Growth)", "Step 2", "Step 3"]
                }},
                "balanced": {{
                    "title": "String", "desc": "String",
                    "allocation": {{ "extra_debt": 0, "invest": <int> }},
                    "steps": ["Step 1 (Balanced)", "Step 2", "Step 3"]
                }}
            }}
            """
        
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        parsed_data = json.loads(response.text)
        return jsonify(parsed_data)

    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"error": "AI generation failed"}), 500

# --- API: TRANSLATE (DOST MODE) ---
@app.route('/api/translate-plan', methods=['POST'])
def translate_plan():
    data = request.json
    plan_data = data.get('plan')
    target_lang = data.get('language', 'Hinglish') # Default to Hinglish
    
    if not plan_data or not API_KEY:
        return jsonify({"error": "Invalid data or missing API Key"}), 400

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Act as a friendly Indian financial guide ("Dost").
        Translate the following Financial Plan JSON into "{target_lang}".
        
        RULES:
        1. Keep the JSON structure EXACTLY the same (keys: title, desc, steps, allocation).
        2. Do NOT change the numbers (allocation amounts).
        3. Translate the 'title', 'desc', and 'steps' text.
        4. Tone: Encouraging, brotherly, use slight slang (e.g., "Paisa," "Jugad," " टेंशन mat lo").
        
        Input JSON:
        {json.dumps(plan_data)}
        """
        
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return jsonify(json.loads(response.text))

    except Exception as e:
        print(f"Translation Error: {e}")
        return jsonify({"error": "Translation failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)