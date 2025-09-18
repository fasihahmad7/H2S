import streamlit as st
import streamlit.components.v1 as components
import uuid

def custom_text_area(label, placeholder="", height=150, key=None, allow_paste=False):
    """
    Creates a Streamlit text area that optionally prevents pasting.
    
    Args:
        label: Label for the text area
        placeholder: Placeholder text
        height: Height of the text area in pixels
        key: Unique key for the component
        allow_paste: If True, allows pasting (for accessibility)
    """
    component_key = key or str(uuid.uuid4())
    
    # JavaScript to intercept and block the 'paste' event if needed
    js_code = f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const ta = document.querySelector('textarea[data-testid="{component_key}"]');
        if (ta) {{
            ta.addEventListener('paste', function(e) {{
                const allowPaste = {str(allow_paste).lower()};
                if (!allowPaste) {{
                    e.preventDefault();
                    alert('Pasting is disabled to encourage spontaneous answers. If you need paste functionality for accessibility reasons, please contact support.');
                }}
            }});
        }}
    }});
    </script>
    """
    
    components.html(js_code, height=0)
    
    return st.text_area(label, placeholder=placeholder, height=height, key=component_key)