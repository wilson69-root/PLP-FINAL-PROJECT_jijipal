import streamlit as st
from agent.core import get_city_guide, get_ai_summary
from agent.locations import fetch_places_osm
from agent.chat import chat_response
from agent.cache_manager import get_cached_city_guide, cache_places
from streamlit_chat import message
import time

st.set_page_config(page_title="Mtaa+ Dashboard", page_icon="🧭", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stTextInput input {
        border-radius: 10px;
    }
    .stSelectbox select {
        border-radius: 10px;
    }
    .stRadio input {
        border-radius: 10px;
    }
    .stButton button {
        border-radius: 10px;
    }
    .stMarkdown {
        font-size: 18px;
    }
    .stTabs {
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Survival Guide", "📍 Real-Time Places", "💬 Chat with MtaaBot", "🎟️ Bookings & Events"])

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
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2>🛡️ Your {goal} Plan for {city}</h2>
    </div>
    """.format(goal=goal, city=city), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if name and city and goal:
            ai_summary = get_ai_summary(city, budget, goal)
            st.info(ai_summary, icon="💡")
            
            # 🔄 Load cached or updated survival guide data
            guide = get_cached_city_guide(city, budget, goal)
            for tip in guide:
                st.markdown(f"✅ {tip}")
        else:
            st.warning("Please fill in your name, city and goal on the left to generate your survival plan.")

    with col2:
        st.markdown("### 📊 Budget Breakdown")
        st.progress(0.5, text="Daily Budget: KES {}".format(budget))

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
            "",
            ["restaurant", "supermarket", "hospital", "pharmacy", "bank", "atm", "bus_station", "fast_food"],
            index=0,
            help="Choose the type of service you're looking for"
        )
    
    with col2:
        if city:
            # ✅ Caching layer integration
            with st.spinner("Fetching locations..."):
                places = cache_places(city, tag, ttl=3600)  # cache for 1 hour
                if places:
                    for place in places:
                        st.markdown(f"📌 {place}")
                else:
                    st.info("No places found for this category in your area.", icon="🔍")
        else:
            st.warning("Please select a city in the sidebar.", icon="⚠️")

with tab3:
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

with tab4:
    # 🎟️ Bookings & Events Tab
    st.subheader("🎟️ Discover & Book Local Experiences")
    event_type = st.selectbox("🎭 What are you looking for?", ["Concerts", "Cultural Tours", "Workshops", "Meetups", "Nightlife"])
    st.info(f"✨ We'll soon let you book {event_type.lower()} in {city}! Stay tuned.")
    st.button("🔔 Notify Me When Live")

# Footer caption
with st.sidebar:
    st.markdown("---")
    st.caption("Powered by Mtaa+ — Kenya's survival assistant 🇰🇪")
