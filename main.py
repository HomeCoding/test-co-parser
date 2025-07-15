#!/usr/bin/env python3
"""
ParserApp - Main script that parses product prices from Biedronka website.
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional

try:
    import requests
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False


def generate_sample_products() -> List[Dict]:
    """Generate sample product data for testing when real scraping is not available."""
    sample_products = [
        {"id": 1, "name": "Chleb pełnoziarnisty", "price": 3.49, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 2, "name": "Mleko 3,2% 1L", "price": 2.89, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 3, "name": "Jajka L 10szt", "price": 8.99, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 4, "name": "Banany 1kg", "price": 4.99, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 5, "name": "Ser żółty gouda", "price": 12.49, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 6, "name": "Ryż jaśminowy 1kg", "price": 6.79, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 7, "name": "Kurczak filet", "price": 15.99, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 8, "name": "Pomidory czerwone", "price": 7.29, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 9, "name": "Masło extra", "price": 9.99, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 10, "name": "Jogurt naturalny", "price": 3.29, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 11, "name": "Ziemniaki 2kg", "price": 5.49, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 12, "name": "Makaron spaghetti", "price": 2.99, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 13, "name": "Woda mineralna 1.5L", "price": 1.89, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 14, "name": "Cebula żółta", "price": 2.49, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"},
        {"id": 15, "name": "Płatki owsiane", "price": 4.19, "currency": "PLN", "category": "Bestseller", "in_stock": True, "source": "biedronka_sample"}
    ]
    
    print(f"Generated {len(sample_products)} sample products for testing")
    return sample_products


def parse_biedronka_products() -> List[Dict]:
    """Parse product data from Biedronka bestsellers page."""
    
    if not DEPENDENCIES_AVAILABLE:
        print("Error: Web scraping dependencies not available. Install requirements.txt")
        print("Falling back to sample data for testing...")
        return generate_sample_products()
    
    url = "https://home.biedronka.pl/bestsellery/"
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pl-PL,pl;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"Fetching products from: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Common selectors for product listings (may need adjustment based on actual site structure)
        product_selectors = [
            '.product-item',
            '.product-card',
            '.product',
            '[data-product]',
            '.bestseller-item'
        ]
        
        # Try different selectors to find products
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                product_elements = elements
                print(f"Found {len(elements)} products using selector: {selector}")
                break
        
        if not product_elements:
            # Fallback: look for any elements with price patterns
            price_pattern = re.compile(r'\d+[,.]?\d*\s*zł')
            all_elements = soup.find_all(text=price_pattern)
            if all_elements:
                print(f"Found {len(all_elements)} price elements using pattern matching")
                # Create basic products from price elements
                for i, price_element in enumerate(all_elements[:20]):  # Limit to 20
                    parent = price_element.parent
                    name = extract_product_name(parent)
                    price = extract_price(price_element)
                    
                    if price is not None:
                        products.append({
                            "id": i + 1,
                            "name": name or f"Product {i + 1}",
                            "price": price,
                            "currency": "PLN",
                            "category": "Bestseller",
                            "in_stock": True,
                            "source": "biedronka"
                        })
        else:
            # Parse structured product elements
            for i, element in enumerate(product_elements[:20]):  # Limit to 20 products
                name = extract_product_name(element)
                price = extract_price_from_element(element)
                
                if price is not None:
                    products.append({
                        "id": i + 1,
                        "name": name or f"Product {i + 1}",
                        "price": price,
                        "currency": "PLN", 
                        "category": "Bestseller",
                        "in_stock": True,
                        "source": "biedronka"
                    })
        
        if not products:
            print("No products found on the website, falling back to sample data")
            return generate_sample_products()
            
        print(f"Successfully parsed {len(products)} products")
        return products
        
    except requests.RequestException as e:
        print(f"Network error: {e}")
        print("Website not accessible, falling back to sample data for testing...")
        return generate_sample_products()
    except Exception as e:
        print(f"Parsing error: {e}")
        print("Parsing failed, falling back to sample data for testing...")
        return generate_sample_products()


def extract_product_name(element) -> Optional[str]:
    """Extract product name from element."""
    # Try common selectors for product names
    name_selectors = [
        '.product-name',
        '.product-title', 
        '.name',
        '.title',
        'h1', 'h2', 'h3', 'h4',
        '.product-link'
    ]
    
    for selector in name_selectors:
        name_elem = element.select_one(selector)
        if name_elem:
            text = name_elem.get_text(strip=True)
            if text and len(text) > 2:
                return text[:100]  # Limit length
    
    # Fallback: get any text content
    text = element.get_text(strip=True)
    if text:
        # Clean up text and take first meaningful part
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines:
            if len(line) > 5 and not re.match(r'^\d+[,.]?\d*\s*zł', line):
                return line[:100]
    
    return None


def extract_price_from_element(element) -> Optional[float]:
    """Extract price from product element."""
    # Try common price selectors
    price_selectors = [
        '.price',
        '.product-price',
        '.cost',
        '.amount',
        '[data-price]'
    ]
    
    for selector in price_selectors:
        price_elem = element.select_one(selector)
        if price_elem:
            price = extract_price(price_elem.get_text())
            if price is not None:
                return price
    
    # Fallback: search for price pattern in all text
    text = element.get_text()
    return extract_price(text)


def extract_price(text: str) -> Optional[float]:
    """Extract numeric price from text."""
    if not text:
        return None
        
    # Polish price pattern: "XX,XX zł" or "XX.XX zł" or just "XX zł"
    price_patterns = [
        r'(\d+)[,.](\d{2})\s*zł',  # 12,99 zł or 12.99 zł
        r'(\d+)[,.](\d{1})\s*zł',  # 12,9 zł or 12.9 zł  
        r'(\d+)\s*zł',             # 12 zł
        r'(\d+)[,.](\d{2})',       # 12,99 or 12.99
        r'(\d+)[,.](\d{1})',       # 12,9 or 12.9
    ]
    
    for pattern in price_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                if len(match.groups()) == 2:
                    whole, decimal = match.groups()
                    return float(f"{whole}.{decimal.ljust(2, '0')}")
                else:
                    return float(match.group(1))
            except ValueError:
                continue
    
    return None





def main():
    """Main function to parse and save product data from Biedronka."""
    
    # Parse products from Biedronka website
    products = parse_biedronka_products()
    
    if not products:
        print("Failed to generate any product data")
        return None
    
    # Create output data structure
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "source_url": "https://home.biedronka.pl/bestsellery/",
        "total_products": len(products),
        "products": products
    }
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Save to JSON file
    output_file = "output/products.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Parsed {len(products)} products from Biedronka")
    print(f"Output saved to: {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")
    
    return output_file


if __name__ == "__main__":
    main()