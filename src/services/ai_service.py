"""
AI Service module for handling all AI-related operations.
"""
import google.generativeai as genai
import time
import logging
from functools import wraps
from typing import Union, List, Dict, Any
from ..utils.config import MODEL_NAME

logger = logging.getLogger(__name__)

def retry_on_error(max_retries: int = 3, delay: int = 1):
    """Decorator for retrying AI operations with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            last_error = None
            
            while retries < max_retries:
                try:
                    if retries > 0:
                        time.sleep(delay * (2 ** (retries - 1)))
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    error_str = str(e).lower()
                    
                    # Handle specific error types
                    if "quota" in error_str:
                        logger.error("API quota exceeded")
                        raise Exception("API quota exceeded. Please try again later.")
                    elif "invalid" in error_str:
                        logger.error("Invalid API key")
                        raise Exception("Invalid API key. Please check your configuration.")
                    
                    retries += 1
                    logger.warning(f"Retry {retries}/{max_retries} for {func.__name__}: {e}")
                    
                    if retries == max_retries:
                        logger.error(f"Max retries exceeded for {func.__name__}: {last_error}")
                        raise last_error
                        
            return None
        return wrapper
    return decorator

class AIService:
    """Centralized AI service for handling all AI operations."""
    
    def __init__(self, api_key: str):
        """Initialize the AI service with API key."""
        self.api_key = api_key
        self.model_name = MODEL_NAME
        self._configure_api()
        
    def _configure_api(self):
        """Configure the Google AI API."""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"AI service initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to configure AI API: {e}")
            raise
    
    @retry_on_error(max_retries=3, delay=2)
    def generate_content(self, prompt: Union[str, List[Dict[str, Any]]]) -> str:
        """
        Generate content using the AI model.
        
        Args:
            prompt: Either a string prompt or list of message dictionaries
            
        Returns:
            Generated text content
        """
        try:
            # Handle both single string prompts and message lists
            if isinstance(prompt, str):
                messages = [{"role": "user", "parts": [prompt]}]
            else:
                messages = prompt
                
            response = self.model.generate_content(messages)
            
            if not response or not response.text:
                raise ValueError("Empty response from AI model")
                
            logger.info("Successfully generated AI content")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating AI content: {e}")
            raise
    
    def generate_interview_question(self, role: str, experience: str, 
                                  interview_type: str, difficulty: str, 
                                  focus_points: str) -> Dict[str, str]:
        """Generate an interview question with expected answer."""
        context = f"""As an expert interviewer for a {role} position with {experience} experience expectation,
generate a relevant {interview_type.lower()} interview question.

Role Context:
- Position: {role}
- Experience Level: {experience}
- Interview Type: {interview_type}
- Difficulty: {difficulty}
- Focus Areas: {focus_points}

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

        try:
            response_text = self.generate_content(context)
            
            # Parse the response
            parts = response_text.split("Expected Answer:", 1)
            question_part = parts[0].replace("Question:", "", 1).strip() if len(parts) > 0 else response_text
            answer_part = parts[1].strip() if len(parts) > 1 else "No model answer provided."
            
            return {
                "question": question_part,
                "expected_answer": answer_part
            }
            
        except Exception as e:
            logger.error(f"Error generating interview question: {e}")
            raise
    
    def evaluate_response(self, role: str, experience: str, interview_type: str, 
                         difficulty: str, question: str, user_answer: str) -> Dict[str, str]:
        """Evaluate a user's response to an interview question."""
        evaluation_context = f"""As an expert interviewer for {role} positions with {experience} experience expectation, evaluate this response:

Question Asked: {question}
Candidate's Answer: {user_answer}
Role: {role}
Experience Level: {experience}
Interview Type: {interview_type}
Difficulty: {difficulty}

Provide a detailed evaluation in this EXACT format (use numbers only, no brackets):

Technical Assessment:
- Knowledge Depth: 7.5 - [brief explanation]
- Implementation Understanding: 6.0 - [brief explanation]  
- Best Practices Awareness: 7.0 - [brief explanation]

Communication Assessment:
- Clarity: 8.0 - [brief explanation]
- Structure: 7.5 - [brief explanation]
- Professionalism: 8.5 - [brief explanation]

Experience Level Match:
- Expected Level: {experience}
- Demonstrated Level: [assessment]
- Score: 7.0

Key Strengths:
- [Point 1]
- [Point 2]

Areas for Improvement:
- [Point 1]
- [Point 2]

Follow-up Question:
[Ask a logically connected {difficulty} difficulty question]

Expected Answer:
[Provide a model answer with key points]

IMPORTANT: Use decimal numbers (like 7.5, 6.0, 8.5) for all scores. Do not use brackets around scores."""

        try:
            response_text = self.generate_content(evaluation_context)
            
            # Parse the response
            parts = response_text.split("Follow-up Question:", 1)
            assessment_part = parts[0].strip()
            follow_up_part = parts[1] if len(parts) > 1 else "No follow-up provided."
            
            follow_up_parts = follow_up_part.split("Expected Answer:", 1)
            follow_up_question = follow_up_parts[0].strip()
            follow_up_expected = follow_up_parts[1].strip() if len(follow_up_parts) > 1 else "No model answer for follow-up."
            
            return {
                "assessment": assessment_part,
                "follow_up_question": follow_up_question,
                "follow_up_expected": follow_up_expected
            }
            
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            raise