"""
Food-Verse AI Agent Engine
Communicates with Google Cloud Gemini Multimodal APIs.
"""

import io
import re
from typing import List, Optional, Dict
from PIL import Image
import prompts
from config import DEFAULT_MODEL


def extract_nutritional_metrics(text: str) -> Dict[str, any]:
    """Parse key numerical metrics from the generated markdown report."""
    metrics = {
        "dish_name": "Identified Dish",
        "calories": 480,
        "protein": 34,
        "carbs": 45,
        "fat": 18,
        "fiber": 7,
        "health_score": 8.5,
        "risk_level": "SAFE"
    }

    # Extract dish name
    name_match = re.search(r"\*\*Dish Name\*\*:\s*([^\n\r]+)", text)
    if name_match:
        metrics["dish_name"] = name_match.group(1).strip()

    # Extract calories
    cal_match = re.search(r"\*\*Calories\*\*.*?(\d{2,4})\s*(?:kcal|calories)?", text, re.IGNORECASE)
    if cal_match:
        metrics["calories"] = int(cal_match.group(1))

    # Extract protein
    pro_match = re.search(r"\*\*Protein\*\*.*?(\d{1,3})\s*g", text, re.IGNORECASE)
    if pro_match:
        metrics["protein"] = int(pro_match.group(1))

    # Extract carbs
    carb_match = re.search(r"\*\*Carbohydrates\*\*.*?(\d{1,3})\s*g", text, re.IGNORECASE)
    if carb_match:
        metrics["carbs"] = int(carb_match.group(1))

    # Extract fat
    fat_match = re.search(r"\*\*Total Fat\*\*.*?(\d{1,3})\s*g", text, re.IGNORECASE)
    if fat_match:
        metrics["fat"] = int(fat_match.group(1))

    # Extract fiber
    fiber_match = re.search(r"\*\*Dietary Fiber\*\*.*?(\d{1,3})\s*g", text, re.IGNORECASE)
    if fiber_match:
        metrics["fiber"] = int(fiber_match.group(1))

    # Extract health score
    score_match = re.search(r"\*\*Healthiness Score\*\*:\s*([\d\.]+)", text, re.IGNORECASE)
    if score_match:
        try:
            metrics["health_score"] = float(score_match.group(1))
        except ValueError:
            pass

    return metrics


class FoodVerseAgent:
    def __init__(self, api_key: str = "", model_name: str = DEFAULT_MODEL):
        self.api_key = api_key.strip()
        self.model_name = model_name
        self.client = None
        self.sdk_type = None

        if self.api_key:
            self._init_client()

    def _init_client(self):
        """Initialize Google GenAI client with fallback support."""
        # 1. Try modern google-genai SDK
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            self.sdk_type = "google-genai"
            return
        except (ImportError, Exception):
            pass

        # 2. Try legacy google-generativeai SDK
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=self.api_key)
            self.client = legacy_genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=prompts.SYSTEM_PROMPT
            )
            self.sdk_type = "google-generativeai"
            return
        except (ImportError, Exception):
            self.client = None
            self.sdk_type = None

    def is_configured(self) -> bool:
        return bool(self.api_key and self.client is not None)

    def analyze_meal(
        self,
        image: Optional[Image.Image],
        dietary_context: str = "None",
        user_notes: str = ""
    ) -> str:
        """Analyze food photo for identification, calories, and macros."""
        prompt_text = prompts.MEAL_ANALYSIS_PROMPT.format(
            dietary_context=dietary_context,
            user_notes=user_notes or "None provided"
        )

        if not self.is_configured():
            return self._mock_meal_analysis(dietary_context, user_notes)

        return self._call_multimodal(prompt=prompt_text, image=image)

    def inspect_fridge_and_cook(
        self,
        image: Optional[Image.Image],
        cuisine: str = "Any / Fusion",
        prep_time: str = "30 mins",
        skill_level: str = "Intermediate",
        dietary_pref: str = "None"
    ) -> str:
        """Detect fridge/pantry ingredients and suggest zero-waste recipes."""
        prompt_text = prompts.FRIDGE_INSPECTOR_PROMPT.format(
            cuisine=cuisine,
            prep_time=prep_time,
            skill_level=skill_level,
            dietary_pref=dietary_pref
        )

        if not self.is_configured():
            return self._mock_fridge_recipes(cuisine)

        return self._call_multimodal(prompt=prompt_text, image=image)

    def check_allergens(
        self,
        image: Optional[Image.Image],
        allergens: List[str],
        description: str = ""
    ) -> str:
        """Scan meal for allergen risks and cross-contamination."""
        allergen_str = ", ".join(allergens) if allergens else "None specified"
        prompt_text = prompts.ALLERGEN_SAFETY_PROMPT.format(allergens=allergen_str)
        if description:
            prompt_text += f"\nAdditional dish description: {description}"

        if not self.is_configured():
            return self._mock_allergen_scan(allergens)

        return self._call_multimodal(prompt=prompt_text, image=image)

    def chat_message(
        self,
        message: str,
        image: Optional[Image.Image] = None,
        chat_history: Optional[List[dict]] = None
    ) -> str:
        """Interactive culinary assistant message."""
        if not self.is_configured():
            return (
                "👋 **Food-Verse Demo Assistant**: I received your query! "
                f"You asked: *\"{message}\"*. \n\n"
                "*(To enable live Google Cloud Gemini reasoning, please input your Gemini API Key in the left sidebar!)*"
            )

        context_prompt = prompts.CHAT_AGENT_SYSTEM_PROMPT + "\n\nUser Question:\n" + message
        return self._call_multimodal(prompt=context_prompt, image=image)

    def _call_multimodal(self, prompt: str, image: Optional[Image.Image]) -> str:
        """Helper to invoke Gemini multimodal endpoint."""
        try:
            if self.sdk_type == "google-genai":
                from google.genai import types
                contents = []
                if image:
                    contents.append(image)
                contents.append(prompt)

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=prompts.SYSTEM_PROMPT,
                        temperature=0.4
                    )
                )
                return response.text

            elif self.sdk_type == "google-generativeai":
                parts = []
                if image:
                    parts.append(image)
                parts.append(prompt)
                response = self.client.generate_content(parts)
                return response.text

            else:
                return "⚠️ Error: Neither `google-genai` nor `google-generativeai` SDK is available in the environment."

        except Exception as e:
            return f"⚠️ **Google Cloud Gemini Error**: {str(e)}\n\nPlease ensure your API Key is valid and has Gemini API enabled."

    # --- Realistic Fallback Demos (allows testing immediately without an API key) ---

    def _mock_meal_analysis(self, dietary_context: str, user_notes: str = "") -> str:
        if "salad" in user_notes.lower():
            return f"""### 🍽️ Dish Identification
- **Dish Name**: California Harvest Avocado & Kale Bowl with Chickpeas, Cherry Tomatoes & Goat Cheese
- **Estimated Portion Weight**: ~340 grams
- **Key Ingredients Visible**: Chopped curly kale, baby spinach, Haas avocado slices, roasted chickpeas, cucumber ribbons, crumbled goat cheese, lemon vinaigrette

### 📊 Nutritional Breakdown (Estimated)
| Metric | Quantity | Daily Value % |
| :--- | :--- | :--- |
| **Calories** | **385 kcal** | ~19% |
| **Protein** | **16g** | ~32% |
| **Carbohydrates** | **34g** | ~12% |
| **Dietary Fiber** | **11g** | ~39% |
| **Total Fat** | **22g** | ~28% |
| **Key Micronutrients** | Vitamin K, Folate, Vitamin C, Potassium | Very High |

### 🥗 Health & Diet Evaluation
- **Healthiness Score**: **9.5 / 10** (Superfood Antioxidant Bowl)
- **Dietary Alignment**: Vegetarian, Gluten-Free, and High-Fiber. (Target was: *{dietary_context}*).
- **Strengths**: Exceptional prebiotic fiber content from legumes and monounsaturated healthy fats from avocado.
- **Tips for Optimization**: Add grilled tofu, edamame, or pumpkin seeds to increase total protein above 25g.

### ⚠️ Allergen & Warning Flags
- **Allergens Present**: 🥛 **Dairy (Goat cheese)**.
- **Gluten Status**: 100% naturally gluten-free.

*(⚡ Demo Preview Mode: Add your Gemini API key in the sidebar for live vision AI on any image!)*
"""
        elif "pizza" in user_notes.lower():
            return f"""### 🍽️ Dish Identification
- **Dish Name**: Artisan Neapolitan Margherita Pizza with San Marzano Tomatoes & Fresh Basil
- **Estimated Portion Weight**: ~320 grams (2 large slices)
- **Key Ingredients Visible**: Woodfired sourdough crust, crushed San Marzano tomatoes, fresh mozzarella fior di latte, basil leaves, extra virgin olive oil

### 📊 Nutritional Breakdown (Estimated)
| Metric | Quantity | Daily Value % |
| :--- | :--- | :--- |
| **Calories** | **590 kcal** | ~30% |
| **Protein** | **24g** | ~48% |
| **Carbohydrates** | **68g** | ~25% |
| **Dietary Fiber** | **4g** | ~14% |
| **Total Fat** | **23g** | ~29% |
| **Key Micronutrients** | Lycopene, Calcium, Vitamin A | Moderate |

### 🥗 Health & Diet Evaluation
- **Healthiness Score**: **7.2 / 10** (Classic Mediterranean Comfort)
- **Dietary Alignment**: Vegetarian friendly. (Target was: *{dietary_context}*).
- **Strengths**: Clean ingredient profile with fermented dough and antioxidant-rich lycopene from roasted tomatoes.
- **Tips for Optimization**: Pair with a crisp leafy arugula side salad to add micronutrients and fiber.

### ⚠️ Allergen & Warning Flags
- **Allergens Present**: 🌾 **Gluten (Wheat crust)**, 🥛 **Dairy (Mozzarella)**.
- **Cross-Contamination**: May be baked in shared ovens with nut/meat toppings.

*(⚡ Demo Preview Mode: Add your Gemini API key in the sidebar for live vision AI on any image!)*
"""
        return f"""### 🍽️ Dish Identification
- **Dish Name**: Grilled Salmon with Tri-Color Quinoa, Steamed Broccoli & Sliced Avocado (Mediterranean)
- **Estimated Portion Weight**: ~380 grams
- **Key Ingredients Visible**: Atlantic salmon fillet, quinoa grain blend, broccoli florets, fresh avocado, microgreens, charred lemon

### 📊 Nutritional Breakdown (Estimated)
| Metric | Quantity | Daily Value % |
| :--- | :--- | :--- |
| **Calories** | **480 kcal** | ~24% |
| **Protein** | **38g** | ~76% |
| **Carbohydrates** | **32g** | ~11% |
| **Dietary Fiber** | **6g** | ~21% |
| **Total Fat** | **22g** | ~28% |
| **Key Micronutrients** | Omega-3 Fatty Acids, Vitamin D, Potassium, Vitamin C | High |

### 🥗 Health & Diet Evaluation
- **Healthiness Score**: **9.2 / 10** (Nutrient-dense powerhouse)
- **Dietary Alignment**: Compatible with High-Protein, Mediterranean, and Gluten-Free lifestyles. (Target was: *{dietary_context}*).
- **Strengths**: Outstanding ratio of lean protein and heart-healthy Omega-3 fatty acids with low glycemic carbohydrates.
- **Tips for Optimization**: Moderate butter dressing if aiming for stricter caloric deficits.

### ⚠️ Allergen & Warning Flags
- **Allergens Present**: 🐟 **Fish (Salmon)**, 🥛 **Dairy (Butter sauce)**.
- **Gluten Status**: Naturally gluten-free (verify sauce thickeners).

*(⚡ Demo Preview Mode: Add your Gemini API key in the sidebar for real-time live vision AI!)*
"""

    def _mock_fridge_recipes(self, cuisine: str) -> str:
        return f"""### 🧊 Detected Inventory
- **Fresh Produce**: Bell peppers (red & green), cherry tomatoes, fresh spinach, yellow onions, garlic
- **Proteins / Dairy**: Eggs (half-dozen), block of feta cheese, Greek yogurt
- **Pantry & Sauces**: Olive oil, black pepper, canned chickpeas

---

### 👨‍🍳 Recipe Option 1: Mediterranean Shakshuka with Poached Eggs
- **Prep Time**: 10 mins | **Cook Time**: 15 mins | **Difficulty**: Easy
- **Ingredients Used**: Bell peppers, cherry tomatoes, onions, garlic, eggs, feta cheese, olive oil
- **Common Pantry Essentials Needed**: Cumin, paprika, salt, crusty bread
- **Step-by-step Instructions**:
  1. Heat olive oil in a skillet. Sauté diced onions and bell peppers for 5 minutes until tender.
  2. Add minced garlic and crushed cherry tomatoes with a pinch of cumin and salt; simmer into a rich sauce.
  3. Make small wells in the sauce and crack the eggs gently into each pocket.
  4. Cover and cook on low heat for 5-7 minutes until whites are set and yolks are runny. Garnish with crumbled feta.

---

### 👨‍🍳 Recipe Option 2: Crispy Chickpea & Spinach Power Skillet
- **Prep Time**: 5 mins | **Cook Time**: 12 mins
- **Highlights**: High-fiber, vegetarian high-protein quick lunch.
- **Step-by-step Instructions**:
  1. Drain and pat chickpeas dry. Pan-roast in olive oil until crispy and golden.
  2. Toss in garlic and wilt fresh spinach for 90 seconds.
  3. Drizzle with Greek yogurt-garlic sauce and cracked black pepper.

### 💡 Food-Saving Tip
- Wrap remaining fresh spinach leaves in a dry paper towel inside an airtight container; this absorbs moisture and doubles its shelf life!
"""

    def _mock_allergen_scan(self, allergens: List[str]) -> str:
        allergen_str = ", ".join(allergens) if allergens else "None selected"
        return f"""### 🛡️ Safety Assessment
- **Risk Level**: ⚠️ **CAUTION / MODERATE RISK**
- **User Allergens Flagged**: {allergen_str}
- **Scan Finding**: The dish appears to contain dairy components (cheese/cream) and traces of sesame or seeds on the crust.
- **Safe Alternatives**: Request dairy-free cheese or olive-oil drizzle substitution, and ask kitchen to use dedicated gluten-free and nut-free prep surfaces.
"""
