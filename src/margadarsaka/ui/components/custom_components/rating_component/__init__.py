"""
Rating Component for Margadarsaka
A Streamlit custom component for interactive star ratings
"""

import os
import streamlit as st
import streamlit.components.v1 as components
import logging

logger = logging.getLogger(__name__)

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine if the component is being run in development or production mode
_RELEASE = True  # Set to True for integrated deployment

if not _RELEASE:
    # Development mode: use the local build directory
    # Get the path to the js directory in the project structure
    JS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..", "..", "..", "starter-for-js"))
    
    # Check if the component is built
    _component_func = components.declare_component(
        "rating_component",
        url="http://localhost:5173/rating_component.html"
    )
    logger.info(f"Running rating component in development mode. JS_DIR: {JS_DIR}")
else:
    # Production mode: use the static assets from the integrated build
    try:
        # Try to use the static assets from the integrated build
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(parent_dir, "..", "..", "..", "static")
        
        # For integrated deployment, we'll embed the component directly
        _component_func = components.declare_component(
            "rating_component",
            path=None  # Will be handled by the component HTML below
        )
        logger.info(f"Running rating component in production mode.")
    except Exception as e:
        logger.warning(f"Could not load production component, falling back to HTML: {e}")
        _component_func = None


# Create the component function
def rating_component(key=None, initial_value=0, max_stars=5):
    """
    Create a rating component with interactive stars
    
    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component
    initial_value: int
        The initial rating value (0-5)
    max_stars: int
        The maximum number of stars to display
        
    Returns
    -------
    int
        The selected rating (0-5)
    """
    if _component_func is None:
        # Fallback to a simple HTML/JS implementation
        return _create_fallback_rating_component(key, initial_value, max_stars)
    
    # Call the component function
    component_value = _component_func(
        initialValue=initial_value, 
        maxStars=max_stars,
        key=key,
        default=initial_value
    )
    
    return component_value

def _create_fallback_rating_component(key=None, initial_value=0, max_stars=5):
    """
    Fallback rating component using HTML/JavaScript
    """
    component_html = f"""
    <div id="rating-{key or 'default'}" style="display: flex; gap: 5px; align-items: center; font-family: Arial, sans-serif;">
        <div class="stars-container" style="display: flex; gap: 3px;">
    """
    
    for i in range(1, max_stars + 1):
        filled = "★" if i <= initial_value else "☆"
        color = "#FFAC33" if i <= initial_value else "#E0E0E0"
        component_html += f"""
            <span class="star" data-value="{i}" style="font-size: 24px; cursor: pointer; color: {color}; transition: color 0.2s;"
                  onmouseover="highlightStars({i}, '{key or 'default'}')"
                  onclick="selectRating({i}, '{key or 'default'}')">{filled}</span>
        """
    
    component_html += f"""
        </div>
        <span id="rating-text-{key or 'default'}" style="margin-left: 10px; color: #666; font-size: 14px;">
            {_get_rating_text(initial_value)}
        </span>
    </div>
    
    <script>
    function highlightStars(rating, componentKey) {{
        const container = document.getElementById('rating-' + componentKey);
        const stars = container.querySelectorAll('.star');
        stars.forEach((star, index) => {{
            if (index < rating) {{
                star.style.color = '#FFAC33';
                star.textContent = '★';
            }} else {{
                star.style.color = '#E0E0E0';
                star.textContent = '☆';
            }}
        }});
    }}
    
    function selectRating(rating, componentKey) {{
        const textElement = document.getElementById('rating-text-' + componentKey);
        const labels = ['Not rated', 'Poor', 'Below average', 'Average', 'Good', 'Excellent'];
        textElement.textContent = rating > 0 ? labels[Math.min(rating, labels.length - 1)] : labels[0];
        
        // Store the selected rating (this would normally communicate back to Streamlit)
        window['rating_' + componentKey] = rating;
    }}
    </script>
    """
    
    # Use Streamlit's HTML component
    components.html(component_html, height=60)
    
    # Return the initial value (in a real implementation, this would get the selected value)
    return initial_value

def _get_rating_text(rating):
    """Get text description for rating"""
    labels = ['Not rated', 'Poor', 'Below average', 'Average', 'Good', 'Excellent']
    return labels[min(rating, len(labels) - 1)] if rating > 0 else labels[0]


# Demo app for testing
if __name__ == "__main__":
    st.set_page_config(page_title="Rating Component Demo")
    
    st.title("Rating Component Demo")
    st.write("This is a demo of the rating component")
    
    # Use the component
    rating = rating_component(key="rating1")
    
    # Display the result
    st.write(f"Selected rating: {rating}")
    
    # Show different sizes
    st.subheader("Different configurations")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("3 stars:")
        rating2 = rating_component(key="rating2", max_stars=3)
        st.write(f"Selected rating: {rating2}")
    
    with col2:
        st.write("7 stars with initial value 4:")
        rating3 = rating_component(key="rating3", max_stars=7, initial_value=4)
        st.write(f"Selected rating: {rating3}")