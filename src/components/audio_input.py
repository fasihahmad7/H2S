import streamlit as st
from .custom_text_input import custom_text_area
from typing import Optional
import time
from ..utils.helpers import speech_to_text

class AudioInput:
    def __init__(self):
        if 'recording' not in st.session_state:
            st.session_state.recording = False
            
    def get_user_input(self, placeholder: str = "Enter your answer") -> Optional[str]:
        """
        Get user input through either text or speech.
        
        Args:
            placeholder: Placeholder text for the text input field
            
        Returns:
            str: The user's input text, either typed or transcribed from speech
        """
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Use a unique key for the text area to prevent pre-filling
            text_input = custom_text_area(
                "Your Answer",
                placeholder=placeholder,
                height=150,
                allow_paste=False,
                key=f"user_input_{st.session_state.session_stats['total_questions']}"
            )
            
        with col2:
            use_mic = st.button(
                "🎤 Use Microphone",
                type="primary",
                help="Click to record your answer using your microphone"
            )
            
        if use_mic:
            st.session_state.recording = True
            with st.spinner("🎤 Recording... Speak now"):
                speech_text = speech_to_text()
                
                if speech_text:
                    # If speech was recognized, update the text area
                    st.session_state.recording = False
                    return speech_text
                else:
                    st.error("Could not recognize speech. Please try again or type your answer.")
                    st.session_state.recording = False
                    return None
                    
        return text_input if text_input else None