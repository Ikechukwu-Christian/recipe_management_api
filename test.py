# tests/test_main.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_recipe():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        recipe_data = {
            "title": "Spaghetti Carbonara",
            "description": "Classic Italian pasta dish",
            "instructions": "Cook pasta, fry bacon, mix with eggs and cheese",
            "ingredients": [
                {"name": "pasta", "quantity": 200},
                {"name": "bacon", "quantity": 100},
                {"name": "eggs", "quantity": 2},
                {"name": "parmesan cheese", "quantity": 50}
            ],
            "nutritional_info": {
                "calories": 600,
                "fat": 20,
                "protein": 30
            }
        }
        response = await ac.post("/recipes/", json=recipe_data)
        assert response.status_code == 200
        assert response.json()["title"] == "Spaghetti Carbonara"
