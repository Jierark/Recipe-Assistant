from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# We want to format the different parts of a recipe in specific ways
class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str

class Recipe(BaseModel):
    id: str
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    prep_time: str
    cook_time: str
    servings: int
    cuisine: Optional[str] = None
    diet: Optional[str] = None
    nutrition: Optional[Dict[str, Any]] = None
    difficulty: Optional[str] = None
    image_url: Optional[str] = None