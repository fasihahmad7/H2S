import re
from typing import List, Dict, Any

def extract_scores_from_text(content: str) -> Dict[str, float]:
    """Extract numerical scores from assessment text using targeted parsing."""
    scores = {}
    
    # Define specific patterns for each metric we're looking for
    patterns = {
        'knowledge_depth': [
            r'Knowledge Depth:\s*(\d+(?:\.\d+)?)',
            r'- Knowledge Depth:\s*(\d+(?:\.\d+)?)',
            r'Knowledge.*?(\d+(?:\.\d+)?)/10'
        ],
        'implementation': [
            r'Implementation Understanding:\s*(\d+(?:\.\d+)?)',
            r'- Implementation Understanding:\s*(\d+(?:\.\d+)?)',
            r'Implementation.*?(\d+(?:\.\d+)?)/10'
        ],
        'best_practices': [
            r'Best Practices Awareness:\s*(\d+(?:\.\d+)?)',
            r'- Best Practices Awareness:\s*(\d+(?:\.\d+)?)',
            r'Best Practices.*?(\d+(?:\.\d+)?)/10'
        ],
        'clarity': [
            r'Clarity:\s*(\d+(?:\.\d+)?)',
            r'- Clarity:\s*(\d+(?:\.\d+)?)',
            r'Clarity.*?(\d+(?:\.\d+)?)/10'
        ],
        'structure': [
            r'Structure:\s*(\d+(?:\.\d+)?)',
            r'- Structure:\s*(\d+(?:\.\d+)?)',
            r'Structure.*?(\d+(?:\.\d+)?)/10'
        ],
        'professionalism': [
            r'Professionalism:\s*(\d+(?:\.\d+)?)',
            r'- Professionalism:\s*(\d+(?:\.\d+)?)',
            r'Professionalism.*?(\d+(?:\.\d+)?)/10'
        ],
        'experience_match': [
            r'Score:\s*(\d+(?:\.\d+)?)',
            r'alignment.*?(\d+(?:\.\d+)?)/10',
            r'Experience.*?Score.*?(\d+(?:\.\d+)?)'
        ]
    }
    
    # Extract scores for each category
    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                score = float(match.group(1))
                if 1 <= score <= 10:  # Valid score range
                    scores[category] = score
                    break
    
    # If we couldn't extract specific scores, try a fallback approach
    if not scores:
        # Look for any scores in the text and assign them logically
        all_scores = re.findall(r'\b(\d+(?:\.\d+)?)\b', content)
        valid_scores = [float(s) for s in all_scores if 1 <= float(s) <= 10]
        
        if valid_scores:
            # Assign scores in order of appearance
            if len(valid_scores) >= 1:
                scores['knowledge_depth'] = valid_scores[0]
            if len(valid_scores) >= 2:
                scores['implementation'] = valid_scores[1]
            if len(valid_scores) >= 3:
                scores['best_practices'] = valid_scores[2]
            if len(valid_scores) >= 4:
                scores['clarity'] = valid_scores[3]
            if len(valid_scores) >= 5:
                scores['structure'] = valid_scores[4]
            if len(valid_scores) >= 6:
                scores['professionalism'] = valid_scores[5]
    
    return scores

def calculate_role_specific_metrics(
    role: str,
    experience: str,
    messages: List[Dict[str, Any]]
) -> Dict[str, float]:
    """
    Calculates role-specific metrics based on the interview history.
    Creates a cohesive scoring system where overall score is calculated from components.

    Args:
        role: The job role for the interview.
        experience: The experience level for the interview.
        messages: A list of messages from the interview session.

    Returns:
        A dictionary containing the calculated metrics.
    """
    # Collect all individual scores from assessments
    technical_scores = []  # knowledge_depth, implementation, best_practices
    communication_scores = []  # clarity, structure, professionalism
    experience_scores = []  # experience_match scores
    
    assessment_count = 0

    for message in messages:
        if message.get("role") == "assistant" and message.get("type") == "assessment":
            content = message.get("content", "")
            assessment_count += 1
            
            # Extract scores from this assessment
            scores = extract_scores_from_text(content)
            
            if scores:
                # Technical component scores
                tech_components = []
                if 'knowledge_depth' in scores:
                    tech_components.append(scores['knowledge_depth'])
                if 'implementation' in scores:
                    tech_components.append(scores['implementation'])
                if 'best_practices' in scores:
                    tech_components.append(scores['best_practices'])
                
                if tech_components:
                    technical_scores.append(sum(tech_components) / len(tech_components))
                
                # Communication component scores
                comm_components = []
                if 'clarity' in scores:
                    comm_components.append(scores['clarity'])
                if 'structure' in scores:
                    comm_components.append(scores['structure'])
                if 'professionalism' in scores:
                    comm_components.append(scores['professionalism'])
                
                if comm_components:
                    communication_scores.append(sum(comm_components) / len(comm_components))
                
                # Experience match scores
                if 'experience_match' in scores:
                    experience_scores.append(scores['experience_match'])

    # If no scores were extracted, return zeros
    if not technical_scores and not communication_scores and not experience_scores:
        return {
            "domain_knowledge": 0.0,
            "methodology_understanding": 0.0,
            "practical_experience": 0.0,
            "overall_score": 0.0
        }

    # Calculate component averages with fallbacks
    avg_technical = sum(technical_scores) / len(technical_scores) if technical_scores else 6.0
    avg_communication = sum(communication_scores) / len(communication_scores) if communication_scores else 6.0
    avg_experience = sum(experience_scores) / len(experience_scores) if experience_scores else 6.0

    # Map to our display metrics with logical relationships
    domain_knowledge = avg_technical  # Technical skills represent domain knowledge
    methodology_understanding = avg_communication  # Communication shows methodology understanding
    practical_experience = avg_experience  # Experience match shows practical experience
    
    # Calculate overall score as weighted average of components
    # Technical skills are most important, followed by experience, then communication
    overall_score = (
        domain_knowledge * 0.5 +  # 50% weight on technical/domain knowledge
        practical_experience * 0.3 +  # 30% weight on experience match
        methodology_understanding * 0.2  # 20% weight on communication/methodology
    )

    result = {
        "domain_knowledge": round(domain_knowledge, 1),
        "methodology_understanding": round(methodology_understanding, 1),
        "practical_experience": round(practical_experience, 1),
        "overall_score": round(overall_score, 1)
    }
    
    return result