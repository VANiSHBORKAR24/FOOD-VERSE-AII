# Food-Verse AI: Multimodal Food Intelligence Agent
**Google Cloud Generative AI Virtual Internship Capstone Project Report**
*MySkillWallet / SmartInternz Track: Generative AI with Google Cloud*

---

## 1. Executive Summary & Abstract
In modern health, fitness, and home management, understanding meal composition, nutritional value, and dietary risks is challenging. Traditional apps require tedious manual logging, searching generic databases, and guessing portion sizes. Furthermore, millions of households struggle with domestic food waste caused by unorganized refrigerators and pantries.

**Food-Verse AI** is an end-to-end multimodal AI application powered by **Google Cloud Generative AI (Gemini 1.5 Multimodal Architecture)**. By simply photographing a meal plate or open refrigerator, Food-Verse AI autonomously detects dishes, calculates portion weights, estimates macronutrients (protein, carbs, fat, fiber) and calories, suggests zero-waste culinary recipes from on-hand ingredients, and enforces strict allergen safety scans.

---

## 2. Problem Statement & Motivation
1. **Manual Nutrition Logging Friction**: Counting calories and macros by manually searching foods leads to high user dropout.
2. **Portion Misestimation**: People often misjudge serving sizes, distorting dietary tracking.
3. **Food Waste in Households**: Edible food is discarded simply because people don't know what recipes can be made with whatever random ingredients remain in their fridge.
4. **Allergen Risks**: Hidden allergens (gluten thickeners, peanut bases, dairy cross-contamination) pose health hazards when dining out.

---

## 3. System Architecture & Workflow

```
                                ┌────────────────────────────────────┐
                                │             User Device            │
                                │  (Camera / Food Image / Question)  │
                                └─────────────────┬──────────────────┘
                                                  │
                                                  ▼
                                ┌────────────────────────────────────┐
                                │       Streamlit UI Dashboard       │
                                │   (Uploads, Sliders, Visuals)      │
                                └─────────────────┬──────────────────┘
                                                  │
                                                  ▼
                                ┌────────────────────────────────────┐
                                │       Food-Verse Agent Engine      │
                                │   - Session & Dietary Context      │
                                │   - Persona & System Instruction   │
                                │   - Safety Verification Guard      │
                                └─────────────────┬──────────────────┘
                                                  │
                                                  ▼
                                ┌────────────────────────────────────┐
                                │  Google Cloud Gemini 1.5 Multimodal│
                                │  - Native Image-Text Tokenization  │
                                │  - Portions & Volume Estimation    │
                                │  - Multi-hop Culinary Reasoning    │
                                └─────────────────┬──────────────────┘
                                                  │
                                                  ▼
                                ┌────────────────────────────────────┐
                                │      Formatted Output & Visuals    │
                                │  - Nutritional Breakdown Table     │
                                │  - Plotly Macro Donut Chart        │
                                │  - Zero-Waste Recipes & Prep Tips  │
                                └────────────────────────────────────┘
```

---

## 4. Key Modules & Functional Features

### 📸 Module 1: Meal Vision & Calorie Scanner
- Accepts meal photographs from gallery or live camera feed.
- Identifies dishes, cuisines, and key visible ingredients.
- Estimates gram weight, total calories, protein, carbs, fats, and fiber.
- Renders an interactive Plotly donut chart visualising macronutrient ratios.
- Provides a "Healthiness Score" (1-10) with actionable dietary optimization tips.

### 🧊 Module 2: Fridge-to-Table Zero-Waste Chef
- Visual inventory parsing: Scans open fridges or pantry shelves to isolate produce, dairy, meats, and condiments.
- Contextual recipe generation: Yields two customized recipes based on selected cuisine style (Italian, Asian, Mexican, etc.), preparation time, and cooking skill level.
- Food preservation advice: Provides practical techniques to extend ingredient freshness.

### 🛡️ Module 3: Allergen & Safety Guard
- Scans meal images or restaurant descriptions against critical user allergens (peanuts, gluten, shellfish, dairy, soy, eggs, tree nuts).
- Categorizes threat into SAFE, CAUTION, or HIGH RISK.
- Flags hidden cross-contamination risks (cooking oils, shared fryers, broths).

### 💬 Module 4: Conversational Culinary Agent
- Multi-turn interactive chef and nutritionist chatbot.
- Answers ingredient substitution queries, cooking techniques, and dietary planning.

---

## 5. Technology Stack & Google Cloud Services

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Foundation Model** | **Google Gemini 1.5 Flash / Pro** | Native multimodal vision-language understanding, fast inference, long context |
| **Cloud AI Platform** | **Google Cloud Vertex AI / AI Studio** | Managed LLM endpoint deployment, API lifecycle & monitoring |
| **Application Logic** | **Python 3.10+** | Core orchestrator and agent controller |
| **User Interface** | **Streamlit** | Responsive, modern web interface with file upload, camera, and reactive state |
| **Data Visualization** | **Plotly Express & Pandas** | Dynamic interactive charts for macronutrient distribution |
| **SDKs** | `google-genai` / `google-generativeai` | Unified Google GenAI client library |

---

## 6. Prompt Engineering Techniques Applied
1. **System Persona Framing**: Setting the agent as an elite clinical nutritionist and certified chef.
2. **Schema-Constrained Markdown Output**: Directing the LLM to reply with standardized markdown tables, metrics, and bullet sections to guarantee predictable UI rendering.
3. **Contextual Grounding**: Injecting user dietary goals (e.g. Keto, Diabetic-friendly) into the prompt context for personalized analysis.
4. **Safety Verification Framing**: Enforcing heightened sensitivity during allergen analysis to prioritize diner safety.

---

## 7. Viva & Technical Interview Q&A Guide

#### Q1: Why did you choose Google Gemini 1.5 over a traditional CNN (like ResNet or YOLO) + separate LLM?
> **Answer**: Traditional pipelines require a computer vision detector to label bounding boxes, which are then passed to a separate text LLM. This leads to information loss and cascading errors. Gemini 1.5 is natively multimodal—it processes pixels and text in the same transformer space, enabling it to perceive textures, cooking styles (fried vs. grilled), sauces, and portion depths simultaneously.

#### Q2: How does the agent handle zero-waste cooking?
> **Answer**: The agent receives an image of the raw ingredients inside a pantry or fridge. It runs visual inventory parsing to categorize produce, proteins, and staples, then synthesizes recipes that prioritize consuming perishable items first, requiring only minimal pantry basics.

#### Q3: What is the difference between Gemini 1.5 Flash and Gemini 1.5 Pro in this project?
> **Answer**: Gemini 1.5 Flash is lightweight, low-latency, and cost-effective, ideal for real-time mobile meal scanning and interactive chat. Gemini 1.5 Pro provides deeper reasoning capabilities, useful for complex multi-ingredient nutritional audits and clinical dietary assessments.

#### Q4: How is user safety ensured regarding allergens?
> **Answer**: The agent uses an Allergen Safety prompt that explicitly flags both direct visible ingredients and covert vectors like sauces, marinades, frying oil cross-contamination, and thickeners.

---

## 8. Conclusion & Future Roadmap
Food-Verse AI demonstrates the power of Google Cloud Generative AI to solve everyday consumer health and sustainability challenges. Future phases could integrate live barcode scanning via Open Food Facts API and synchronization with Google Fit or Apple HealthKit for automated dietary logging.
