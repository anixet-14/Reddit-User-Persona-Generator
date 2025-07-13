"""
Utility Functions

This module contains utility functions for URL validation, text processing,
and other helper functions used throughout the application.
"""

import re
import logging
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse


def validate_reddit_url(url: str) -> bool:
    """
    Validate if a URL is a valid Reddit user profile URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid Reddit user URL, False otherwise
    """
    pattern = r'^https?://(www\.)?reddit\.com/user/[a-zA-Z0-9_-]+/?$'
    return bool(re.match(pattern, url))


def extract_username_from_url(url: str) -> Optional[str]:
    """
    Extract username from Reddit user profile URL.
    
    Args:
        url: Reddit user profile URL
        
    Returns:
        Username if valid URL, None otherwise
    """
    try:
        parsed = urlparse(url)
        if parsed.netloc in ['reddit.com', 'www.reddit.com']:
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) >= 2 and path_parts[0] == 'user':
                return path_parts[1]
    except Exception:
        pass
    
    return None


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing line breaks.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to specified maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove any remaining non-printable characters
    sanitized = re.sub(r'[^\w\s\-_\.]', '', sanitized)
    
    # Replace multiple underscores/spaces with single underscore
    sanitized = re.sub(r'[_\s]+', '_', sanitized)
    
    return sanitized.strip('_')


def format_timestamp(timestamp: float) -> str:
    """
    Format Unix timestamp to human-readable string.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted date string
    """
    from datetime import datetime
    
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "Unknown"


def calculate_account_age(created_utc: float) -> str:
    """
    Calculate account age from creation timestamp.
    
    Args:
        created_utc: Account creation timestamp
        
    Returns:
        Human-readable account age
    """
    from datetime import datetime
    
    try:
        created_date = datetime.fromtimestamp(created_utc)
        current_date = datetime.now()
        delta = current_date - created_date
        
        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = delta.days % 30
        
        if years > 0:
            return f"{years} year{'s' if years > 1 else ''}, {months} month{'s' if months > 1 else ''}"
        elif months > 0:
            return f"{months} month{'s' if months > 1 else ''}, {days} day{'s' if days > 1 else ''}"
        else:
            return f"{days} day{'s' if days > 1 else ''}"
    except Exception:
        return "Unknown"


def get_top_subreddits(posts: List[Dict[str, Any]], comments: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get top subreddits by activity.
    
    Args:
        posts: List of posts
        comments: List of comments
        limit: Maximum number of subreddits to return
        
    Returns:
        List of top subreddits with activity counts
    """
    subreddit_counts = {}
    
    # Count posts
    for post in posts:
        subreddit = post.get('subreddit', '')
        if subreddit:
            if subreddit not in subreddit_counts:
                subreddit_counts[subreddit] = {'posts': 0, 'comments': 0}
            subreddit_counts[subreddit]['posts'] += 1
    
    # Count comments
    for comment in comments:
        subreddit = comment.get('subreddit', '')
        if subreddit:
            if subreddit not in subreddit_counts:
                subreddit_counts[subreddit] = {'posts': 0, 'comments': 0}
            subreddit_counts[subreddit]['comments'] += 1
    
    # Sort by total activity
    sorted_subreddits = sorted(
        subreddit_counts.items(),
        key=lambda x: x[1]['posts'] + x[1]['comments'],
        reverse=True
    )
    
    # Format results
    result = []
    for subreddit, counts in sorted_subreddits[:limit]:
        result.append({
            'subreddit': subreddit,
            'posts': counts['posts'],
            'comments': counts['comments'],
            'total': counts['posts'] + counts['comments']
        })
    
    return result


def validate_user_data(user_data: Dict[str, Any]) -> bool:
    """
    Validate user data structure.
    
    Args:
        user_data: User data dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['username', 'created_utc', 'posts', 'comments']
    
    for field in required_fields:
        if field not in user_data:
            return False
    
    # Validate posts structure
    if not isinstance(user_data['posts'], list):
        return False
    
    # Validate comments structure
    if not isinstance(user_data['comments'], list):
        return False
    
    return True


def print_progress(current: int, total: int, prefix: str = "Progress") -> None:
    """
    Print progress bar.
    
    Args:
        current: Current progress
        total: Total items
        prefix: Prefix string
    """
    if total == 0:
        percentage = 100
    else:
        percentage = (current / total) * 100
    
    bar_length = 50
    filled_length = int(bar_length * current // total) if total > 0 else 0
    
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r{prefix}: [{bar}] {percentage:.1f}% ({current}/{total})', end='')
    
    if current == total:
        print()  # New line when complete
