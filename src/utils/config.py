"""
Configuration settings for the AI Interview Assistant.
"""
from typing import Dict, List

# AI Model Settings
MODEL_NAME = 'gemini-pro'
TEMPERATURE = 0.7
TOP_P = 0.8
TOP_K = 40

# Interview Settings
JOB_ROLES: List[str] = [
    "Software Engineer",
    "Data Scientist",
    "Product Manager",
    "Full Stack Developer",
    "AI/ML Engineer",
    "DevOps Engineer"
]

QUESTION_TYPES: Dict[str, str] = {
    "technical": "Generate a technical question that tests specific knowledge and problem-solving skills.",
    "behavioral": "Generate a behavioral question that assesses past experiences and soft skills.",
    "problem_solving": "Generate a problem-solving question that evaluates analytical thinking."
}

# Performance Analysis Settings
ANALYSIS_WEIGHTS = {
    'response_quality': 0.5,
    'technical_accuracy': 0.3,
    'communication_clarity': 0.2
}
