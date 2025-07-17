import unittest
from agent.scrapers import scrape_meal_prices

class TestScrapeMealPrices(unittest.TestCase):
    def test_scrape_meal_prices_returns_list(self):
        # Test with a known city
        city = "Nairobi"
        result = scrape_meal_prices(city)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        # At least one tip should mention a price or food-related keyword
        self.assertTrue(any(any(word in tip.lower() for word in ["meal", "food", "water", "groceries", "milk", "rice"]) for tip in result))

    def test_scrape_meal_prices_invalid_city(self):
        # Test with a non-existent city
        city = "FakeCity123"
        result = scrape_meal_prices(city)
        self.assertIsInstance(result, list)
        self.assertTrue(any("no food prices found" in tip.lower() or "failed to scrape" in tip.lower() for tip in result))

if __name__ == "__main__":
    unittest.main()
