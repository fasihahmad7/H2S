import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Streamlit Page Configuration (MUST BE FIRST STREAMLIT COMMAND) ---
st.set_page_config(page_title="AI Interview Assistant", page_icon="🤖")

# --- Global Variables ---
MODEL_TO_USE = None
MODEL_INSTANCE = None
SDK_VERSION_DISPLAYED = False

def initialize_ai_model():
    global MODEL_TO_USE, MODEL_INSTANCE, SDK_VERSION_DISPLAYED

    if not SDK_VERSION_DISPLAYED:
        st.sidebar.caption(f"SDK: google-generativeai v{genai.__version__}")
        print(f"CONSOLE: Using google-generativeai SDK version: {genai.__version__}")
        SDK_VERSION_DISPLAYED = True

    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        st.error("🔴 API key (GOOGLE_API_KEY) not found. Check your .env file.")
        return False

    try:
        genai.configure(api_key=api_key)
        print("CONSOLE: Gemini API configured successfully.")

        # --- Model Selection for Hackathon ---
        # Prioritize Flash for potentially better free-tier performance
        hackathon_model_priority = [
            "models/gemini-1.5-flash-latest",
            "models/gemini-1.5-pro-latest"
        ]
        
        available_models_for_generation = []
        print("\nCONSOLE: Checking available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models_for_generation.append(m.name)
                print(f"CONSOLE: - Found model supporting generateContent: {m.name}")

        selected_model_name = None
        for model_name_option in hackathon_model_priority:
            if model_name_option in available_models_for_generation:
                selected_model_name = model_name_option
                break
        
        if not selected_model_name and available_models_for_generation: # Fallback if preferred not found
            selected_model_name = available_models_for_generation[0]
            st.warning(f"⚠️ Preferred hackathon models not found. Using first available: {selected_model_name}")


        if selected_model_name:
            MODEL_TO_USE = selected_model_name
            MODEL_INSTANCE = genai.GenerativeModel(MODEL_TO_USE)
            st.success(f"✅ AI Model Ready: Using **`{MODEL_TO_USE}`**")
            print(f"CONSOLE: Successfully created model instance for: {MODEL_TO_USE}")
            return True
        else:
            st.error("🔴 No suitable generative models found from your available list.")
            print("CONSOLE: No suitable generative models found that support 'generateContent'.")
            return False

    except Exception as e:
        st.error(f"🔴 Error during AI Model setup: {str(e)}")
        st.error("Troubleshooting: Check API key, 'Generative Language API' in GCP, SDK version. For quota errors, try again in a minute.")
        print(f"CONSOLE: Error during Gemini API setup or model instantiation: {str(e)}")
        return False

# --- Initialize AI Model on App Start ---
model_ready = initialize_ai_model()

# --- UI and App Logic ---
st.title("🤖 AI Interview Assistant")

if not model_ready:
    st.warning("⚠️ AI Model could not be initialized. Please check errors above and ensure your API key is set up correctly.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Interview Settings")
    if MODEL_TO_USE:
        st.caption(f"Active AI Model: `{MODEL_TO_USE}`")
    
    role = st.text_input("Job Role", "Software Engineer")
    field = st.text_input("Field/Industry", "Technology")

    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if not st.session_state.interview_started:
        if st.button("Start Interview"):
            st.session_state.interview_started = True
            st.session_state.chat_history = [] # Reset history
            st.rerun()
    elif st.button("End Interview & Reset"):
        st.session_state.interview_started = False
        st.session_state.chat_history = []
        st.rerun()

def get_ai_response(role_val, field_val, question_val, answer_val):
    global MODEL_INSTANCE, MODEL_TO_USE
    if not MODEL_INSTANCE:
        return "Error: AI Model not initialized."

    prompt = f"""As an expert interviewer for {role_val} positions in {field_val}, evaluate this answer.
    Question: {question_val}
    Candidate's Answer: {answer_val}
    
    Provide feedback in the following format:
    1. Score (1-10): Rate the answer
    2. Strengths: What was good about the answer
    3. Areas for Improvement: What could be better
    4. Better Answer Example: A sample improved answer
    """
    try:
        with st.spinner(f"🤖 AI ({MODEL_TO_USE.split('/')[-1]}) is thinking..."): # Shorter model name
            response = MODEL_INSTANCE.generate_content(prompt)
        return response.text
    except Exception as e_gen:
        error_message = f"Error getting AI response: {str(e_gen)}"
        st.error(f"🔴 {error_message}")
        print(f"CONSOLE: {error_message}")
        if "429" in str(e_gen) or "quota" in str(e_gen).lower():
            return f"Error: API Quota Exceeded for {MODEL_TO_USE}. Please wait a minute and try again. (Hackathon Free Tier Limit)"
        return error_message

# Main Interview Interface
if st.session_state.interview_started:
    questions_db = {
        "Software Engineer": [
            "Explain a challenging project you worked on and how you solved problems.",
            "How do you keep up with new technologies and trends?",
            "Describe a time when you had to deal with a difficult team member."
        ],
        "Data Scientist": [
            "Explain a complex data analysis to a non-technical person.",
            "How do you handle missing or incomplete data?",
            "Describe a project where you applied machine learning."
        ]
    }
    available_questions = questions_db.get(role, questions_db["Software Engineer"])
    question = st.selectbox("Practice Question:", available_questions, key="current_question")
    answer = st.text_area("Your Answer:", height=150, key="current_answer")

    if st.button("Get Feedback"):
        if answer.strip():
            feedback = get_ai_response(role, field, question, answer)
            st.session_state.chat_history.append({
                "question": question,
                "answer": answer,
                "feedback": feedback
            })
            st.rerun()
        else:
            st.warning("Please provide an answer first.")

    if st.session_state.chat_history:
        st.subheader("Interview Progress")
        for i, interaction in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Interaction {len(st.session_state.chat_history) - i}: {interaction['question'][:50]}...", expanded=(i==0)):
                st.markdown(f"**Question:** {interaction['question']}")
                st.markdown(f"**Your Answer:**\n```\n{interaction['answer']}\n```")
                st.markdown(f"**AI Feedback:**\n{interaction['feedback']}")
else:
    if model_ready:
        st.info("👈 Set job details & click 'Start Interview' to begin practicing!")

# Footer
st.markdown("---")
st.markdown("Hackathon AI Interview Practice Tool")