a = '{"search_terms": "Korean dish beef", "cuisine": "Korean", "diet": None, "ingredients": "beef"}'
print(a)
import json

a = '{"search_term": "Korean dish beef", "cuisine": "Korean", "diet": "None", "ingredients": "beef"}'
b = json.loads(a)
print(type(b))
print(b)