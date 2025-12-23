from datetime import datetime
from app.config import SessionLocal
from app.models.drink import Drink
from app.models.ingredient import Ingredient
from app.models.drink_ingredient import DrinkIngredient
from app.models.customized_drink import CustomizedDrink


def seed_data():
    db = SessionLocal()
    
    try:
        # Clear existing data (except users)
        db.query(DrinkIngredient).delete()
        db.query(CustomizedDrink).delete()
        db.query(Ingredient).delete()
        db.query(Drink).delete()
        
        # Seed Drinks
        drinks_data = [
            {
                "name": "Caffe Latte",
                "category": "Espresso",
                "description": "Rich espresso balanced with steamed milk and a light layer of foam",
                "image_url": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_CaffeLatte.jpg",
                "base_beverage": "Espresso",
                "default_size": "Grande",
                "default_ice_level": "Hot",
                "default_sweetness_level": 0,
                "is_customizable": True,
                "createdAt": datetime.now()
            },
            {
                "name": "Caramel Macchiato",
                "category": "Espresso",
                "description": "Freshly steamed milk with vanilla-flavored syrup, marked with espresso and finished with caramel sauce",
                "image_url": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_CaramelMacchiato.jpg",
                "base_beverage": "Espresso",
                "default_size": "Grande",
                "default_ice_level": "Hot",
                "default_sweetness_level": 4,
                "is_customizable": True,
                "createdAt": datetime.now()
            },
            {
                "name": "White Chocolate Mocha",
                "category": "Espresso",
                "description": "Espresso combined with white chocolate sauce and steamed milk, topped with whipped cream",
                "image_url": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_WhiteChocolateMocha.jpg",
                "base_beverage": "Espresso",
                "default_size": "Grande",
                "default_ice_level": "Hot",
                "default_sweetness_level": 5,
                "is_customizable": True,
                "createdAt": datetime.now()
            },
            {
                "name": "Iced Matcha Green Tea Latte",
                "category": "Tea",
                "description": "Smooth and creamy matcha sweetened just right and served with milk over ice",
                "image_url": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_IcedMatchaGreenTeaLatte.jpg",
                "base_beverage": "Matcha",
                "default_size": "Grande",
                "default_ice_level": "Regular Ice",
                "default_sweetness_level": 4,
                "is_customizable": True,
                "createdAt": datetime.now()
            },
            {
                "name": "Strawberry Acai Refresher",
                "category": "Refresher",
                "description": "Sweet strawberry flavors accented by passion fruit and acai notes",
                "image_url": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_StrawberryAcaiStarbucksRefresher.jpg",
                "base_beverage": "Refresher Base",
                "default_size": "Grande",
                "default_ice_level": "Regular Ice",
                "default_sweetness_level": 4,
                "is_customizable": True,
                "createdAt": datetime.now()
            }
        ]
        
        drinks = [Drink(**data) for data in drinks_data]
        db.add_all(drinks)
        db.commit()
        print(f"✅ Seeded {len(drinks)} drinks")
        
        # Seed Ingredients
        ingredients_data = [
            # Milk types
            {"name": "Whole Milk", "type": "milk", "created_at": datetime.now()},
            {"name": "2% Milk", "type": "milk", "created_at": datetime.now()},
            {"name": "Nonfat Milk", "type": "milk", "created_at": datetime.now()},
            {"name": "Oat Milk", "type": "milk", "created_at": datetime.now()},
            {"name": "Almond Milk", "type": "milk", "created_at": datetime.now()},
            {"name": "Soy Milk", "type": "milk", "created_at": datetime.now()},
            {"name": "Coconut Milk", "type": "milk", "created_at": datetime.now()},
            
            # Syrups
            {"name": "Vanilla Syrup", "type": "syrup", "created_at": datetime.now()},
            {"name": "Caramel Syrup", "type": "syrup", "created_at": datetime.now()},
            {"name": "Hazelnut Syrup", "type": "syrup", "created_at": datetime.now()},
            {"name": "Peppermint Syrup", "type": "syrup", "created_at": datetime.now()},
            {"name": "Mocha Syrup", "type": "syrup", "created_at": datetime.now()},
            {"name": "White Chocolate Syrup", "type": "syrup", "created_at": datetime.now()},
            
            # Toppings
            {"name": "Whipped Cream", "type": "topping", "created_at": datetime.now()},
            {"name": "Caramel Drizzle", "type": "topping", "created_at": datetime.now()},
            {"name": "Chocolate Drizzle", "type": "topping", "created_at": datetime.now()},
            {"name": "Cinnamon Powder", "type": "topping", "created_at": datetime.now()},
            
            # Espresso shots
            {"name": "Espresso Shot", "type": "shot", "created_at": datetime.now()},
            
            # Base
            {"name": "Matcha Powder", "type": "base", "created_at": datetime.now()},
            {"name": "Refresher Base", "type": "base", "created_at": datetime.now()},
        ]
        
        ingredients = [Ingredient(**data) for data in ingredients_data]
        db.add_all(ingredients)
        db.commit()
        print(f"✅ Seeded {len(ingredients)} ingredients")
        
        # Seed Drink-Ingredient relationships
        drink_ingredients_data = [
            # Caffe Latte (drink id: 1)
            {"drink_id": 1, "ingredient_id": 1, "quantity": 12, "unit": "oz", "is_removable": True},
            {"drink_id": 1, "ingredient_id": 18, "quantity": 2, "unit": "shot", "is_removable": False},
            
            # Caramel Macchiato (drink id: 2)
            {"drink_id": 2, "ingredient_id": 1, "quantity": 10, "unit": "oz", "is_removable": True},
            {"drink_id": 2, "ingredient_id": 8, "quantity": 4, "unit": "pump", "is_removable": True},
            {"drink_id": 2, "ingredient_id": 9, "quantity": 1, "unit": "drizzle", "is_removable": True},
            {"drink_id": 2, "ingredient_id": 18, "quantity": 2, "unit": "shot", "is_removable": False},
            
            # White Chocolate Mocha (drink id: 3)
            {"drink_id": 3, "ingredient_id": 1, "quantity": 10, "unit": "oz", "is_removable": True},
            {"drink_id": 3, "ingredient_id": 13, "quantity": 4, "unit": "pump", "is_removable": True},
            {"drink_id": 3, "ingredient_id": 14, "quantity": 1, "unit": "topping", "is_removable": True},
            {"drink_id": 3, "ingredient_id": 18, "quantity": 2, "unit": "shot", "is_removable": False},
            
            # Iced Matcha Green Tea Latte (drink id: 4)
            {"drink_id": 4, "ingredient_id": 1, "quantity": 12, "unit": "oz", "is_removable": True},
            {"drink_id": 4, "ingredient_id": 19, "quantity": 3, "unit": "scoop", "is_removable": False},
            
            # Strawberry Acai Refresher (drink id: 5)
            {"drink_id": 5, "ingredient_id": 20, "quantity": 16, "unit": "oz", "is_removable": False},
        ]
        
        drink_ingredients = [DrinkIngredient(**data) for data in drink_ingredients_data]
        db.add_all(drink_ingredients)
        db.commit()
        print(f"✅ Seeded {len(drink_ingredients)} drink-ingredient relationships")
        
        # Seed Customized Drinks
        customized_drinks_data = [
            {
                "name": "My Perfect Latte",
                "base_drink_name": "Caffe Latte",
                "base_drink_photo": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_CaffeLatte.jpg",
                "image": "/uploads/drinks/sample-latte.png",
                "milk_type": "Oat Milk",
                "sugar_level": "50%",
                "cup_size": "Venti",
                "extras": "Extra Shot, Vanilla Syrup",
                "total_price": 6.95,
                "created_at": datetime.now()
            },
            {
                "name": "Iced Caramel Cloud",
                "base_drink_name": "Caramel Macchiato",
                "base_drink_photo": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_CaramelMacchiato.jpg",
                "image": "/uploads/drinks/sample-caramel.png",
                "milk_type": "Almond Milk",
                "sugar_level": "75%",
                "cup_size": "Grande",
                "extras": "Extra Caramel Drizzle, Whipped Cream",
                "total_price": 7.45,
                "created_at": datetime.now()
            },
            {
                "name": "Zen Matcha",
                "base_drink_name": "Iced Matcha Green Tea Latte",
                "base_drink_photo": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190617_IcedMatchaGreenTeaLatte.jpg",
                "image": "/uploads/drinks/sample-matcha.png",
                "milk_type": "Coconut Milk",
                "sugar_level": "25%",
                "cup_size": "Venti",
                "extras": "Light Ice",
                "total_price": 6.25,
                "created_at": datetime.now()
            }
        ]
        
        customized_drinks = [CustomizedDrink(**data) for data in customized_drinks_data]
        db.add_all(customized_drinks)
        db.commit()
        print(f"✅ Seeded {len(customized_drinks)} customized drinks")
        
        print("\n🎉 Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()

