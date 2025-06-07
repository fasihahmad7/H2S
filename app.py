import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import json

# --- Constants ---
JOB_ROLES = [
    "Software Engineer", "Data Scientist", "Product Manager",
    "Full Stack Developer", "AI/ML Engineer", "DevOps Engineer",
    "QA Engineer", "Automation Test Engineer", "SDET",
    "Performance Test Engineer"
]

EXPERIENCE_RANGES = [
    "0-2 years", "2-5 years", "5-8 years", "8+ years"
]

QUESTION_TYPES = {
    "technical": "Generate a technical question that tests specific knowledge and problem-solving skills.",
    "behavioral": "Generate a behavioral question that assesses past experiences and soft skills.",
    "problem_solving": "Generate a problem-solving question that evaluates analytical thinking."
}

# --- Model Configuration ---
# In your main streamlit app file

def initialize_ai_model() -> Optional[genai.GenerativeModel]:
    """Initialize and configure the Gemini AI model."""
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        st.error("🔴 API key (GOOGLE_API_KEY) not found. Check your .env file.")
        return None

    try:
        genai.configure(api_key=api_key)
        
        # --- THE FINAL FIX ---
        # Use the powerful Gemini 1.5 Pro model that your key has access to.
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
        
        return model
    except Exception as e:
        st.error(f"🔴 Error during AI Model setup: {str(e)}")
        st.error("Troubleshooting: Check API key, 'Generative Language API' in GCP, SDK version.")
        return None

def generate_interview_question(model: genai.GenerativeModel, job_role: str, question_type: str, experience: str) -> str:
    """Generate an interview question based on job role, type, and experience level."""
    prompt = f"""Generate a {question_type} interview question for a {job_role} position with {experience} of experience.
    The question should:
    1. Match the experience level ({experience})
    2. Be specific to the role and requirements
    3. Test both knowledge and application
    4. Be clear and concise
    5. Encourage detailed responses
    Question type context: {QUESTION_TYPES[question_type]}
    Return only the question text, with no introductory phrases."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        return "Failed to generate question. Please try again."

def analyze_answer(model: genai.GenerativeModel, job_role: str, question: str, answer: str) -> Dict[str, Any]:
    """Analyze interview answer and provide feedback safely using JSON."""
    prompt = f"""Analyze this interview answer for a {job_role} position.
    Question: {question}
    Answer: {answer}
    Provide feedback as a valid JSON object. Do not include markdown formatting like ```json.
    Your entire response should be only the JSON object, structured as follows:
    {{
        "score": <integer from 1 to 10>,
        "strengths": ["<strength 1>", "<strength 2>"],
        "areas_for_improvement": ["<area 1>", "<area 2>"],
        "suggested_answer": "<a brief example of a strong answer>",
        "technical_accuracy": <integer from 1 to 10>,
        "communication_clarity": <integer from 1 to 10>
    }}"""

    error_feedback = {
        "score": 0, "strengths": ["Analysis failed"],
        "areas_for_improvement": ["Please try again"],
        "suggested_answer": "Analysis unavailable", "technical_accuracy": 0, "communication_clarity": 0
    }

    try:
        response = model.generate_content(prompt)
        text_response = response.text
        cleaned_text = text_response.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON from model: {e}")
        st.error(f"Model's raw response was: {text_response}")
        return error_feedback
    except Exception as e:
        st.error(f"Error analyzing answer: {str(e)}")
        return error_feedback

# --- Main Application ---
def main():
    # Page Configuration
    st.set_page_config(
        page_title="AI Interview Assistant",
        page_icon="🤖",
        layout="wide"
    )
    st.title("🤖 AI Interview Assistant")

    # --- DIAGNOSTIC BLOCK ---
    # This will show us exactly which version of the library is being used.
    st.info(f"**Running `google-generativeai` version:** `{genai.__version__}`")
    # --- END OF DIAGNOSTIC BLOCK ---

    # Initialize components
    model = initialize_ai_model()
    if not model:
        st.warning("⚠️ Please set up your API key in the .env file to continue.")
        st.stop()

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'interview_history' not in st.session_state:
        st.session_state.interview_history = []    # Sidebar configuration
    with st.sidebar:
        st.header("Interview Settings")
        job_role = st.selectbox("Select Position", JOB_ROLES)
        experience = st.selectbox("Years of Experience", EXPERIENCE_RANGES)
        question_type = st.selectbox("Question Type", list(QUESTION_TYPES.keys()))
        st.markdown("---")
        st.write("### Instructions")
        st.write("1. Select your target position & question type.\n2. Generate a question.\n3. Submit your answer for AI feedback.")

    # Main interview interface
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"### Interview for {job_role} Position")

        if st.button("Generate New Question"):
            st.session_state.current_question = None
            with st.spinner("Generating question..."):                st.session_state.current_question = generate_interview_question(
                    model, job_role, question_type, experience
                )

        if st.session_state.current_question:
            st.info(f"**Question:** {st.session_state.current_question}")
            answer = st.text_area("Your Answer:", height=200, key=f"answer_{st.session_state.current_question}")

            if st.button("Submit Answer"):
                if not answer.strip():
                    st.warning("Please provide an answer before submitting.")
                else:
                    with st.spinner("Analyzing your response..."):
                        feedback = analyze_answer(model, job_role, st.session_state.current_question, answer)
                        st.session_state.interview_history.append({
                            'question': st.session_state.current_question, 'answer': answer, 'feedback': feedback
                        })
                        st.success("### Feedback Received!")
                        sub_col1, sub_col2, sub_col3 = st.columns(3)
                        sub_col1.metric("Overall Score", f"{feedback.get('score', 'N/A')}/10")
                        sub_col2.metric("Technical", f"{feedback.get('technical_accuracy', 'N/A')}/10")
                        sub_col3.metric("Clarity", f"{feedback.get('communication_clarity', 'N/A')}/10")
                        st.write("**Strengths:**")
                        for strength in feedback.get('strengths', []): st.write(f"✅ {strength}")
                        st.write("\n**Areas for Improvement:**")
                        for area in feedback.get('areas_for_improvement', []): st.write(f"📝 {area}")
                        st.write("\n**Suggested Answer Snippet:**")
                        st.info(feedback.get('suggested_answer', 'Not available.'))

    with col2:
        st.write("### Interview History")
        if not st.session_state.interview_history:
            st.caption("Your past questions in this session will appear here.")
        for idx, item in enumerate(reversed(st.session_state.interview_history)):
            with st.expander(f"Q{len(st.session_state.interview_history) - idx}: {item['question'][:40]}..."):
                st.write("**Question:**", item['question'])
                st.write("**Score:**", f"{item['feedback'].get('score', 'N/A')}/10")
                st.write("**Your Answer:**", item['answer'])

if __name__ == "__main__":
    main()