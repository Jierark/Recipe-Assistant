from openai import OpenAI
from dotenv import load_dotenv
import os
from app.schemas import *
import json

from app.services.agent_service import NLPAgent

load_dotenv()

class RecipeService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.nlp_agent = NLPAgent()
    # Accessed via /api/recipes?query=
    def search_recipes(self,query: str):
        processed_query = self.nlp_agent.process_recipe_query(query)

        return self.search_recipes_parameterized(
            cuisine=processed_query["cuisine"],
            diet=processed_query["diet"],
            ingredients=processed_query["ingredients"],
        )

    def search_recipes_parameterized(self, cuisine=None, diet=None, ingredients=None):
        prompt = f"Can you find recipes"
        if cuisine and cuisine != 'null':
            prompt += f" in {cuisine} cuisine"
        if diet and diet != 'null':
            prompt += f" that follow a {diet} diet"
        if ingredients and ingredients != 'null':
            prompt += f" using the following ingredients: {ingredients}"

        prompt += "? ONLY provide a small list of possible recipes. Do not add any extraneous information to your output."
        print("sending prompt:", prompt)
        response = self.client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": prompt}]
        )
        print("response received from recipe search")
        return response.choices[0].message.content

    def get_recipe_details(self, recipe_name: str):
        prompt = f"""
        Please provide detailed information about the recipe for {recipe_name}. Include the following details:
        - Title
        - Description
        - Ingredients with amounts and units
        - Step-by-Step Instructions
        - Prep time
        - Cook time
        - Number of servings
        - Cuisine type
        - Dietary information
        - Nutritional information
        - Difficulty level
        - Image URL, if possible

        Format the response in JSON using these fields:
        {Recipe.model_json_schema()}
        """

        response = self.client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        try:
            json_response = json.loads(response.choices[0].message.content)
            return json_response
        except json.JSONDecodeError:
            print("Error: Could not parse JSON response")
            print("Raw response:", response.choices[0].message.content)
            return {"error": "Could not parse recipe details"}