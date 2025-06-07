import google.generativeai as genai
import json
from typing import Dict, List, Optional, Any
import numpy as np

class InterviewAnalyzer:
    def __init__(self, model):
        self.model = model
        self.performance_weights = {
            'verbal_content': 0.4,
            'non_verbal': 0.3,
            'voice_quality': 0.3
        }
        
    def _analyze_non_verbal_cues(self, video_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze non-verbal communication aspects."""
        if not video_metrics:
            return {
                'score': 0,
                'feedback': 'No video analysis available'
            }
            
        attention_score = np.mean(video_metrics.get('attention_scores', [0]))
        eye_contact_score = np.mean(video_metrics.get('eye_contact_scores', [0]))
        confidence_score = np.mean(video_metrics.get('confidence_scores', [0]))
        
        non_verbal_score = (attention_score + eye_contact_score + confidence_score) / 3
        
        feedback = []
        if attention_score < 0.7:
            feedback.append("Work on maintaining consistent focus during the interview")
        if eye_contact_score < 0.7:
            feedback.append("Improve eye contact with the camera")
        if confidence_score < 0.7:
            feedback.append("Display more confident body language and posture")
            
        return {
            'score': non_verbal_score,
            'feedback': feedback if feedback else ['Good non-verbal communication']
        }
    
    def _analyze_voice_qualities(self, audio_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze voice and speech patterns."""
        if not audio_metrics:
            return {
                'score': 0,
                'feedback': 'No audio analysis available'
            }
            
        clarity_score = np.mean(audio_metrics.get('clarity_score', [0]))
        avg_wpm = np.mean(audio_metrics.get('words_per_minute', [0]))
        filler_ratio = sum(audio_metrics.get('filler_words', [0])) / max(len(audio_metrics.get('filler_words', [1])), 1)
        
        # Score calculations
        clarity_weight = 0.4
        pace_weight = 0.3
        filler_weight = 0.3
        
        pace_score = 1.0 - min(abs(avg_wpm - 135) / 50, 1.0)  # Optimal WPM around 135
        filler_score = 1.0 - min(filler_ratio, 1.0)
        
        voice_score = (clarity_score * clarity_weight + 
                      pace_score * pace_weight + 
                      filler_score * filler_weight)
        
        feedback = []
        if clarity_score < 0.7:
            feedback.append("Work on speaking more clearly and distinctly")
        if pace_score < 0.7:
            feedback.append(f"Adjust speaking pace (currently {avg_wpm:.0f} WPM, aim for 120-150 WPM)")
        if filler_score < 0.7:
            feedback.append("Reduce use of filler words (um, uh, like, etc.)")
            
        return {
            'score': voice_score,
            'feedback': feedback if feedback else ['Good voice quality and speech patterns']
        }
        
    def analyze_response(self, 
                        job_role: str, 
                        question: str, 
                        answer: str, 
                        video_metrics: Optional[Dict[str, Any]] = None, 
                        audio_metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Comprehensive analysis of interview response combining verbal content,
        non-verbal cues, and voice qualities.
        """
        # Analyze non-verbal aspects
        non_verbal_analysis = self._analyze_non_verbal_cues(video_metrics)
        
        # Analyze voice qualities
        voice_analysis = self._analyze_voice_qualities(audio_metrics)
        
        # Prepare detailed context for AI analysis
        prompt = f"""As an expert interviewer for {job_role} positions, provide a comprehensive evaluation of this interview response.

Question: {question}
Verbal Answer: {answer}

Non-verbal Analysis:
- Attention Score: {video_metrics.get('attention_score', 'N/A')}
- Eye Contact Score: {video_metrics.get('eye_contact_score', 'N/A')}
- Confidence Score: {video_metrics.get('confidence_score', 'N/A')}

Voice Analysis:
- Clarity Score: {audio_metrics.get('avg_clarity', 'N/A')}
- Speaking Pace: {audio_metrics.get('avg_wpm', 'N/A')} WPM
- Filler Words Used: {audio_metrics.get('total_fillers', 'N/A')}

Provide a detailed evaluation in JSON format:
{{
    "content_analysis": {{
        "relevance_score": (1-10),
        "clarity_score": (1-10),
        "structure_score": (1-10),
        "strengths": ["point1", "point2", ...],
        "improvements": ["point1", "point2", ...],
        "example_better_answer": "concise example of an improved answer"
    }},
    "delivery_feedback": {{
        "body_language": ["specific points about posture, expressions, etc."],
        "voice_qualities": ["specific points about tone, pace, clarity, etc."],
        "overall_presence": "analysis of professional presence"
    }},
    "technical_assessment": {{
        "knowledge_depth": (1-10),
        "practical_understanding": (1-10),
        "problem_solving": (1-10)
    }},
    "category": "technical|behavioral|communication",
    "overall_impression": "summary of the complete evaluation"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            ai_feedback = json.loads(response.text)
            
            # Calculate weighted final score
            content_score = (ai_feedback['content_analysis']['relevance_score'] + 
                           ai_feedback['content_analysis']['clarity_score'] + 
                           ai_feedback['content_analysis']['structure_score']) / 3
            
            final_score = (
                content_score * self.performance_weights['verbal_content'] +
                non_verbal_analysis['score'] * self.performance_weights['non_verbal'] +
                voice_analysis['score'] * self.performance_weights['voice_quality']
            )
            
            # Combine all feedback
            return {
                "score": final_score,
                "content_analysis": ai_feedback['content_analysis'],
                "delivery_feedback": {
                    **ai_feedback['delivery_feedback'],
                    "non_verbal_feedback": non_verbal_analysis['feedback'],
                    "voice_feedback": voice_analysis['feedback']
                },
                "technical_assessment": ai_feedback['technical_assessment'],
                "category": ai_feedback['category'],
                "overall_impression": ai_feedback['overall_impression']
            }
            
        except Exception as e:
            return {
                "score": 5.0,
                "content_analysis": {
                    "strengths": ["Unable to analyze completely"],
                    "improvements": ["Technical error in analysis"],
                    "example_better_answer": "Analysis unavailable"
                },
                "delivery_feedback": {
                    "body_language": non_verbal_analysis['feedback'],
                    "voice_feedback": voice_analysis['feedback'],
                    "overall_presence": "Analysis incomplete due to technical error"
                },
                "technical_assessment": {
                    "knowledge_depth": 5,
                    "practical_understanding": 5,
                    "problem_solving": 5
                },
                "category": "error",
                "overall_impression": "Analysis incomplete due to technical error"
            }
