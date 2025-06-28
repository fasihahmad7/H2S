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

# Role-specific evaluation criteria
ROLE_CRITERIA = {
    "Software Engineer": {
        "core_skills": ["Data Structures", "Algorithms", "System Design", "Programming Languages"],
        "practices": ["Clean Code", "Testing", "Version Control", "CI/CD"],
        "soft_skills": ["Problem Solving", "Communication", "Collaboration"],
        "evaluation_weights": {
            "technical_depth": 0.4,
            "coding_practices": 0.3,
            "system_thinking": 0.3
        }
    },
    "Data Scientist": {
        "core_skills": ["Statistics", "Machine Learning", "Data Analysis", "Feature Engineering"],
        "practices": ["Model Evaluation", "Data Preprocessing", "Experiment Design"],
        "soft_skills": ["Research", "Data Visualization", "Business Understanding"],
        "evaluation_weights": {
            "analytical_thinking": 0.4,
            "technical_knowledge": 0.3,
            "research_methodology": 0.3
        }
    },
    "DevOps Engineer": {
        "core_skills": ["Infrastructure", "Automation", "Cloud Services", "CI/CD"],
        "practices": ["Monitoring", "Security", "Scalability", "Reliability"],
        "soft_skills": ["Troubleshooting", "Documentation", "Incident Response"],
        "evaluation_weights": {
            "infrastructure_knowledge": 0.4,
            "automation_skills": 0.3,
            "operational_excellence": 0.3
        }
    },
    "QA Engineer": {
        "core_skills": ["Test Design", "Test Automation", "Bug Tracking", "Test Coverage"],
        "practices": ["Test Planning", "Quality Metrics", "Test Frameworks"],
        "soft_skills": ["Attention to Detail", "Process Improvement", "Risk Assessment"],
        "evaluation_weights": {
            "testing_methodology": 0.4,
            "automation_expertise": 0.3,
            "quality_mindset": 0.3
        }
    }
}

# Experience level expectations
EXPERIENCE_CRITERIA = {
    "0-2 years": {
        "base_score": 6.0,
        "threshold": 0.7,
        "expectations": {
            "knowledge": "Basic understanding of fundamentals",
            "independence": "Works with guidance",
            "complexity": "Handles simple tasks",
            "leadership": "Learns from team"
        }
    },
    "2-5 years": {
        "base_score": 7.0,
        "threshold": 0.75,
        "expectations": {
            "knowledge": "Good grasp of concepts",
            "independence": "Works independently",
            "complexity": "Handles moderate complexity",
            "leadership": "Mentors juniors"
        }
    },
    "5-8 years": {
        "base_score": 8.0,
        "threshold": 0.8,
        "expectations": {
            "knowledge": "Deep technical expertise",
            "independence": "Fully autonomous",
            "complexity": "Handles complex projects",
            "leadership": "Technical leadership"
        }
    },
    "8+ years": {
        "base_score": 8.5,
        "threshold": 0.85,
        "expectations": {
            "knowledge": "Expert level understanding",
            "independence": "Strategic thinking",
            "complexity": "Architects solutions",
            "leadership": "Drives innovation"
        }
    }
}

# Interview type focus areas
INTERVIEW_FOCUS = {
    "Technical": {
        "primary": "technical_skills",
        "secondary": "problem_solving",
        "evaluation_aspects": [
            "Technical depth",
            "Code quality",
            "Architecture",
            "Best practices"
        ]
    },
    "Behavioral": {
        "primary": "soft_skills",
        "secondary": "experience",
        "evaluation_aspects": [
            "Communication",
            "Leadership",
            "Collaboration",
            "Problem handling"
        ]
    },
    "Problem Solving": {
        "primary": "analytical",
        "secondary": "approach",
        "evaluation_aspects": [
            "Problem breakdown",
            "Solution design",
            "Trade-offs",
            "Implementation"
        ]
    }
}

# Difficulty level modifiers
DIFFICULTY_MODIFIERS = {
    "Easy": {
        "complexity": 0.7,
        "depth": "fundamental concepts",
        "scope": "single concept"
    },
    "Medium": {
        "complexity": 0.85,
        "depth": "applied knowledge",
        "scope": "multiple concepts"
    },
    "Hard": {
        "complexity": 1.0,
        "depth": "advanced topics",
        "scope": "complex scenarios"
    },
    "Legend": {
        "complexity": 1.2,
        "depth": "expert knowledge",
        "scope": "system design"
    }
}
