"""
Core class running agent tasks for the Mtaa Agent Project.
This is the main orchestrator that coordinates all agent functionality.
"""

from agent.scraper import scrape_rentals, scrape_food, scrape_places, scrape_bus_fares
from agent.itinerary import generate_itinerary
from agent.cache import get_cached_data, cache_data
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentTaskRunner:
    """
    Main class that orchestrates all agent tasks including scraping, 
    data processing, and itinerary generation.
    """
    
    def __init__(self, city, budget, goal="Survive"):
        self.city = city
        self.budget = budget
        self.goal = goal
        self.data_cache = {}
        
        logger.info(f"Initialized AgentTaskRunner for {city} with budget KES {budget}, goal: {goal}")
    
    def run_all_tasks(self):
        """
        Run all agent tasks and return consolidated results.
        This is the main method that orchestrates everything.
        """
        logger.info(f"Starting all tasks for {self.city}")
        
        start_time = time.time()
        
        try:
            results = {
                "rentals": self.get_rentals(),
                "food": self.get_food(),
                "chill_spots": self.get_chill(),
                "transport": self.get_transport(),
                "itinerary": self.generate_itinerary(),
                "metadata": {
                    "city": self.city,
                    "budget": self.budget,
                    "goal": self.goal,
                    "execution_time": time.time() - start_time,
                    "timestamp": time.time()
                }
            }
            
            logger.info(f"Completed all tasks in {results['metadata']['execution_time']:.2f} seconds")
            return results
            
        except Exception as e:
            logger.error(f"Error running tasks: {e}")
            return {
                "error": str(e),
                "city": self.city,
                "budget": self.budget,
                "goal": self.goal
            }
    
    def get_rentals(self):
        """Get rental information for the city."""
        logger.info(f"Fetching rentals for {self.city}")
        
        try:
            rentals = scrape_rentals(self.city)
            
            # Filter by budget if possible
            filtered_rentals = self._filter_rentals_by_budget(rentals)
            
            self.data_cache['rentals'] = filtered_rentals
            return filtered_rentals
            
        except Exception as e:
            logger.error(f"Error getting rentals: {e}")
            return [f"Error fetching rentals for {self.city}: {str(e)}"]
    
    def get_food(self):
        """Get food and restaurant information for the city."""
        logger.info(f"Fetching food options for {self.city}")
        
        try:
            food_options = scrape_food(self.city)
            self.data_cache['food'] = food_options
            return food_options
            
        except Exception as e:
            logger.error(f"Error getting food options: {e}")
            return [f"Error fetching food options for {self.city}: {str(e)}"]
    
    def get_chill(self):
        """Get chill spots and entertainment places for the city."""
        logger.info(f"Fetching chill spots for {self.city}")
        
        try:
            chill_spots = scrape_places(self.city, "chill")
            self.data_cache['chill_spots'] = chill_spots
            return chill_spots
            
        except Exception as e:
            logger.error(f"Error getting chill spots: {e}")
            return [f"Error fetching chill spots for {self.city}: {str(e)}"]
    
    def get_transport(self):
        """Get transportation and fare information for the city."""
        logger.info(f"Fetching transport info for {self.city}")
        
        try:
            transport_info = scrape_bus_fares(self.city)
            self.data_cache['transport'] = transport_info
            return transport_info
            
        except Exception as e:
            logger.error(f"Error getting transport info: {e}")
            return [f"Error fetching transport info for {self.city}: {str(e)}"]
    
    def generate_itinerary(self):
        """Generate a personalized itinerary based on collected data."""
        logger.info(f"Generating itinerary for {self.city}")
        
        try:
            # Ensure we have all the data
            if not self.data_cache:
                logger.warning("No cached data available, running basic tasks first")
                self.get_rentals()
                self.get_food()
                self.get_chill()
                self.get_transport()
            
            itinerary = generate_itinerary(
                city=self.city, 
                budget=self.budget,
                goal=self.goal,
                data=self.data_cache
            )
            return itinerary
            
        except Exception as e:
            logger.error(f"Error generating itinerary: {e}")
            return f"Error generating itinerary for {self.city}: {str(e)}"
    
    def get_survival_tips(self):
        """Get survival tips specific to the city and budget."""
        logger.info(f"Getting survival tips for {self.city}")
        
        cache_key = f"survival_tips_{self.city.lower()}_{self.budget}_{self.goal}"
        cached_tips = get_cached_data(cache_key)
        
        if cached_tips:
            return cached_tips
        
        # Generate survival tips based on collected data
        tips = self._generate_survival_tips()
        
        # Cache the tips
        cache_data(cache_key, tips, ttl=3600*24)  # Cache for 24 hours
        
        return tips
    
    def get_budget_breakdown(self):
        """Get a detailed budget breakdown for the city."""
        logger.info(f"Creating budget breakdown for {self.city}")
        
        breakdown = {
            "total_budget": self.budget,
            "currency": "KES",
            "city": self.city,
            "estimated_expenses": self._calculate_estimated_expenses(),
            "savings_tips": self._get_budget_saving_tips(),
            "budget_feasibility": self._assess_budget_feasibility()
        }
        
        return breakdown
    
    def _filter_rentals_by_budget(self, rentals):
        """Filter rental options based on budget (assuming 30% of budget for rent)."""
        max_rent = self.budget * 0.3  # 30% of budget for rent
        
        filtered = []
        for rental in rentals:
            # Simple parsing to extract price (this would be more sophisticated in real implementation)
            if "KES" in rental:
                try:
                    # Extract number after KES
                    price_str = rental.split("KES")[1].split("/")[0].strip()
                    price = int(price_str.replace(",", ""))
                    
                    if price <= max_rent:
                        filtered.append(f"{rental} ✅ (Within budget)")
                    else:
                        filtered.append(f"{rental} ⚠️ (Above recommended budget)")
                except:
                    filtered.append(rental)  # Include if we can't parse price
            else:
                filtered.append(rental)
        
        return filtered
    
    def _generate_survival_tips(self):
        """Generate survival tips based on city and budget."""
        base_tips = [
            f"Start with temporary accommodation while you search for permanent housing in {self.city}",
            f"Join local WhatsApp groups and Facebook communities for {self.city} residents",
            f"Learn basic Swahili phrases - it helps with negotiations and daily interactions",
            f"Always carry cash - many places in {self.city} don't accept cards",
            f"Use matatus for cheaper transport, but verify routes with locals first"
        ]
        
        # Add budget-specific tips
        if self.budget < 30000:
            base_tips.extend([
                "Consider shared accommodation to reduce costs",
                "Cook at home instead of eating out frequently",
                "Use boda bodas sparingly - walk short distances to save money"
            ])
        elif self.budget > 80000:
            base_tips.extend([
                "You can afford better neighborhoods - research safer areas",
                "Consider getting a car or using ride-hailing apps regularly",
                "Explore higher-end restaurants and entertainment options"
            ])
        
        return base_tips
    
    def _calculate_estimated_expenses(self):
        """Calculate estimated monthly expenses breakdown."""
        return {
            "rent": int(self.budget * 0.3),  # 30% for rent
            "food": int(self.budget * 0.25),  # 25% for food
            "transport": int(self.budget * 0.15),  # 15% for transport
            "utilities": int(self.budget * 0.10),  # 10% for utilities
            "entertainment": int(self.budget * 0.10),  # 10% for entertainment
            "savings": int(self.budget * 0.10)  # 10% for savings
        }
    
    def _get_budget_saving_tips(self):
        """Get money-saving tips for the specific city."""
        return [
            f"Shop at local markets in {self.city} for cheaper fresh produce",
            f"Use matatu routes instead of taxis when possible in {self.city}",
            f"Cook meals at home - eating out frequently can consume 40% of your budget",
            f"Join local community groups to find discounts and deals in {self.city}",
            f"Consider buying second-hand items for non-essential purchases"
        ]
    
    def _assess_budget_feasibility(self):
        """Assess if the budget is realistic for the city."""
        # Basic assessment logic (would be more sophisticated with real data)
        if self.budget < 20000:
            return "Tight budget - will require careful planning and shared accommodation"
        elif self.budget < 50000:
            return "Moderate budget - comfortable living with some constraints"
        else:
            return "Comfortable budget - good living standards achievable"
    
    def refresh_data(self):
        """Refresh all cached data by running scraping tasks again."""
        logger.info("Refreshing all data...")
        self.data_cache.clear()
        return self.run_all_tasks()
    
    def get_summary_report(self):
        """Get a comprehensive summary report."""
        if not self.data_cache:
            self.run_all_tasks()
        
        return {
            "city": self.city,
            "budget": self.budget,
            "goal": self.goal,
            "data_summary": {
                "rentals_found": len(self.data_cache.get('rentals', [])),
                "food_options": len(self.data_cache.get('food', [])),
                "chill_spots": len(self.data_cache.get('chill_spots', [])),
                "transport_options": len(self.data_cache.get('transport', []))
            },
            "recommendations": {
                "budget_breakdown": self.get_budget_breakdown(),
                "survival_tips": self.get_survival_tips()
            }
        }