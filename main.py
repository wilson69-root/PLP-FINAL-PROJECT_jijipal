import streamlit as st
from agent.agent_runner import AgentTaskRunner
from models.hf_model import ask_model, check_model_status
from agent.chat import chat_response
from agent.cache import get_cached_data, cache_data
from ui.components import (
    apply_custom_css, render_card, render_data_list, 
    render_budget_breakdown, render_metric_cards, 
    render_itinerary_card, render_city_summary,
    render_emergency_info, render_tips_section
)
from streamlit_chat import message
import time

st.set_page_config(page_title="Mtaa+ Dashboard", page_icon="🧭", layout="wide")

# Apply custom CSS styling
apply_custom_css()

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Survival Guide", "📍 Real-Time Places", "🤖 Full Agent Report", "💬 Chat with MtaaBot", "🎟️ Bookings & Events"])

# Sidebar - User Profile
with st.sidebar:
    st.image("https://raw.githubusercontent.com/streamlit/streamlit/main/docs/_static/images/logo.png", width=100)
    st.title("🧭 Mtaa+ Navigator")
    
    # User Profile Section
    st.subheader("👤 Your Profile")
    name = st.text_input("", "", placeholder="Enter your name...")
    
    # Location Section
    st.subheader("📍 Your Location")
    city = st.selectbox(
        "",
        ["Nairobi", "Kisumu", "Mombasa", "Eldoret"],
        index=0,
        help="Select your current city"
    )
    
    # Goal Section
    st.subheader("🎯 Your Goal")
    goal = st.radio(
        "",
        ["Survive", "Explore", "Relocate"],
        index=0,
        help="Choose your main objective"
    )
    
    # Budget Section
    st.subheader("💰 Your Budget")
    budget_type = st.radio("💸 Budget Type", ["Daily", "Monthly"], index=1)
    raw_budget = st.text_input("💰 Your Budget in KES", value="50000")

    try:
        budget = int(raw_budget)
        if budget_type == "Daily":
            budget *= 30  # Convert daily to monthly
    except ValueError:
        st.warning("Please enter a valid number for budget.")
        budget = 50000

with tab1:
    # Survival Guide Tab
    st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <h2>🛡️ Your {goal} Plan for {city}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if name and city and goal:
            # Initialize agent runner
            runner = AgentTaskRunner(city, budget, goal)
            
            # Get AI summary using the new model
            try:
                summary_prompt = f"Provide a brief survival summary for someone in {city}, Kenya with a budget of KES {budget} and goal: {goal}"
                ai_summary = ask_model(summary_prompt, max_new_tokens=200)
                render_card("💡 AI Insights", ai_summary, "info", "🤖")
            except Exception as e:
                st.warning(f"AI model unavailable: {e}")
                ai_summary = f"Welcome to {city}! With your {goal.lower()} goal and KES {budget:,} budget, focus on securing accommodation, finding affordable food options, and establishing reliable transport routes."
                render_card("💡 Getting Started", ai_summary, "info", "🏁")
            
            # Get survival tips using the agent runner
            with st.spinner("Generating survival guide..."):
                try:
                    survival_tips = runner.get_survival_tips()
                    render_tips_section(survival_tips, "🛡️ Essential Survival Tips")
                except Exception as e:
                    st.error(f"Error generating survival tips: {e}")
        else:
            st.warning("Please fill in your name, city and goal on the left to generate your survival plan.")

    with col2:
        if name and city and goal:
            # Budget breakdown using agent runner
            try:
                runner = AgentTaskRunner(city, budget, goal)
                budget_breakdown = runner.get_budget_breakdown()
                render_budget_breakdown(budget_breakdown)
            except Exception as e:
                st.error(f"Error creating budget breakdown: {e}")
                st.markdown("### 📊 Budget Overview")
                st.progress(0.5, text=f"Daily Budget: KES {budget//30}")
        else:
            st.markdown("### 📊 Budget Overview")
            st.info("Fill in your details to see budget breakdown")

with tab2:
    # 📍 Real-Time Places Tab
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2>📍 Find Services Near You</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        tag = st.selectbox(
            "Service Type",
            ["restaurant", "supermarket", "hospital", "pharmacy", "bank", "atm", "bus_station", "fast_food"],
            index=0,
            help="Choose the type of service you're looking for"
        )
        
        if st.button("🔄 Refresh Data"):
            # Clear cache for this city and tag
            cache_key = f"places_{city.lower()}_{tag}"
            st.rerun()
    
    with col2:
        if city:
            # Use agent runner to get places data
            with st.spinner("Fetching locations..."):
                try:
                    runner = AgentTaskRunner(city, budget, goal)
                    places = runner.get_chill() if tag in ['restaurant', 'fast_food'] else []
                    
                    # For other services, use a mock response (would be real scraping in production)
                    if tag not in ['restaurant', 'fast_food']:
                        places = [
                            f"{tag.title()} in {city} - Location 1",
                            f"{tag.title()} in {city} - Location 2", 
                            f"{tag.title()} in {city} - Location 3",
                            f"24/7 {tag.title()} service in {city}",
                            f"Popular {tag.title()} near {city} center"
                        ]
                    
                    if places:
                        render_data_list(places, f"📍 {tag.title()} Options in {city}")
                    else:
                        st.info("No places found for this category in your area.", icon="🔍")
                        
                except Exception as e:
                    st.error(f"Error fetching places: {e}")
        else:
            st.warning("Please select a city in the sidebar.", icon="⚠️")

with tab3:
    # 🤖 Full Agent Report Tab - New comprehensive report
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2>🤖 Complete Mtaa Agent Analysis</h2>
        <p>Comprehensive data gathering and itinerary generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    if name and city and goal:
        if st.button("🚀 Run Complete Agent Analysis", type="primary"):
            with st.spinner("Running comprehensive analysis... This may take a moment."):
                try:
                    # Initialize agent runner
                    runner = AgentTaskRunner(city, budget, goal)
                    
                    # Run all tasks
                    results = runner.run_all_tasks()
                    
                    # Display results
                    if "error" not in results:
                        # City summary
                        render_city_summary(runner.get_summary_report())
                        
                        # Create columns for organized display
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Rentals
                            if results.get('rentals'):
                                render_data_list(results['rentals'][:5], "🏠 Housing Options")
                            
                            # Food options
                            if results.get('food'):
                                render_data_list(results['food'][:5], "🍽️ Food & Dining")
                        
                        with col2:
                            # Transport
                            if results.get('transport'):
                                render_data_list(results['transport'][:5], "🚌 Transportation")
                            
                            # Chill spots
                            if results.get('chill_spots'):
                                render_data_list(results['chill_spots'][:5], "🎯 Places to Visit")
                        
                        # Itinerary
                        st.markdown("### 📅 Generated Itinerary")
                        itinerary = results.get('itinerary')
                        
                        if isinstance(itinerary, dict) and 'days' in itinerary:
                            for day_data in itinerary['days'][:3]:  # Show first 3 days
                                render_itinerary_card(day_data)
                        else:
                            # If it's a string response from AI
                            render_card("📋 Your Itinerary", str(itinerary), "info", "📅")
                        
                        # Emergency info
                        render_emergency_info(city)
                        
                        # Execution info
                        metadata = results.get('metadata', {})
                        execution_time = metadata.get('execution_time', 0)
                        st.success(f"✅ Analysis completed in {execution_time:.2f} seconds")
                        
                    else:
                        st.error(f"Error running analysis: {results.get('error')}")
                        
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
                    st.info("Please try again or check your internet connection.")
    else:
        st.warning("Please fill in your details in the sidebar to run the complete analysis.")
        render_card(
            "ℹ️ How it works", 
            "The Full Agent Analysis runs all scraping tasks, generates personalized recommendations, creates an itinerary, and provides emergency information for your selected city and budget.",
            "info"
        )

with tab4:
    # 💬 Chat with MtaaBot Tab
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2>💬 Chat with MtaaBot</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        personality = st.selectbox(
            "🧠 Choose Bot Style",
            ["💡 Practical", "😊 Friendly", "🧘 Calm"],
            index=0,
            help="Choose how you'd like MtaaBot to respond"
        )
        
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
    
    with col2:
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("What would you like to ask MtaaBot?"):
            # Add user message to chat
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Thinking..."):
                    response = chat_response(
                        user_input=prompt,
                        personality=personality,
                        context_city=city,
                        context_goal=goal,
                        context_budget=budget
                    )
                message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with tab5:
    # 🎟️ Bookings & Events Tab
    st.subheader("🎟️ Discover & Book Local Experiences")
    event_type = st.selectbox("🎭 What are you looking for?", ["Concerts", "Cultural Tours", "Workshops", "Meetups", "Nightlife"])
    st.info(f"✨ We'll soon let you book {event_type.lower()} in {city}! Stay tuned.")
    st.button("🔔 Notify Me When Live")

# Footer caption
with st.sidebar:
    st.markdown("---")
    st.caption("Powered by Mtaa+ — Kenya's survival assistant 🇰🇪")
