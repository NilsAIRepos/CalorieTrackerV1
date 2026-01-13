"""Agent pipeline for calorie tracking."""

import json
from typing import TypedDict, Optional
import sys

# Determine if we are running as a package or a script
if __package__:
    from .search import search_nutrition
    from .routers.llm import get_connector
else:
    # When running as a script, we need to ensure we can import 'search' and 'routers'
    # We assume the script is run from the 'backend' directory or root
    try:
        from search import search_nutrition
        from routers.llm import get_connector
    except ImportError:
        # Fallback if running from root and backend is not in path directly as top level
        # This handles 'python backend/agent.py' if the CWD is root
        from backend.search import search_nutrition
        from backend.routers.llm import get_connector

# Define the structure of the final output
class Ingredient(TypedDict):
    name: str
    amount: str
    calories: int
    protein: float
    carbs: float
    fat: float
    sugar: float

class MealPlan(TypedDict):
    name: str
    ingredients: list[Ingredient]
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    total_sugar: float

class AgentResponse(TypedDict):
    text: str
    draft_entry: Optional[MealPlan]

class Agent:
    def __init__(self, provider="local", base_url=None, model=None):
        self.connector = get_connector(provider, base_url, model)

    def process_message(self, history: list[dict]) -> AgentResponse:
        """
        Process the user's message history and determine the next step.
        """
        # Construct the context from history
        # We need to pass the conversation history to the analysis prompt
        # so the LLM can resolve references (e.g., "It was fried" refers to "Eggs" from prev turn).

        system_instruction = """You are a calorie tracking assistant. Your goal is to log meals accurately.
Analyze the user's latest input in the context of the conversation.
- If the user provides a food item but details are missing (e.g. quantity, preparation method), output {"action": "CLARIFY", "question": "..."}.
- If the user provides specific food items, output {"action": "SEARCH", "items": ["item 1", "item 2"]}.
- If the user is just saying hi or asking non-food questions, output {"action": "CHITCHAT", "reply": "..."}.

Output ONLY raw JSON. Do not use Markdown blocks."""

        # Construct full prompt with history
        # We assume 'history' contains {"role": "user"|"assistant", "content": "..."}
        messages = [{"role": "system", "content": system_instruction}]

        # Append history (skip system messages if any, though usually history is user/assistant)
        # We might limit history length if it gets too long, but for now take all.
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        response_text = None
        try:
            response_text = self.connector.chat(messages)
            # Try to clean the response in case LLM adds backticks
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            # Find the first { and last }
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end != -1:
                response_text = response_text[start:end]

            plan = json.loads(response_text)
        except Exception as e:
            # Fallback for parsing errors
            print(f"Agent JSON Parse/Chat Error: {e}")
            if response_text:
                print(f"Response text was: {response_text}")

            # Check for connection error to provide better message
            str_e = str(e)
            if "Connection refused" in str_e or "Max retries exceeded" in str_e:
                return {"text": "I cannot connect to the AI service. Please ensure Ollama is running.", "draft_entry": None}

            return {"text": "I'm having trouble understanding. Could you please specify what you ate?", "draft_entry": None}

        action = plan.get("action")

        if action == "CHITCHAT":
            return {"text": plan.get("reply", "Hello! Ready to log your meal?"), "draft_entry": None}

        if action == "CLARIFY":
            return {"text": plan.get("question", "Could you provide more details?"), "draft_entry": None}

        if action == "SEARCH":
            items = plan.get("items", [])
            ingredients_data = []

            # Notify user (in a real streaming setup this would be better, here we just do the work)
            # We will gather info for each item.

            for item in items:
                # 1. Search
                snippets = search_nutrition(item)
                snippet_text = "\n".join(snippets)

                # 2. Extract Data using LLM
                extract_prompt = [
                    {"role": "system", "content": f"""You are a nutritionist.
Based on the following search results, extract the nutritional info for '{item}'.
Search Results:
{snippet_text}

Estimate the values for the specific amount mentioned in '{item}'.
If the amount is not clear in the text, use a standard serving size and note it.
Output valid JSON only:
{{
  "name": "{item}",
  "amount": "detected amount or serving size",
  "calories": int,
  "protein": float (grams),
  "carbs": float (grams),
  "fat": float (grams),
  "sugar": float (grams)
}}
"""},
                    {"role": "user", "content": "Extract nutrition."}
                ]
                try:
                    extract_res = self.connector.chat(extract_prompt)
                    extract_res = extract_res.replace("```json", "").replace("```", "").strip()
                    start = extract_res.find("{")
                    end = extract_res.rfind("}") + 1
                    if start != -1 and end != -1:
                        extract_res = extract_res[start:end]

                    data = json.loads(extract_res)
                    ingredients_data.append(data)
                except Exception as e:
                    print(f"Extraction Error for {item}: {e}")
                    # Fallback or skip
                    continue

            # 3. Synthesize Final Entry
            if not ingredients_data:
                return {"text": "I couldn't find nutritional info for that. Could you try again?", "draft_entry": None}

            total_cal = sum(i['calories'] for i in ingredients_data)
            total_pro = sum(i['protein'] for i in ingredients_data)
            total_carb = sum(i['carbs'] for i in ingredients_data)
            total_fat = sum(i['fat'] for i in ingredients_data)
            total_sugar = sum(i['sugar'] for i in ingredients_data)

            meal_name = ", ".join([i['name'] for i in ingredients_data])

            draft = {
                "name": meal_name,
                "ingredients": ingredients_data,
                "total_calories": int(total_cal),
                "total_protein": round(total_pro, 1),
                "total_carbs": round(total_carb, 1),
                "total_fat": round(total_fat, 1),
                "total_sugar": round(total_sugar, 1)
            }

            return {
                "text": f"I've calculated the nutrition for {meal_name}. Please confirm the details below.",
                "draft_entry": draft
            }

        return {"text": "I'm not sure how to help with that.", "draft_entry": None}

if __name__ == "__main__":
    # Test script
    import sys
    from pathlib import Path
    # Add project root to path for imports to work if run directly
    sys.path.append(str(Path(__file__).parent.parent))

    agent = Agent()
    # Use a fake history
    print(agent.process_message([{"role": "user", "content": "I had 2 boiled eggs"}]))
