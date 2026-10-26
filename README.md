# 🥑 Food-Verse AI: Multimodal Food Intelligence Agent

An intelligent, multimodal food recognition, zero-waste culinary planner, and nutrition agent powered by **Google Cloud Generative AI (Gemini 1.5)**.

Built for the **Google Cloud Generative AI Internship / Capstone Track** on **MySkillWallet & SmartInternz**.

---

## 🌟 Key Features & Food-Themed UI

1. **🎨 Warm Culinary Aesthetic**: Designed with an appetite-inspiring palette (Tomato Red, Fresh Basil Green, Saffron Gold, and warm parchment cream cards).
2. **✨ 1-Click Interactive Sample Plates**: Test immediately with pre-loaded high-res culinary samples (Grilled Salmon Quinoa Bowl, Neapolitan Margherita Pizza, Fresh Fridge Basket) or use your own uploads/camera.
3. **📊 Dynamic Nutritional Scoreboard**: Real-time KPI cards for Calories, Protein, Carbs, Fats, and Fiber with an interactive Plotly donut chart.
4. **🥗 Today's Calorie Food Diary**: Log meals with one click, track your daily 2,000 kcal intake with an interactive progress meter, and manage your daily meals history.
5. **🧊 Zero-Waste Fridge Chef**: Visual ingredient detection formulations to eliminate domestic kitchen waste with food preservation hacks.
6. **🛡️ Allergen Safety Radar**: Color-coded danger alerts (Green/Yellow/Red) for peanuts, gluten, dairy, shellfish, and cross-contamination risks.
7. **⚡ Clickable Chef Prompt Pills**: Instant 1-click questions for high-protein breakfasts, low-calorie swaps, preserving greens, and fixing salty recipes.
8. **📑 Full Documentation & Viva Q&A**: Includes complete technical architecture and interview questions in `PROJECT_REPORT.md`.

---

## 🚀 Quick Start Guide

### Step 1: Open the Project Directory
The project has been generated in your workspace at:
```bash
cd /Users/vanishborkar/.gemini/antigravity/scratch/food-verse-ai
```

### Step 2: (Optional) Set up your Gemini API Key
You can use the app immediately in **Demo Mode**, or connect real-time Google Cloud Gemini Vision:
1. Get a free Gemini API key at: [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Either:
   - Copy `.env.example` to `.env` and paste your key:
     ```bash
     cp .env.example .env
     ```
   - Or enter it directly in the app's sidebar when it opens.

### Step 3: Run the Application
You can use the automated startup script:
```bash
./run.sh
```
Or run manually with:
```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Streamlit
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`.

---

## 📂 Project Structure

```
food-verse-ai/
├── app.py               # Streamlit interactive UI application
├── food_agent.py        # Core Multimodal AI Agent logic & fallbacks
├── config.py            # Environment configurations & dietary constants
├── prompts.py           # Advanced prompt engineering & system instructions
├── requirements.txt     # Python dependencies
├── .env.example         # Template for API keys
├── run.sh               # One-click startup script
├── PROJECT_REPORT.md    # Submission-ready project report & Viva Q&A
└── README.md            # Quickstart documentation
```

---

## 🎓 For Course Submission (MySkillWallet / SmartInternz)
- Use `PROJECT_REPORT.md` for your submission writeup, architecture diagrams, and viva preparation.
- You can take screenshots or record a short video walkthrough using the Streamlit web interface.
