"""
Common utility functions for the AI Interview Assistant.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import speech_recognition as sr

def speech_to_text() -> Optional[str]:
    """
    Record audio from the microphone and convert it to text.
    Returns the recognized text or None if recognition fails.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Speak now.")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError:
            print("Could not request results from the speech recognition service")
            return None
            
    except Exception as e:
        print(f"Error accessing microphone: {str(e)}")
        return None

def calculate_average_metrics(metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    """Calculate average values for a list of metrics."""
    if not metrics_list:
        return {}
        
    result = {}
    for key in metrics_list[0].keys():
        values = [m[key] for m in metrics_list if key in m]
        result[key] = sum(values) / len(values) if values else 0
    return result

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string."""
    duration = timedelta(seconds=seconds)
    if duration.days > 0:
        return f"{duration.days}d {duration.seconds//3600}h"
    elif duration.seconds >= 3600:
        return f"{duration.seconds//3600}h {(duration.seconds//60)%60}m"
    else:
        return f"{duration.seconds//60}m {duration.seconds%60}s"

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely parse JSON string with a default value if parsing fails."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp in consistent way across the application."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def calculate_progress(current: float, target: float) -> Dict[str, Any]:
    """Calculate progress towards a target value."""
    progress = (current / target) if target else 0
    return {
        'percentage': min(progress * 100, 100),
        'status': 'completed' if progress >= 1 else 'in_progress',
        'remaining': max(target - current, 0)
    }

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length while preserving words."""
    if len(text) <= max_length:
        return text
        
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return f"{truncated}..."

def parse_duration_string(duration_str: str) -> int:
    """Parse duration string (e.g., '1h 30m') to seconds."""
    total_seconds = 0
    parts = duration_str.lower().split()
    
    for part in parts:
        if part.endswith('h'):
            total_seconds += int(part[:-1]) * 3600
        elif part.endswith('m'):
            total_seconds += int(part[:-1]) * 60
        elif part.endswith('s'):
            total_seconds += int(part[:-1])
            
    return total_seconds

def get_trend_indicator(current: float, previous: float) -> str:
    """Get trend indicator (↑, ↓, or →) based on value comparison."""
    if current > previous:
        return "↑"
    elif current < previous:
        return "↓"
    return "→"
