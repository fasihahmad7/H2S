import streamlit as st
import google.generativeai as genai
from functools import wraps
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def get_focus_points(interview_type: str, role: str) -> str:
    """Get focus points based on interview type and role."""
    if interview_type == "Technical":
        return "technical skills, coding ability, and problem-solving methodology"
    elif interview_type == "Behavioral":
        return "past experiences, soft skills, and professional conduct"
    else:  # Problem Solving
        return "analytical thinking, solution design, and implementation approach"

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
INTERVIEW_TYPES = [
    "Technical", "Behavioral", "Problem Solving"
]

DIFFICULTY_LEVELS = [
    "Easy", "Medium", "Hard", "Legend"
]

JOB_ROLES = [
    "Software Engineer", "Data Scientist", "Product Manager",
    "Full Stack Developer", "AI/ML Engineer", "DevOps Engineer",
    "QA Engineer", "Automation Test Engineer", "SDET", 
    "Performance Test Engineer", "API Test Engineer",
    "Mobile Test Engineer", "Security Test Engineer",
    "Test Architect", "QA Lead", "Functional Tester"
]

EXPERIENCE_RANGES = [
    "0-2 years", "2-5 years", "5-8 years", "8+ years"
]

# Configure Google API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("⚠️ API Key not found! Please follow these steps:")
    st.markdown("""
    1. Create a `.env` file in the project root
    2. Add your Google API key: `GOOGLE_API_KEY=your_key_here`
    3. Restart the application
    """)
    st.stop()

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"⚠️ Error configuring API: {str(e)}")
    st.stop()

# Retry decorator for API calls with rate limiting
def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            last_error = None
            
            while retries < max_retries:
                try:
                    if retries > 0:
                        time.sleep(delay * (2 ** (retries - 1)))  # Exponential backoff
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    error_type = type(e).__name__
                    
                    if "quota" in str(e).lower():
                        st.error("⚠️ API quota exceeded. Please try again later.")
                        raise
                    elif "invalid" in str(e).lower():
                        st.error("⚠️ Invalid API key. Please check your configuration.")
                        raise
                    
                    retries += 1
                    if retries == max_retries:
                        st.error(f"⚠️ Error after {max_retries} retries: {str(last_error)}")
                        raise last_error
                        
            return None
        return wrapper
    return decorator

@retry_on_error(max_retries=3, delay=2)
def get_ai_response(messages):
    """Get AI response with enhanced error handling and rate limiting."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(messages)
        
        if not response or not response.text:
            raise ValueError("Empty response from AI model")
            
        return response.text
        
    except Exception as e:
        st.error(f"⚠️ Error getting AI response: {str(e)}")
        raise

def calculate_role_specific_metrics(role, experience, responses):
    # Initialize metrics with default values
    metrics = {
        'domain_knowledge': 0.0,
        'methodology_understanding': 0.0,
        'practical_experience': 0.0
    }
    
    if not responses:
        return metrics
    
    # Role-specific keywords for scoring
    role_keywords = {
        "Software Engineer": {
            "domain": ["algorithm", "data structure", "programming", "code", "software", "development", "testing", "git"],
            "methodology": ["agile", "scrum", "tdd", "ci/cd", "design pattern", "architecture", "review"],
            "practical": ["implemented", "developed", "built", "created", "managed", "debugged", "optimized"]
        },
        "Data Scientist": {
            "domain": ["machine learning", "statistics", "data analysis", "model", "algorithm", "python", "r"],
            "methodology": ["research", "analysis", "hypothesis", "validation", "cross-validation", "pipeline"],
            "practical": ["analyzed", "trained", "evaluated", "deployed", "improved", "experimented"]
        },
        "Functional Tester": {
            "domain": ["test cases", "requirements", "user scenarios", "acceptance criteria", "defect", "bug", "regression", "test plan"],
            "methodology": ["manual testing", "test design", "test execution", "test strategy", "risk analysis", "test reporting"],
            "practical": ["tested", "verified", "validated", "documented", "reported", "reproduced", "identified"]
        }
        # Add more roles as needed...
    }
    
    # Use default keywords if role not found
    default_keywords = {
        "domain": ["technical", "skill", "knowledge", "understanding"],
        "methodology": ["process", "method", "approach", "solution", "strategy"],
        "practical": ["experience", "project", "worked", "implemented", "handled"]
    }
    
    keywords = role_keywords.get(role, default_keywords)
    
    # Calculate scores based on keyword matches
    for response in responses:
        content = response.get("content", "").lower()
        
        # Domain Knowledge Score
        domain_matches = sum(1 for keyword in keywords["domain"] if keyword in content)
        metrics['domain_knowledge'] += (domain_matches / len(keywords["domain"])) * 10
        
        # Methodology Understanding Score
        method_matches = sum(1 for keyword in keywords["methodology"] if keyword in content)
        metrics['methodology_understanding'] += (method_matches / len(keywords["methodology"])) * 10
        
        # Practical Experience Score
        practical_matches = sum(1 for keyword in keywords["practical"] if keyword in content)
        metrics['practical_experience'] += (practical_matches / len(keywords["practical"])) * 10
    
    # Average the scores
    response_count = len(responses)
    metrics['domain_knowledge'] = round(metrics['domain_knowledge'] / response_count, 1)
    metrics['methodology_understanding'] = round(metrics['methodology_understanding'] / response_count, 1)
    metrics['practical_experience'] = round(metrics['practical_experience'] / response_count, 1)
    
    return metrics

def export_interview_history():
    history = {
        'timestamp': datetime.now().isoformat(),
        'history': st.session_state.interview_history,
        'stats': st.session_state.session_stats
    }
    return json.dumps(history, indent=2)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'interview_history' not in st.session_state:
    st.session_state.interview_history = []
if 'session_stats' not in st.session_state:
    st.session_state.session_stats = {
        'total_questions': 0,
        'technical_score': 0,
        'communication_score': 0,
        'role_specific_metrics': {}
    }
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'current_response' not in st.session_state:
    st.session_state.current_response = ""

# Custom CSS for Adobe-like styling
st.markdown("""
    <style>    /* Hide default Streamlit elements */
    #MainMenu, footer {visibility: hidden;}
    
    /* Input field styling */
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
    
    /* Question formatting */
    .interview-message b {
        color: #1473E6;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .interview-message br {
        content: "";
        display: block;
        margin: 0.5rem 0;
    }
    
    /* Input field styling */
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
    
    /* Question formatting */
    .interview-message b {
        color: #1473E6;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .interview-message br {
        content: "";
        display: block;
        margin: 0.5rem 0;
    }
    
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
    }    /* Interview messages - Adobe-like */
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
    }    .user-message {
        border-left: 4px solid #4B9AD8;
        background-color: #2D2D2D;
    }
    .user-message b, .user-message br, .user-message {
        color: #E6E6E6 !important;
    }
    
    /* Ensure text inputs and placeholders are visible */
    .stTextInput input::placeholder {
        color: #95A5A6 !important;
    }    .stTextInput > div > div > input {
        color: #E6E6E6 !important;
        background-color: #393939 !important;
        border-color: #464646 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1473E6 !important;
        box-shadow: 0 0 0 1px #1473E6 !important;
    }/* Form elements - Adobe-like */
    .stTextInput > div > div, 
    .stSelectbox > div > div,
    div[data-baseweb="select"] > div {
        background-color: #393939 !important;
        border: 1px solid #464646 !important;
        border-radius: 6px !important;
        color: #E6E6E6 !important;
    }
    
    /* Headers and labels - Adobe-like */
    h1, h2, h3, h4, h5, h6,
    label, .stMarkdown p {
        color: #E6E6E6 !important;
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
      /* Dropdown styling - Adobe-like */
    div[role="listbox"] {
        background-color: #393939 !important;
        border: 1px solid #464646 !important;
        border-radius: 6px !important;
    }
    div[role="option"] {
        color: #E6E6E6 !important;
        padding: 8px 12px !important;
    }
    div[role="option"]:hover {
        background-color: #464646 !important;
    }
    div[data-baseweb="select"] span {
        color: #E6E6E6 !important;
    }
    
    /* Input field styling */
    .stTextInput input::placeholder {
        color: #8E8E8E !important;
    }
    
    /* Progress indicators and spinners */
    .stProgress > div > div {
        background-color: #1473E6 !important;
    }
    
    /* Alert and info boxes */
    .stAlert {
        background-color: #393939 !important;
        border: 1px solid #464646 !important;
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

# Main UI
st.markdown('<h1 class="main-title">🎯 AI Interview Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">Powered by Google Gemini 1.5</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("🔧 Interview Setup")
    selected_role = st.selectbox("Choose Your Role", JOB_ROLES, help="Select the position you're interviewing for")
    experience_level = st.selectbox("Your Experience Level", EXPERIENCE_RANGES, help="Select your years of experience")
    interview_type = st.selectbox("Interview Type", INTERVIEW_TYPES, help="Select the type of interview questions")
    difficulty_level = st.selectbox("Question Difficulty", DIFFICULTY_LEVELS, help="Select the difficulty level of questions")
    
    # Interview controls
    st.markdown("### 📊 Interview Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Interview", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_stats = {
                'total_questions': 0,
                'technical_score': 0,
                'communication_score': 0,
                'role_specific_metrics': {}
            }
            st.rerun()
    with col2:
        if st.button("💾 Export History", use_container_width=True):
            history_json = export_interview_history()
            st.download_button(
                "📥 Download History",
                history_json,
                "interview_history.json",
                "application/json",
                use_container_width=True
            )
    
    # Display session statistics
    st.markdown("### 📈 Session Progress")
    metrics = st.session_state.session_stats.get('role_specific_metrics', {})
    st.markdown(f"""
        <div class="stat-box">
            <b>Questions Asked:</b> {st.session_state.session_stats['total_questions']}<br>
            <b>Domain Knowledge:</b> {metrics.get('domain_knowledge', 0):.1f}/10<br>
            <b>Methodology:</b> {metrics.get('methodology_understanding', 0):.1f}/10<br>
            <b>Practical Experience:</b> {metrics.get('practical_experience', 0):.1f}/10
        </div>
    """, unsafe_allow_html=True)

def start_interview(role, experience, interview_type, difficulty):
    """Start a new interview session with initial question."""
    context = f"""As an expert interviewer for a {role} position with {experience} experience expectation, 
generate a relevant {interview_type.lower()} interview question.

Role Context:
- Position: {role}
- Experience Level: {experience}
- Interview Type: {interview_type}
- Difficulty: {difficulty}
- Focus Areas: {get_focus_points(interview_type, role)}

Required Question Criteria:
1. Must be highly relevant to the {role} role
2. Appropriate for {experience} experience level
3. Follows {interview_type.lower()} interview style
4. Matches {difficulty.lower()} difficulty:
   - Easy: Core concepts, fundamentals, daily tasks
   - Medium: Applied knowledge, real scenarios, problem-solving
   - Hard: Complex problems, system design, edge cases
   - Legend: Expert challenges, architecture decisions, innovation

Format your response exactly as:
Question: [Clear, focused question appropriate for role and level]

Expected Answer: [Detailed model answer including:
- Key points that should be covered
- Common pitfalls to avoid
- Best practices to mention
- Experience-appropriate insights]"""
    
    first_question = get_ai_response(context)
    st.session_state.messages = [{"role": "assistant", "content": first_question}]

# Display welcome message if no messages exist
if not st.session_state.messages:
    st.markdown(f"""
        <div style="text-align: center; padding: 40px; background-color: #393939; border-radius: 6px; margin: 20px 0; border: 1px solid #464646;">
            <h2 style="color: #E6E6E6;">👋 Welcome to Your Interview Session!</h2>
            <p style="color: #E6E6E6;">Selected Role: <b>{selected_role}</b></p>
            <p style="color: #E6E6E6;">Experience Level: <b>{experience_level}</b></p>
            <p style="color: #E6E6E6;">Interview Type: <b>{interview_type}</b></p>
            <p style="color: #E6E6E6;">I'll ask you relevant questions and provide detailed feedback.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Center the start button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Start Interview", use_container_width=True, type="primary"):
            with st.spinner("🤖 Preparing your first question..."):
                start_interview(selected_role, experience_level, interview_type, difficulty_level)
                st.rerun()

# Display interview conversation
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "assistant":
        # Split content to separate expected answer
        content = message["content"]
        if "Expected Answer:" in content:
            parts = content.split("Expected Answer:", 1)
            
            # Show the question/feedback part
            st.markdown(
                f'<div class="interview-message interviewer-message">'
                f'<b>👤 Interviewer:</b><br>{parts[0].strip()}'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # Only show expected answer if this is not the latest question or user has responded
            show_expected = (i < len(st.session_state.messages) - 1 or 
                          (i == len(st.session_state.messages) - 1 and 
                           i > 0 and st.session_state.messages[i-1]["role"] == "user"))
            if show_expected:
                st.markdown(
                    f'<div class="interview-message interviewer-message">'
                    f'<b>✓ Expected Answer:</b><br>{parts[1].strip()}'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            # Message without expected answer
            st.markdown(
                f'<div class="interview-message interviewer-message">'
                f'<b>👤 Interviewer:</b><br>{content}'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        # User message
        st.markdown(
            f'<div class="interview-message user-message">'
            f'<b>💬 Your Response:</b><br>{message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )



# Input area for user responses
if st.session_state.messages:  # Only show input if interview has started
    # Get user input
    prompt = st.text_input(
        "Your Response",
        placeholder="Type your answer here and press Enter",
        key="response_input",
        disabled=st.session_state.is_processing
    )
    
    # Only process if there's new input and not already processing
    if prompt and prompt != st.session_state.current_response and not st.session_state.is_processing:
        st.session_state.is_processing = True
        st.session_state.current_response = prompt
        
        with st.spinner("🤔 Analyzing your response..."):
            try:
                # Add user response to messages
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Get previous question for context
                prev_question = ""
                for msg in reversed(st.session_state.messages[:-1]):
                    if msg["role"] == "assistant" and "Question:" in msg["content"]:
                        prev_question = msg["content"].split("Question:")[1].split("Expected Answer:")[0].strip()
                        break
                
                # Prepare context for AI evaluation
                context = f"""As an expert interviewer for {selected_role} positions with {experience_level} experience expectation, evaluate this response:

Question Asked: {prev_question}
Candidate's Answer: {prompt}

Role: {selected_role}
Experience Level: {experience_level}
Interview Type: {interview_type}
Difficulty: {difficulty_level}

Provide a detailed evaluation in this format:

Technical Assessment (1-10):
- Knowledge Depth: [score] - [brief explanation]
- Implementation Understanding: [score] - [brief explanation]
- Best Practices Awareness: [score] - [brief explanation]

Communication Assessment (1-10):
- Clarity: [score] - [brief explanation]
- Structure: [score] - [brief explanation]
- Professionalism: [score] - [brief explanation]

Experience Level Match:
- Expected Level: {experience_level}
- Demonstrated Level: [assessment]
- Score: [1-10]

Key Strengths:
- [Point 1]
- [Point 2]

Areas for Improvement:
- [Point 1]
- [Point 2]

Overall Score: [Calculate average]

Follow-up Question:
[Ask a logically connected {difficulty_level} difficulty question]

Expected Answer:
[Provide a model answer with key points]"""
                
                # Get AI response and update session state
                response = get_ai_response(context)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.interview_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "role": selected_role,
                    "experience": experience_level,
                    "interview_type": interview_type,
                    "question": prev_question,
                    "answer": prompt,
                    "feedback": response
                })
                
                # Update statistics
                st.session_state.session_stats['total_questions'] += 1
                role_metrics = calculate_role_specific_metrics(
                    selected_role,
                    experience_level,
                    st.session_state.messages
                )
                st.session_state.session_stats['role_specific_metrics'] = role_metrics
            
            except Exception as e:
                st.error(f"An error occurred while processing your response: {str(e)}")
            
            finally:
                st.session_state.is_processing = False
                st.rerun()