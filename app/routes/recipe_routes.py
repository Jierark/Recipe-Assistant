from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.services.recipe_service import RecipeService
from app.schemas import *

import logging

logger = logging.getLogger("uvicorn.error")
router = APIRouter()
recipe_service = RecipeService()

# the @ symbol means that when /recipes is accessed, it will invoke the search_recipes method

@router.get("/recipes", response_model=List[Dict[str, str]])
async def search_recipes(query: str):
    '''
    Searches for recipes based on different filters
    '''
    if not query:
        raise HTTPException(status_code=400, detail="You forgot the query")

    try:
        # Get the raw recipes string
        recipes_str = recipe_service.search_recipes(query)
        print(type(recipes_str))
        
        # Parse the string into a list of recipe objects
        recipes = [{"title": title.strip(), "id": str(idx)} 
                  for idx, title in enumerate(recipes_str.split('\n')) 
                  if title.strip()]
        return recipes
    except Exception as e:
        logger.error(f"Error searching recipes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch recipes")
@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe_details(recipe_id: str):
    '''
    Returns more detailed information about a recipe.
    '''
    try:
        recipe_data = recipe_service.get_recipe_details(recipe_id)
        return Recipe(**recipe_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
