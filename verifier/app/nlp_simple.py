import re
from typing import List


def simple_keywords(text: str) -> List[str]:
    """
    Extract simple keywords from text using basic NLP techniques
    """
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Split into words
    words = text.split()
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
    }
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)
    
    return unique_keywords[:10]  # Limit to top 10 keywords


def simple_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate simple similarity between two texts using word overlap
    """
    if not text1.strip() or not text2.strip():
        return 0.0
    
    # Get keywords from both texts
    keywords1 = set(simple_keywords(text1))
    keywords2 = set(simple_keywords(text2))
    
    if not keywords1 or not keywords2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = len(keywords1.intersection(keywords2))
    union = len(keywords1.union(keywords2))
    
    return intersection / union if union > 0 else 0.0


def detect_refutation_terms(text: str) -> bool:
    """
    Detect refutation terms in text that might indicate contradiction
    """
    refutation_patterns = [
        r'\bno\b', r'\bnot\b', r'\bnever\b', r'\bnone\b', r'\bnothing\b',
        r'\bdeny\b', r'\bdenies\b', r'\bdenied\b', r'\bdenial\b',
        r'\bdebunk\b', r'\bdebunks\b', r'\bdebunked\b',
        r'\bdisprove\b', r'\bdisproves\b', r'\bdisproven\b',
        r'\bcontrary\b', r'\bcontradict\b', r'\bcontradicts\b',
        r'\bfalse\b', r'\buntrue\b', r'\bincorrect\b', r'\bwrong\b',
        r'\bno evidence\b', r'\black of evidence\b', r'\binsufficient evidence\b'
    ]
    
    text_lower = text.lower()
    for pattern in refutation_patterns:
        if re.search(pattern, text_lower):
            return True
    
    return False
