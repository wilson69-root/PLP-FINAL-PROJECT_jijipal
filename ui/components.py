"""
Shared UI components for the Mtaa Agent Project Streamlit app.
Reusable components for cards, loaders, metrics, etc.
"""

import streamlit as st
import time
from typing import List, Dict, Any, Optional


def render_card(title: str, content: str, card_type: str = "default", icon: str = None):
    """
    Render a styled card component.
    
    Args:
        title: Card title
        content: Card content
        card_type: Type of card (default, success, warning, error, info)
        icon: Optional emoji icon
    """
    icon_html = f"<span style='font-size: 1.5rem; margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    
    card_classes = {
        "default": "mtaa-card",
        "success": "mtaa-card mtaa-alert success",
        "warning": "mtaa-card mtaa-alert warning", 
        "error": "mtaa-card mtaa-alert error",
        "info": "mtaa-card mtaa-alert info"
    }
    
    card_class = card_classes.get(card_type, "mtaa-card")
    
    st.markdown(f"""
    <div class="{card_class}">
        <h3>{icon_html}{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_data_list(items: List[str], title: str = None, show_icons: bool = True):
    """
    Render a styled list of data items.
    
    Args:
        items: List of items to display
        title: Optional title for the list
        show_icons: Whether to show checkmark icons
    """
    if title:
        st.subheader(title)
    
    for item in items:
        icon = "✅ " if show_icons else ""
        
        # Determine styling based on content
        if "Above" in item or "⚠️" in item:
            item_class = "mtaa-data-item budget-warning"
        elif "Error" in item or "❌" in item:
            item_class = "mtaa-data-item budget-danger"
        else:
            item_class = "mtaa-data-item"
        
        st.markdown(f"""
        <div class="{item_class}">
            {icon}{item}
        </div>
        """, unsafe_allow_html=True)


def render_budget_breakdown(budget_data: Dict[str, Any]):
    """
    Render a budget breakdown component.
    
    Args:
        budget_data: Dictionary containing budget information
    """
    st.markdown("""
    <div class="budget-breakdown">
        <h3>💰 Budget Breakdown</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_budget = budget_data.get('total_budget', 0)
    expenses = budget_data.get('estimated_expenses', {})
    
    if expenses:
        for category, amount in expenses.items():
            percentage = (amount / total_budget * 100) if total_budget > 0 else 0
            
            st.markdown(f"""
            <div class="budget-item">
                <span class="budget-category">{category.title()}</span>
                <span class="budget-amount">KES {amount:,} ({percentage:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress bars for visual representation
        st.markdown("### Visual Breakdown")
        for category, amount in expenses.items():
            percentage = amount / total_budget if total_budget > 0 else 0
            st.progress(percentage, text=f"{category.title()}: KES {amount:,}")


def render_metric_cards(metrics: List[Dict[str, Any]]):
    """
    Render metric cards in a row.
    
    Args:
        metrics: List of metric dictionaries with 'label', 'value', and optional 'delta'
    """
    cols = st.columns(len(metrics))
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            value = metric.get('value', 0)
            label = metric.get('label', '')
            delta = metric.get('delta')
            
            if delta:
                st.metric(label=label, value=value, delta=delta)
            else:
                st.metric(label=label, value=value)


def show_loading_spinner(message: str = "Loading..."):
    """
    Show a loading spinner with message.
    
    Args:
        message: Loading message to display
    """
    st.markdown(f"""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <p style="margin-left: 1rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_itinerary_card(day_data: Dict[str, Any]):
    """
    Render an itinerary day card.
    
    Args:
        day_data: Dictionary containing day information
    """
    day_num = day_data.get('day', 1)
    budget = day_data.get('budget', 0)
    activities = day_data.get('activities', [])
    notes = day_data.get('notes', [])
    
    st.markdown(f"""
    <div class="mtaa-card">
        <h3>📅 Day {day_num} - Budget: KES {budget:,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if activities:
        for activity in activities:
            time_slot = activity.get('time', 'Not specified')
            activity_name = activity.get('activity', 'Activity')
            location = activity.get('location', 'Location TBD')
            cost = activity.get('cost', 0)
            description = activity.get('description', '')
            
            st.markdown(f"""
            <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                <strong>🕐 {time_slot}</strong><br>
                <strong>{activity_name}</strong> at {location}<br>
                <em>{description}</em><br>
                <span style="color: #667eea; font-weight: 600;">Cost: KES {cost}</span>
            </div>
            """, unsafe_allow_html=True)
    
    if notes:
        st.markdown("**💡 Notes:**")
        for note in notes:
            st.markdown(f"- {note}")


def render_city_summary(city_data: Dict[str, Any]):
    """
    Render a city summary component.
    
    Args:
        city_data: Dictionary containing city information
    """
    city = city_data.get('city', 'Unknown City')
    budget = city_data.get('budget', 0)
    goal = city_data.get('goal', 'Survive')
    
    summary = city_data.get('data_summary', {})
    
    st.markdown(f"""
    <div class="mtaa-card">
        <h2>🏙️ {city} - {goal} Plan</h2>
        <p><strong>Budget:</strong> KES {budget:,}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if summary:
        metrics = [
            {'label': 'Rentals Found', 'value': summary.get('rentals_found', 0)},
            {'label': 'Food Options', 'value': summary.get('food_options', 0)},
            {'label': 'Chill Spots', 'value': summary.get('chill_spots', 0)},
            {'label': 'Transport Options', 'value': summary.get('transport_options', 0)}
        ]
        
        render_metric_cards(metrics)


def render_emergency_info(city: str):
    """
    Render emergency information for a city.
    
    Args:
        city: City name
    """
    render_card(
        title="🆘 Emergency Information",
        content=f"""
        <strong>Emergency Services:</strong><br>
        • Police, Fire, Medical: 999 or 112<br>
        • {city} Police: Contact local station<br>
        • Tourist Helpline: 0800 221 000<br><br>
        
        <strong>Important Tips:</strong><br>
        • Keep emergency contacts saved in your phone<br>
        • Know the location of nearest hospital<br>
        • Have backup transportation options<br>
        • Keep some cash for emergencies
        """,
        card_type="error",
        icon="🚨"
    )


def render_tips_section(tips: List[str], title: str = "💡 Helpful Tips"):
    """
    Render a tips section.
    
    Args:
        tips: List of tip strings
        title: Section title
    """
    st.markdown(f"### {title}")
    
    for tip in tips:
        st.markdown(f"""
        <div style="background: #f0f8ff; padding: 0.8rem; margin: 0.5rem 0; 
                    border-left: 4px solid #2196f3; border-radius: 5px;">
            💡 {tip}
        </div>
        """, unsafe_allow_html=True)


def render_chat_message(message: str, is_user: bool = False, avatar: str = None):
    """
    Render a chat message with styling.
    
    Args:
        message: Message content
        is_user: Whether this is a user message
        avatar: Optional avatar emoji
    """
    if avatar is None:
        avatar = "👤" if is_user else "🤖"
    
    message_class = "chat-message user" if is_user else "chat-message assistant"
    
    st.markdown(f"""
    <div class="{message_class}">
        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{avatar}</span>
        {message}
    </div>
    """, unsafe_allow_html=True)


def render_progress_tracker(steps: List[Dict[str, Any]], current_step: int = 0):
    """
    Render a progress tracker for multi-step processes.
    
    Args:
        steps: List of step dictionaries with 'title' and 'description'
        current_step: Current step index (0-based)
    """
    st.markdown("### 📋 Progress Tracker")
    
    for i, step in enumerate(steps):
        if i < current_step:
            icon = "✅"
            status = "Completed"
            style = "color: #28a745;"
        elif i == current_step:
            icon = "🔄"
            status = "In Progress"
            style = "color: #ffc107; font-weight: bold;"
        else:
            icon = "⏳"
            status = "Pending"
            style = "color: #6c757d;"
        
        st.markdown(f"""
        <div style="padding: 0.5rem 0; {style}">
            {icon} <strong>Step {i+1}:</strong> {step['title']} - <em>{status}</em><br>
            <small>{step.get('description', '')}</small>
        </div>
        """, unsafe_allow_html=True)


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    
    # Load CSS from file if it exists, otherwise use inline CSS
    try:
        with open('ui/style.css', 'r') as f:
            css_content = f.read()
    except FileNotFoundError:
        # Fallback inline CSS
        css_content = """
        .mtaa-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #667eea;
        }
        
        .mtaa-data-item {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.5rem 0;
            border-left: 3px solid #28a745;
        }
        
        .budget-breakdown {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        """
    
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def show_success_message(message: str, duration: int = 3):
    """
    Show a temporary success message.
    
    Args:
        message: Success message
        duration: Duration in seconds
    """
    success_placeholder = st.empty()
    success_placeholder.success(message)
    time.sleep(duration)
    success_placeholder.empty()


def show_error_message(message: str, duration: int = 5):
    """
    Show a temporary error message.
    
    Args:
        message: Error message
        duration: Duration in seconds
    """
    error_placeholder = st.empty()
    error_placeholder.error(message)
    time.sleep(duration)
    error_placeholder.empty()


def create_download_button(data: Any, filename: str, button_text: str = "Download Data"):
    """
    Create a download button for data.
    
    Args:
        data: Data to download (will be converted to JSON)
        filename: Name of the download file
        button_text: Text for the download button
    """
    import json
    
    if isinstance(data, dict):
        data_str = json.dumps(data, indent=2)
    else:
        data_str = str(data)
    
    st.download_button(
        label=button_text,
        data=data_str,
        file_name=filename,
        mime="application/json"
    )