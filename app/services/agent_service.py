from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class NLPAgent:
    """
    Processes natural language and converts to relevant jsons for further use
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    def process_recipe_query(self, query: str):
        """
        Given a user input recipe query, output a json with the relevant search terms.
        """

        prompt = f"""
        Analyze this user query: {query}.
        The user is looking for recipes that follow a set of criteria, including cuisine, diet, and use of specified ingredients.

        You should extract the following information from the prompt:
        - search_terms: the main search terms to use
        - cuisine: the specified cuisine (i.e. Spanish, Italian, Asian)
        - diet: specified dietary preferences (i.e. vegetarian, gluten-free)
        - ingredients: any specified ingredients to use 

        IMPORTANT: Return ONLY the JSON object, with no additional text.
        The JSON MUST be valid and follow this exact format:
        {{"search_terms": "string", "cuisine": "string" or None, "diet": "string" or None, "ingredients": "string" or None}}

        Example output:
        {{"search_terms": "chicken pasta", "cuisine": "Italian", "diet": "gluten-free", "ingredients": "tomatoes"}}
        """
        response = self.client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" } # man I can't believe this is what I needed to get json return
        )
        # maybe I should just rewrite this logic, chatGPT is having a ton of issues with formatting jsons
        res = response.choices[0].message.content
        try:
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            # Return a default value
            return {
                "search_terms": query,  # Use the original query as fallback
                "cuisine": None,
                "diet": None,
                "ingredients": None
            }