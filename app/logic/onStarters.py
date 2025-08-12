import chainlit as cl


@cl.set_starters
async def execute():
    return [
        cl.Starter(
            label="Constrained Recipe Finder",
            message="Suggest me some recipes. I'm vegetarian and I don't know what to cook for breakfast. It should be less than 1000 calories though.",
            icon="/public/food.svg",
        ),
        cl.Starter(
            label="Vague Recipe Finder",
            message="Help me finding a recipe that I cooked in the past. I remember that I had to cook guanciale, then mix the eggs and cook pasta",
            icon="/public/food.svg",
        ),
        cl.Starter(
            label="Similar Recipe Finder",
            message="I really liked the lentil stew recipe. Can you give me a couple of similar recipes?",
            icon="/public/similar_recipes.svg",
        ),
        cl.Starter(
            label="Shopping List Generator",
            message="Give me the shopping list for the recipe pasta alla carbonara.",
            icon="/public/shopping.svg",
        ),
        cl.Starter(
            label="Store Product Locator",
            message="Help me finding the extra virgin olive oil, of Filippo Berio brand, in the Edeka supermarket",
            icon="/public/location.svg",
        ),
        cl.Starter(
            label="Mixed",
            message="Give me all the ingredients of pasta alla carbonara, then prepare a shopping list for it and give me the location of each product inside Edeka.",
            icon="/public/mixed.svg",
        ),
    ]
