Dost Financial 🚀
AI-Powered Financial Strategy Engine for the Indian Context

Dost Financial is a privacy-first, lightweight financial planning application designed to help users navigate debt and wealth creation. Unlike standard calculators, it uses Generative AI (Google Gemini 2.5) to build personalized "Dual-Scenario" roadmaps based on a user's unique financial profile.

🌟 Key Features
Cyberpunk Dashboard: A sleek, dark-mode UI ("Neon aesthetics") built with pure HTML/CSS/JS for zero-latency interactions.

Dual-Brain Engine: Generates two distinct financial paths simultaneously:

🔥 Monk Mode (Aggressive): Prioritizes rapid debt elimination (Snowball method).

🌱 Smart Growth (Balanced): Balances debt payoff with systematic investment planning (SIPs).

Zero-Debt Logic: Automatically detects debt-free users and switches strategy to Wealth Acceleration vs. Wealth Fortress.

🇮🇳 Dost Mode: A unique localization feature that translates financial jargon into encouraging "Hinglish" (Hindi + English) using AI, making finance feel like advice from a friend.

Privacy First: No database. No login required. All data exists only in the user's browser session.

Interactive Simulation: Real-time Chart.js visualizations that project wealth growth over 10 years based on the selected strategy.

PDF Blueprint: Users can download a detailed, step-by-step operational roadmap as a PDF.

🛠️ Tech Stack
Frontend: HTML5, CSS3 (Custom Neon UI), JavaScript (Vanilla), Bootstrap 5, Chart.js.

Backend: Python (Flask).

AI Engine: Google Gemini API (gemini-2.5-flash).

Deployment: Docker / Render / Koyeb (Stateless architecture).

⚡ Quick Start
Prerequisites
Python 3.9 or higher

A Google Cloud API Key (for Gemini)

1. Clone the Repository
Bash

git clone https://github.com/newgen-technopath
/dost-financial.git
cd dost-financial
2. Set Up Environment
It is recommended to use a virtual environment.

Bash

# Create virtual env
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Configure API Key
Create a .env file or export your key directly:

Bash

# Linux/Mac
export GOOGLE_API_KEY="your_actual_api_key_here"

# Windows (Command Prompt)
set GOOGLE_API_KEY=your_actual_api_key_here
5. Run the Application
Bash

python app.py
Visit http://localhost:5000 in your browser.

📂 Project Structure
Plaintext

dost-financial/
├── app.py              # Main Flask server & AI Logic
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment command for Render/Koyeb
├── templates/
│   ├── index.html      # Dashboard & Input Logic
│   └── report.html     # Blueprint & Dost Mode Logic
└── README.md           # Documentation
🚀 Deployment
This app is stateless and ready for serverless deployment.

Deploy on Render (Recommended)
Push code to GitHub.

Create a new Web Service on Render.

Connect your repository.

Add Environment Variable: GOOGLE_API_KEY.

Deploy!

Deploy on Koyeb
Push code to GitHub.

Create a new App on Koyeb.

Select GitHub as the source.

Add Environment Variable: GOOGLE_API_KEY.

Deploy!

Website is all already deployed but it might fail to fetch api sometimes so to test the application it is  recommended to run on vscode
