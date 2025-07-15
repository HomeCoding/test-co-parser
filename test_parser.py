#!/usr/bin/env python3
"""
Simple tests for the parser functionality.
"""

import sys
import os

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(__file__))

from main import extract_price, generate_fallback_products


def test_price_extraction():
    """Test price extraction from various text formats."""
    
    test_cases = [
        ("12,99 zł", 12.99),
        ("5.49 zł", 5.49),
        ("100 zł", 100.0),
        ("3,5 zł", 3.50),
        ("Produkt kosztuje 15,99 zł na wyprzedaży", 15.99),
        ("Cena: 7.25", 7.25),
        ("", None),
        ("brak ceny", None),
        ("29,99", 29.99),
    ]
    
    print("Testing price extraction...")
    
    for text, expected in test_cases:
        result = extract_price(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' -> {result} (expected: {expected})")
        
        if result != expected:
            return False
    
    return True


def test_fallback_products():
    """Test fallback product generation."""
    
    print("\nTesting fallback products...")
    
    products = generate_fallback_products()
    
    # Basic validation
    assert len(products) > 0, "Should generate at least one product"
    assert all('name' in p for p in products), "All products should have names"
    assert all('price' in p for p in products), "All products should have prices"
    assert all('currency' in p for p in products), "All products should have currency"
    assert all(p['currency'] == 'PLN' for p in products), "All products should use PLN currency"
    assert all(isinstance(p['price'], (int, float)) for p in products), "All prices should be numeric"
    
    print(f"✓ Generated {len(products)} fallback products")
    print(f"✓ Sample product: {products[0]['name']} - {products[0]['price']} {products[0]['currency']}")
    
    return True


def main():
    """Run all tests."""
    
    print("Running parser tests...\n")
    
    try:
        success = True
        success &= test_price_extraction()
        success &= test_fallback_products()
        
        if success:
            print("\n✓ All tests passed!")
            return 0
        else:
            print("\n✗ Some tests failed!")
            return 1
            
    except Exception as e:
        print(f"\n✗ Test error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())