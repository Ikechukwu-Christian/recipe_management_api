# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from models import Recipe, Ingredient, NutritionalInfo, recipes_db

app = FastAPI()

# Create a recipe
@app.post("/recipes/")
async def create_recipe(recipe: Recipe):
    recipes_db.append(recipe)
    return recipe

# Read all recipes
@app.get("/recipes/", response_model=List[Recipe])
async def get_recipes():
    return recipes_db

# Read a single recipe by its index
@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    if recipe_id < len(recipes_db):
        return recipes_db[recipe_id]
    raise HTTPException(status_code=404, detail="Recipe not found")

# Update a recipe
@app.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: int, recipe: Recipe):
    if recipe_id < len(recipes_db):
        recipes_db[recipe_id] = recipe
        return {"message": "Recipe updated successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")

# Delete a recipe
@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    if recipe_id < len(recipes_db):
        del recipes_db[recipe_id]
        return {"message": "Recipe deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")

# Search recipes by title
@app.get("/recipes/search/")
async def search_recipes_by_title(title: str):
    found_recipes = [recipe for recipe in recipes_db if title.lower() in recipe.title.lower()]
    return found_recipes

# Filter recipes by ingredient
@app.get("/recipes/filter/")
async def filter_recipes_by_ingredient(ingredient_name: str):
    filtered_recipes = [recipe for recipe in recipes_db if any(ingredient.name.lower() == ingredient_name.lower() for ingredient in recipe.ingredients)]
    return filtered_recipes

# Filter recipes by nutritional content
@app.get("/recipes/filter/nutrition/")
async def filter_recipes_by_nutrition(calories: float = None, fat: float = None, protein: float = None):
    filtered_recipes = [recipe for recipe in recipes_db if 
                        (calories is None or recipe.nutritional_info.calories <= calories) and
                        (fat is None or recipe.nutritional_info.fat <= fat) and
                        (protein is None or recipe.nutritional_info.protein <= protein)]
    return filtered_recipes

# Create a recipe with calculated nutritional information
@app.post("/recipes/calculate/")
async def create_recipe_with_nutrition(recipe: Recipe):
    recipe.nutritional_info = calculate_nutritional_info(recipe.ingredients)
    recipes_db.append(recipe)
    return recipe
