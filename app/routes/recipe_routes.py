from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.services.recipe_service import RecipeService
from app.schemas import *
router = APIRouter()
recipe_service = RecipeService()

# the @ symbol means that when /recipes is accessed, it will invoke the search_recipes method
@router.get("/recipes", response_model=str)
async def search_recipes(query: str):
    '''
    Searches for recipes based on different filters
    '''
    if not query:
        raise HTTPException(status_code=400,detail="You forgot the query")

    return recipe_service.search_recipes(query)

@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: str):
    '''
    Returns more detailed information about a recipe.
    '''
    try:
        recipe_data = recipe_service.get_recipe_details(recipe_id)
        return Recipe(**recipe_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/recipes/{recipe_id}/ingredients", response_model=List[Ingredient])
async def get_recipe_ingredients(recipe_id: str):
    '''
    Returns ingredients for a recipe
    '''
    return []
