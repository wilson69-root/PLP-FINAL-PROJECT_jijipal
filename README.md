# MtaaAgentProject

A comprehensive Kenyan city survival assistant that helps users navigate, survive, explore, and relocate in Kenyan cities through intelligent data scraping, AI-powered recommendations, and personalized itinerary generation.

## 🏗️ Project Structure

```
MtaaAgentProject/
├── agent/
│   ├── __init__.py
│   ├── scraper.py              # All web scraping logic
│   ├── prompt_templates.py     # Prompt templates for HuggingFace model
│   ├── agent_runner.py         # Core class running agent tasks
│   ├── cache.py                # Caching scraped results (diskcache)
│   ├── itinerary.py            # Itinerary generation logic
│   └── [existing files...]     # Other existing agent files
│
├── models/
│   └── hf_model.py             # HuggingFace transformer interface
│
├── ui/
│   ├── style.css               # Custom Streamlit styling
│   └── components.py           # Shared UI components (cards, loaders)
│
├── cache/                      # Auto-generated cache directory
├── main.py                     # Main Streamlit entry point
├── example_usage.py            # Example usage demonstration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit App**
   ```bash
   streamlit run main.py
   ```

3. **Try the Example Script**
   ```bash
   python example_usage.py
   ```

## 🧩 Key Components

### AgentTaskRunner
The core orchestrator class that coordinates all agent functionality:

```python
from agent.agent_runner import AgentTaskRunner

runner = AgentTaskRunner(city="Nairobi", budget=50000, goal="Survive")
results = runner.run_all_tasks()
```

### HuggingFace Model Interface
AI-powered responses using transformer models:

```python
from models.hf_model import ask_model

response = ask_model("What are good areas to live in Nairobi?")
```

### Smart Caching
Persistent caching for scraped data:

```python
from agent.cache import cache_data, get_cached_data

cache_data("key", data, ttl=3600)  # Cache for 1 hour
cached = get_cached_data("key")
```

### Web Scraping
Unified scraping interface:

```python
from agent.scraper import scrape_rentals, scrape_food

rentals = scrape_rentals("Nairobi")
food_options = scrape_food("Nairobi")
```

## 🎯 Features

- **🏠 Housing Search**: Find rentals within budget with filtering
- **🍽️ Food Discovery**: Locate restaurants and food options
- **🚌 Transport Info**: Get matatu routes and fare information
- **🎯 Entertainment**: Discover chill spots and activities
- **📅 Itinerary Generation**: AI-powered day-by-day planning
- **💰 Budget Analysis**: Smart budget breakdown and recommendations
- **🛡️ Survival Tips**: Context-aware survival guidance
- **💬 AI Chat**: Interactive assistance with MtaaBot
- **💾 Smart Caching**: Efficient data storage and retrieval

## 🔧 Configuration

### Model Configuration
Edit `models/hf_model.py` to change the AI model:

```python
DEFAULT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
FALLBACK_MODEL = "microsoft/DialoGPT-medium"
```

### Scraping Configuration
Customize scrapers in `agent/scraper.py` for real data sources:

```python
def scrape_rentals(city):
    # Replace with actual scraping logic
    # Use BeautifulSoup, Playwright, etc.
    pass
```

### UI Customization
Modify `ui/style.css` for custom styling and `ui/components.py` for new components.

## 📊 Usage Examples

### Basic Usage
```python
from agent.agent_runner import AgentTaskRunner

# Initialize for Nairobi with 50k budget
runner = AgentTaskRunner("Nairobi", 50000, "Survive")

# Get specific data
rentals = runner.get_rentals()
food_options = runner.get_food()
budget_breakdown = runner.get_budget_breakdown()

# Run comprehensive analysis
all_results = runner.run_all_tasks()
```

### AI Interaction
```python
from models.hf_model import ask_model

# Get AI recommendations
response = ask_model(
    "Recommend budget accommodation in Nairobi for KES 15,000",
    max_new_tokens=200
)
```

### Custom Itinerary
```python
from agent.itinerary import generate_itinerary

itinerary = generate_itinerary(
    city="Nairobi",
    budget=30000,
    goal="Explore",
    duration=7,
    preferences="cultural sites, local food"
)
```

## 🛠️ Development

### Adding New Scrapers
1. Create scraping function in `agent/scraper.py`
2. Add caching logic using `agent/cache.py`
3. Integrate with `AgentTaskRunner` in `agent/agent_runner.py`

### Adding New UI Components
1. Create component in `ui/components.py`
2. Add styling in `ui/style.css`
3. Use in `main.py` Streamlit app

### Adding New AI Prompts
1. Define templates in `agent/prompt_templates.py`
2. Create formatting functions
3. Use with `models/hf_model.py`

## 📋 Dependencies

Core dependencies include:
- `streamlit` - Web interface
- `transformers` - AI model interface
- `beautifulsoup4` - Web scraping
- `playwright` - Dynamic content scraping
- `diskcache` - Persistent caching
- `requests` - HTTP requests
- `huggingface_hub` - Model management

## 🚀 Future Enhancements

- Real-time data scraping from Kenyan websites
- Integration with local APIs (matatu routes, housing platforms)
- User authentication and personalized profiles
- Mobile app development
- Multi-language support (Swahili, local languages)
- Integration with payment systems for bookings
- Offline functionality for essential information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.
