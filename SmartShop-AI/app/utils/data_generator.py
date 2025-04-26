import random
from datetime import datetime, timedelta
import uuid
from typing import List, Dict

class DataGenerator:
    def __init__(self):
        self.categories = [
            "Electronics", "Fashion", "Home & Garden", "Books", "Sports", 
            "Beauty", "Toys", "Automotive", "Health", "Grocery",
            "Pet Supplies", "Office Products", "Music", "Movies", "Games"
        ]
        
        self.brands = {
            "Electronics": ["Apple", "Samsung", "Sony", "LG", "Dell", "HP", "Lenovo", "Asus", "Acer", "Microsoft"],
            "Fashion": ["Nike", "Adidas", "Zara", "H&M", "Uniqlo", "Gucci", "Prada", "Levi's", "Tommy Hilfiger", "Ralph Lauren"],
            "Home & Garden": ["IKEA", "Wayfair", "Ashley", "Pottery Barn", "Crate & Barrel", "West Elm", "HomeGoods", "Bed Bath & Beyond"],
            "Books": ["Penguin", "HarperCollins", "Simon & Schuster", "Macmillan", "Random House", "Scholastic", "Hachette"],
            "Sports": ["Nike", "Adidas", "Under Armour", "Puma", "Reebok", "New Balance", "ASICS", "The North Face"],
            "Beauty": ["L'Oreal", "Maybelline", "MAC", "Estee Lauder", "Clinique", "Revlon", "NYX", "Urban Decay"],
            "Toys": ["LEGO", "Hasbro", "Mattel", "Fisher-Price", "Playmobil", "Melissa & Doug", "Nintendo"],
            "Automotive": ["Bosch", "3M", "Michelin", "Castrol", "Mobil", "Shell", "Goodyear", "Continental"],
            "Health": ["Johnson & Johnson", "Centrum", "Nature Made", "One A Day", "Vitafusion", "Garden of Life"],
            "Grocery": ["Nestle", "Kellogg's", "General Mills", "Kraft Heinz", "PepsiCo", "Coca-Cola", "Mars", "Hershey's"],
            "Pet Supplies": ["Purina", "Royal Canin", "Pedigree", "Hill's", "Blue Buffalo", "KONG", "PetSafe"],
            "Office Products": ["3M", "Staples", "HP", "Canon", "Epson", "Brother", "Fellowes", "Logitech"],
            "Music": ["Fender", "Gibson", "Yamaha", "Roland", "Shure", "Audio-Technica", "Pioneer"],
            "Movies": ["Disney", "Warner Bros", "Universal", "Sony Pictures", "Paramount", "20th Century Studios"],
            "Games": ["Nintendo", "Sony", "Microsoft", "EA", "Ubisoft", "Activision", "Rockstar Games"]
        }
        
        self.product_templates = {
            "Electronics": [
                "{brand} Smartphone {id}",
                "{brand} Laptop {id}",
                "{brand} Tablet {id}",
                "{brand} Smartwatch {id}",
                "{brand} Headphones {id}",
                "{brand} TV {id}",
                "{brand} Camera {id}",
                "{brand} Gaming Console {id}",
                "{brand} Wireless Earbuds {id}",
                "{brand} Smart Speaker {id}"
            ],
            "Fashion": [
                "{brand} T-Shirt {id}",
                "{brand} Jeans {id}",
                "{brand} Sneakers {id}",
                "{brand} Jacket {id}",
                "{brand} Dress {id}",
                "{brand} Hoodie {id}",
                "{brand} Sweater {id}",
                "{brand} Shorts {id}",
                "{brand} Skirt {id}",
                "{brand} Boots {id}"
            ],
            "Home & Garden": [
                "{brand} Sofa {id}",
                "{brand} Dining Table {id}",
                "{brand} Bed Frame {id}",
                "{brand} Garden Tools {id}",
                "{brand} Lighting {id}",
                "{brand} Kitchenware {id}",
                "{brand} Bathroom Set {id}",
                "{brand} Outdoor Furniture {id}",
                "{brand} Home Decor {id}",
                "{brand} Storage Solution {id}"
            ],
            "Books": [
                "{brand} Fiction Novel {id}",
                "{brand} Cookbook {id}",
                "{brand} Biography {id}",
                "{brand} Self-Help Book {id}",
                "{brand} Children's Book {id}",
                "{brand} Science Book {id}",
                "{brand} History Book {id}",
                "{brand} Business Book {id}",
                "{brand} Art Book {id}",
                "{brand} Educational Book {id}"
            ],
            "Sports": [
                "{brand} Running Shoes {id}",
                "{brand} Yoga Mat {id}",
                "{brand} Gym Bag {id}",
                "{brand} Sports Wear {id}",
                "{brand} Fitness Equipment {id}",
                "{brand} Basketball {id}",
                "{brand} Tennis Racket {id}",
                "{brand} Bicycle {id}",
                "{brand} Swimming Gear {id}",
                "{brand} Hiking Gear {id}"
            ],
            "Beauty": [
                "{brand} Lipstick {id}",
                "{brand} Foundation {id}",
                "{brand} Skincare Set {id}",
                "{brand} Perfume {id}",
                "{brand} Hair Care {id}",
                "{brand} Makeup Palette {id}",
                "{brand} Face Mask {id}",
                "{brand} Nail Polish {id}",
                "{brand} Beauty Tools {id}",
                "{brand} Body Lotion {id}"
            ],
            "Toys": [
                "{brand} Building Set {id}",
                "{brand} Board Game {id}",
                "{brand} Action Figure {id}",
                "{brand} Doll {id}",
                "{brand} Educational Toy {id}",
                "{brand} Remote Control Car {id}",
                "{brand} Puzzle {id}",
                "{brand} Arts & Crafts {id}",
                "{brand} Plush Toy {id}",
                "{brand} Outdoor Toy {id}"
            ],
            "Automotive": [
                "{brand} Car Parts {id}",
                "{brand} Motor Oil {id}",
                "{brand} Car Care Kit {id}",
                "{brand} Tires {id}",
                "{brand} Car Electronics {id}",
                "{brand} Tools Set {id}",
                "{brand} Car Accessories {id}",
                "{brand} Battery {id}",
                "{brand} Cleaning Products {id}",
                "{brand} Safety Equipment {id}"
            ],
            "Health": [
                "{brand} Vitamins {id}",
                "{brand} Supplements {id}",
                "{brand} First Aid Kit {id}",
                "{brand} Pain Relief {id}",
                "{brand} Wellness Products {id}",
                "{brand} Fitness Tracker {id}",
                "{brand} Health Monitor {id}",
                "{brand} Personal Care {id}",
                "{brand} Sleep Aid {id}",
                "{brand} Nutrition Products {id}"
            ],
            "Grocery": [
                "{brand} Snacks {id}",
                "{brand} Beverages {id}",
                "{brand} Breakfast Items {id}",
                "{brand} Canned Goods {id}",
                "{brand} Dairy Products {id}",
                "{brand} Baking Supplies {id}",
                "{brand} Condiments {id}",
                "{brand} Frozen Foods {id}",
                "{brand} Organic Products {id}",
                "{brand} Pantry Staples {id}"
            ],
            "Pet Supplies": [
                "{brand} Pet Food {id}",
                "{brand} Pet Toys {id}",
                "{brand} Pet Bed {id}",
                "{brand} Pet Carrier {id}",
                "{brand} Grooming Kit {id}",
                "{brand} Pet Treats {id}",
                "{brand} Pet Health {id}",
                "{brand} Pet Accessories {id}",
                "{brand} Pet Training {id}",
                "{brand} Pet Cleaning {id}"
            ],
            "Office Products": [
                "{brand} Printer {id}",
                "{brand} Office Chair {id}",
                "{brand} Desk {id}",
                "{brand} Stationery Set {id}",
                "{brand} Paper Products {id}",
                "{brand} Office Supplies {id}",
                "{brand} Filing System {id}",
                "{brand} Calculator {id}",
                "{brand} Shredder {id}",
                "{brand} Office Electronics {id}"
            ],
            "Music": [
                "{brand} Guitar {id}",
                "{brand} Piano {id}",
                "{brand} Drums {id}",
                "{brand} Microphone {id}",
                "{brand} Music Production {id}",
                "{brand} DJ Equipment {id}",
                "{brand} Studio Gear {id}",
                "{brand} Music Accessories {id}",
                "{brand} Sheet Music {id}",
                "{brand} Instrument Care {id}"
            ],
            "Movies": [
                "{brand} Action Movie {id}",
                "{brand} Comedy {id}",
                "{brand} Drama {id}",
                "{brand} Sci-Fi {id}",
                "{brand} Horror {id}",
                "{brand} Documentary {id}",
                "{brand} Animation {id}",
                "{brand} TV Series {id}",
                "{brand} Movie Collection {id}",
                "{brand} Special Edition {id}"
            ],
            "Games": [
                "{brand} Video Game {id}",
                "{brand} Gaming Console {id}",
                "{brand} Controller {id}",
                "{brand} Gaming Headset {id}",
                "{brand} Gaming Chair {id}",
                "{brand} Gaming Mouse {id}",
                "{brand} Gaming Keyboard {id}",
                "{brand} Gaming Monitor {id}",
                "{brand} Gaming Bundle {id}",
                "{brand} Gaming Accessories {id}"
            ]
        }

    def generate_product_name(self, category: str, brand: str) -> str:
        templates = self.product_templates.get(category, ["{brand} Product {id}"])
        return random.choice(templates).format(
            brand=brand,
            id=str(random.randint(100, 999))
        )

    def generate_description(self, category: str, brand: str, name: str) -> str:
        features = [
            "High quality", "Premium design", "Latest technology",
            "Best seller", "Customer favorite", "Award winning",
            "Innovative", "Eco-friendly", "Professional grade",
            "Limited edition", "Exclusive design", "Advanced features",
            "Energy efficient", "User friendly", "Ergonomic design",
            "Smart technology", "Sustainable", "Handcrafted",
            "Luxury finish", "Premium materials", "Enhanced performance",
            "Space saving", "Versatile", "Multi-functional"
        ]
        
        benefits = [
            "Perfect for everyday use",
            "Ideal for professionals",
            "Great for beginners",
            "Suitable for all skill levels",
            "Designed for maximum comfort",
            "Built to last",
            "Easy to maintain",
            "Excellent value for money",
            "Backed by warranty",
            "Includes free support"
        ]

        return f"{name} by {brand}. {random.choice(features)} product in {category} category. " \
               f"Features include {', '.join(random.sample(features, 3))}. {random.choice(benefits)}."

    def generate_bulk_data(self, num_users=100, num_products=1000, num_behaviors=5000) -> Dict:
        users = []
        products = []
        user_behaviors = []

        # Generate Users with unique emails
        used_emails = set()
        for i in range(num_users):
            joined_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            # Benzersiz e-posta oluştur
            while True:
                email = f"user_{i}_{random.randint(1000, 9999)}@example.com"
                if email not in used_emails:
                    used_emails.add(email)
                    break
            
            user = {
                "id": str(uuid.uuid4()),
                "name": f"User_{random.randint(1000, 9999)}",
                "email": email,
                "age": random.randint(18, 70),
                "joined_date": joined_date
            }
            users.append(user)

        # Generate Products
        for _ in range(num_products):
            category = random.choice(self.categories)
            brand = random.choice(self.brands[category])
            name = self.generate_product_name(category, brand)
            created_at = datetime.now() - timedelta(days=random.randint(1, 180))
            
            product = {
                "id": str(uuid.uuid4()),
                "name": name,
                "category": category,
                "brand": brand,
                "price": round(random.uniform(10, 1000), 2),
                "description": self.generate_description(category, brand, name),
                "rating": round(random.uniform(3.5, 5), 1),
                "stock": random.randint(0, 100),
                "created_at": created_at
            }
            products.append(product)

        # Generate User Behaviors
        actions = ["view", "cart", "purchase", "wishlist", "review"]
        for _ in range(num_behaviors):
            user = random.choice(users)
            product = random.choice(products)
            action = random.choice(actions)
            behavior_time = datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            behavior = {
                "id": str(uuid.uuid4()),
                "user_id": user["id"],
                "product_id": product["id"],
                "category": product["category"],  # Add the product's category
                "action": action,
                "timestamp": behavior_time
            }
            user_behaviors.append(behavior)

        return {
            "users": users,
            "products": products,
            "user_behaviors": user_behaviors
        }

    def generate_user_behavior(self, user_id: str, product_id: str) -> Dict:
        return {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "product_id": product_id,
            "category": random.choice(["Electronics", "Books", "Clothing", "Home", "Sports"]),  # Kategori ekledik
            "action": random.choice(["view", "purchase", "add_to_cart", "wishlist"]),
            "timestamp": datetime.utcnow()
        }
