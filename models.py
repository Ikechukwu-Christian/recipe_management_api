# models.py
from typing import List
from pydantic import BaseModel

class NutritionalInfo(BaseModel):
    calories: float
    fat: float
    protein: float

class Ingredient(BaseModel):
    name: str
    quantity: float

class Recipe(BaseModel):
    title: str
    description: str
    instructions: str
    ingredients: List[Ingredient]
    nutritional_info: NutritionalInfo

# Database simulation
recipes_db = []
