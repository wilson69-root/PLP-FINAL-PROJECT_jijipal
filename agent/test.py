import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
import requests
import json
from scrapers import scrape_numbeo_specific  # Assumes the scraper is in numbeo_specific_scraper.py

class TestNumbeoScraper(unittest.TestCase):
    def setUp(self):
        # Expected items for validation
        self.expected_items = {
            "rent": [
                "Apartment (1 bedroom) in City Centre",
                "Apartment (1 bedroom) Outside of Centre"
            ],
            "food": [
                "Meal, Inexpensive Restaurant",
                "Rice (white), (1kg)"
            ],
            "water": [
                "Water (1.5 liter bottle)"
            ],
            "transport": [
                "One-way Ticket (Local Transport)",
                "Monthly Pass (Regular Price)"
            ]
        }

    @patch('requests.get')
    def test_scrape_numbeo_specific_mock(self, mock_get):
        # Mock HTML content for Numbeo's Nairobi page
        mock_html = """
        <table class="data_wide_table">
            <tr><th>Item</th><th>Price</th><th>Range</th></tr>
            <tr><td>Apartment (1 bedroom) in City Centre</td><td>30,000.00 KES</td><td>25,000-25,000</td></tr>
            <tr><td>Apartment (1 bedroom) Outside of Centre</td><td>18,000.00 KES</td><td>15,000-20,000</td></tr>
            <tr><td>Meal, Inexpensive Restaurant</td><td>350.00 KES</td><td>200-500</td></tr>
            <tr><td>Rice (white), (1kg)</td><td>150.00 KES</td><td>100-200</td></tr>
            <tr><td>Water (1.5 liter bottle)</td><td>80.00 KES</td><td>50-100</td></tr>
            <tr><td>One-way Ticket (Local Transport)</td><td>50.00 KES</td><td>40-60</td></tr>
            <tr><td>Monthly Pass (Regular Price)</td><td>3,000.00 KES</td><td>2,500-3,500</td></tr>
        </table>
        """
        
        # Mock the requests.get response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = mock_html.encode()
        mock_response.raise_for_status = lambda: None
        
        # Run the scraper
        result = scrape_numbeo_specific("Nairobi")
        
        # Verify the result is a dictionary
        self.assertIsInstance(result, dict, "Scraper should return a dictionary")
        
        # Verify all expected categories are present
        self.assertEqual(set(result.keys()), set(self.expected_items.keys()), "All categories should be present")
        
        # Verify the number of items in each category
        for category, items in self.expected_items.items():
            self.assertEqual(len(result[category]), len(items), f"{category} should have {len(items)} items")
            
            # Verify item names and price format
            for item, expected_item in zip(result[category], items):
                self.assertIn(expected_item, item, f"Item {expected_item} should be in {category}")
                self.assertTrue(item.startswith(f"{expected_item}: ~"), f"Item {item} should start with '{expected_item}: ~'")
                self.assertTrue(item.endswith("KES"), f"Item {item} should end with 'KES'")
    
    def test_scrape_numbeo_specific_live(self):
        # Note: Use this test sparingly to avoid overloading Numbeo's servers
        result = scrape_numbeo_specific("Nairobi")
        
        # Check if the result is a dictionary (or error message)
        self.assertIsInstance(result, dict, "Live scrape should return a dictionary")
        
        # Verify categories
        self.assertEqual(set(result.keys()), set(self.expected_items.keys()), "All categories should be present")
        
        # Verify the number of items in each category
        for category, items in self.expected_items.items():
            self.assertEqual(len(result[category]), len(items), f"{category} should have {len(items)} items")
            
            # Verify item names and price format (using KSh for live data)
            for item, expected_item in zip(result[category], items):
                self.assertIn(expected_item, item, f"Item {expected_item} should be in {category}")
                self.assertTrue(item.startswith(f"{expected_item}: ~"), f"Item {item} should start with '{expected_item}: ~'")
                self.assertTrue(item.endswith("KSh"), f"Item {item} should end with 'KSh'")

if __name__ == '__main__':
    unittest.main()