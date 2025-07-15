#!/usr/bin/env python3
"""
ParserApp - Main script that generates stub JSON with fake products and prices.
"""

import json
import random
import os
from datetime import datetime


def generate_fake_products(count=10):
    """Generate fake product data with names and prices."""
    
    # Sample product names and categories
    product_names = [
        "Laptop", "Mouse", "Keyboard", "Monitor", "Phone", "Tablet", 
        "Headphones", "Speaker", "Camera", "Printer", "Router", "Cable",
        "Charger", "Case", "Stand", "Dock", "Drive", "Memory", "Processor", "Graphics Card"
    ]
    
    brands = ["TechCorp", "DigiTech", "ElectroMax", "SmartDevices", "ProGear"]
    
    products = []
    
    for i in range(count):
        product = {
            "id": i + 1,
            "name": f"{random.choice(brands)} {random.choice(product_names)}",
            "price": round(random.uniform(10.99, 999.99), 2),
            "currency": "USD",
            "category": random.choice(["Electronics", "Computers", "Accessories", "Mobile", "Audio"]),
            "in_stock": random.choice([True, False]),
            "rating": round(random.uniform(1.0, 5.0), 1)
        }
        products.append(product)
    
    return products


def main():
    """Main function to generate and save product data."""
    
    # Generate fake products
    products = generate_fake_products(15)
    
    # Create output data structure
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "total_products": len(products),
        "products": products
    }
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Save to JSON file
    output_file = "output/products.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(products)} fake products")
    print(f"Output saved to: {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")
    
    return output_file


if __name__ == "__main__":
    main()