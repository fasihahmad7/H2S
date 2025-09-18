"""
UI Manager for handling user interface components and styling.
"""
import streamlit as st
from typing import Dict, Any, List

class UIManager:
    """Manages UI components and styling."""
    
    def __init__(self):
        """Initialize UI manager."""
        self._apply_custom_css()
    
    def _apply_custom_css(self):
        """Apply custom CSS styling."""
        st.markdown("""
            <style>
            /* Hide default Streamlit elements */
            #MainMenu, footer {visibility: hidden;}
            
            /* Base styles - Adobe-like theme */
            .stApp {
                background-color: #2D2D2D;
            }
            
            /* Top bar styling */
            header {
                background-color: #323232 !important;
                border-bottom: 1px solid #464646;
            }
            
            /* Global text color */
            .stApp, .stTextInput, .stSelectbox, div[data-baseweb="select"],
            .streamlit-expanderHeader, div[data-testid="stMarkdown"] {
                color: #E6E6E6 !important;
            }
            
            /* Sidebar styling - Adobe-like */
            section[data-testid="stSidebar"] {
                background-color: #2D2D2D;
                border-right: 1px solid #464646;
            }
            section[data-testid="stSidebar"] .stMarkdown {
                color: #E6E6E6;
            }
            section[data-testid="stSidebar"] .stMarkdown a {
                color: #4B9AD8;
            }
            
            /* Title and containers - Adobe-like */
            .main-title {
                text-align: center;
                color: #E6E6E6;
                padding: 1.5rem;
                border-radius: 6px;
                margin: 1rem 0;
                background: #1473E6;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            }
            .stat-box {
                background-color: #393939;
                padding: 1rem;
                border-radius: 6px;
                margin: 0.5rem 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                border-left: 4px solid #1473E6;
            }
            
            /* Interview messages - Adobe-like */
            .interview-message {
                padding: 1rem;
                border-radius: 6px;
                margin: 1rem 0;
                background-color: #393939;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                color: #E6E6E6;
            }
            .interviewer-message {
                border-left: 4px solid #1473E6;
            }
            .model-answer {
                border-left: 4px solid #4CAF50;
                background-color: #3a4a3a;
            }
            .assessment {
                border-left: 4px solid #FF9800;
                background-color: #4a423a;
            }
            .user-message {
                border-left: 4px solid #4B9AD8;
                background-color: #2D2D2D;
            }
            .user-message b, .user-message br, .user-message {
                color: #E6E6E6 !important;
            }
            
            /* Form elements - Adobe-like */
            .stTextInput > div > div > input {
                color: #E6E6E6 !important;
                background-color: #393939 !important;
                border: 1px solid #464646 !important;
                border-radius: 6px !important;
                padding: 0.5rem 1rem !important;
            }
            .stTextInput > div > div > input:focus {
                border-color: #1473E6 !important;
                box-shadow: 0 0 0 1px #1473E6 !important;
            }
            .stTextInput input::placeholder {
                color: #95A5A6 !important;
            }
            
            /* Button styling - Adobe-like */
            .stButton > button {
                width: 100%;
                background: #1473E6 !important;
                color: white !important;
                border: none !important;
                padding: 0.5rem 1rem !important;
                border-radius: 6px !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button:hover {
                background: #0D66D0 !important;
                transform: translateY(-1px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2) !important;
            }
            
            /* Headers and labels - Adobe-like */
            h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
                color: #E6E6E6 !important;
            }
            
            /* Links */
            a {
                color: #4B9AD8 !important;
                text-decoration: none !important;
            }
            a:hover {
                text-decoration: underline !important;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def render_title(self):
        """Render the main application title."""
        st.markdown('<h1 class="main-title">🎯 AI Interview Assistant</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;">Powered by Google Gemini 1.5</p>', unsafe_allow_html=True)
    
    def render_welcome_message(self, role: str, experience: str, interview_type: str):
        """Render the welcome message when no interview has started."""
        st.markdown(f"""
            <div style="text-align: center; padding: 40px; background-color: #393939; border-radius: 6px; margin: 20px 0; border: 1px solid #464646;">
                <h2 style="color: #E6E6E6;">👋 Welcome to Your Interview Session!</h2>
                <p style="color: #E6E6E6;">Selected Role: <b>{role}</b></p>
                <p style="color: #E6E6E6;">Experience Level: <b>{experience}</b></p>
                <p style="color: #E6E6E6;">Interview Type: <b>{interview_type}</b></p>
                <p style="color: #E6E6E6;">I'll ask you relevant questions and provide detailed feedback.</p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_session_stats(self, stats: Dict[str, Any]):
        """Render session statistics in the sidebar."""
        metrics = stats.get('role_specific_metrics', {})
        st.markdown(f"""
            <div class="stat-box">
                <b>Questions Asked:</b> {stats['total_questions']}<br>
                <b>Domain Knowledge:</b> {metrics.get('domain_knowledge', 0):.1f}/10<br>
                <b>Methodology:</b> {metrics.get('methodology_understanding', 0):.1f}/10<br>
                <b>Practical Experience:</b> {metrics.get('practical_experience', 0):.1f}/10<br>
                <b>Overall Score:</b> {metrics.get('overall_score', 0):.1f}/10
            </div>
        """, unsafe_allow_html=True)
    
    def render_message(self, message: Dict[str, Any], is_last_message: bool, has_user_response_after: bool):
        """Render a single message in the conversation."""
        if message["role"] == "assistant":
            msg_type = message.get("type", "question")
            content = message["content"]

            if msg_type == "question":
                question_text = content.get("question", "Error: Question text missing.")
                expected_answer_text = content.get("expected_answer", "")

                # Show the question
                st.markdown(
                    f'<div class="interview-message interviewer-message">'
                    f'<b>👤 Question:</b><br>{question_text}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Show expected answer if not the current question
                if not is_last_message or has_user_response_after:
                    if expected_answer_text:
                        st.markdown(
                            f'<div class="interview-message model-answer">'
                            f'<b>✓ Model Answer:</b><br>{expected_answer_text}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

            elif msg_type == "assessment":
                st.markdown(
                    f'<div class="interview-message assessment">'
                    f'<b>📊 Assessment:</b><br>{content}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        elif message["role"] == "user":
            st.markdown(
                f'<div class="interview-message user-message">'
                f'<b>💬 Your Response:</b><br>{message["content"]}'
                f'</div>',
                unsafe_allow_html=True
            )
    
    def render_conversation(self, messages: List[Dict[str, Any]]):
        """Render the entire conversation."""
        for i, message in enumerate(messages):
            is_last_message = (i == len(messages) - 1)
            has_user_response_after = False
            
            if not is_last_message:
                if i + 1 < len(messages) and messages[i + 1]["role"] == "user":
                    has_user_response_after = True
            
            self.render_message(message, is_last_message, has_user_response_after)