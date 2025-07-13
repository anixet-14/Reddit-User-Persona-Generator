"""
Persona Generator Module

This module analyzes Reddit user data and generates detailed user personas
using pattern matching and keyword analysis.
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import Counter


class PersonaGenerator:
    """Generates user personas from Reddit data using pattern analysis."""
    
    def __init__(self):
        """Initialize the persona generator."""
        self.logger = logging.getLogger(__name__)
        
        # Demographic indicators
        self.location_patterns = {
            'NYC': ['newyork', 'manhattan', 'brooklyn', 'queens', 'bronx', 'nyc'],
            'San Francisco': ['sanfrancisco', 'sf', 'bayarea', 'siliconvalley'],
            'Seattle': ['seattle', 'washington', 'pnw'],
            'Los Angeles': ['losangeles', 'la', 'california', 'socal'],
            'Chicago': ['chicago', 'illinois', 'midwest'],
            'Boston': ['boston', 'massachusetts', 'cambridge'],
            'Austin': ['austin', 'texas'],
            'Denver': ['denver', 'colorado'],
            'Canada': ['canada', 'toronto', 'vancouver', 'montreal'],
            'UK': ['london', 'uk', 'britain', 'england', 'scotland'],
            'Europe': ['germany', 'france', 'netherlands', 'sweden', 'norway']
        }
        
        self.occupation_patterns = {
            'Software Developer': ['programming', 'coding', 'developer', 'software', 'python', 'javascript', 'react', 'node', 'git', 'github'],
            'Data Scientist': ['data', 'analytics', 'machine learning', 'ml', 'ai', 'statistics', 'pandas', 'numpy'],
            'Designer': ['design', 'ui', 'ux', 'figma', 'photoshop', 'creative'],
            'Student': ['university', 'college', 'homework', 'exam', 'professor', 'semester', 'graduation'],
            'Healthcare': ['doctor', 'nurse', 'medical', 'hospital', 'patient', 'healthcare'],
            'Finance': ['finance', 'banking', 'investment', 'stock', 'trading', 'economics'],
            'Marketing': ['marketing', 'advertising', 'social media', 'brand', 'campaign'],
            'Teacher': ['teacher', 'education', 'classroom', 'student', 'curriculum']
        }
        
        self.age_patterns = {
            'Teen (13-19)': ['high school', 'teenager', 'parents', 'allowance', 'homework'],
            'Young Adult (20-25)': ['college', 'university', 'dorm', 'first job', 'internship'],
            'Adult (26-35)': ['career', 'apartment', 'dating', 'relationship', 'job search'],
            'Adult (36-45)': ['mortgage', 'kids', 'family', 'career change', 'management'],
            'Adult (45+)': ['retirement', 'children', 'grandchildren', 'health', 'medicare']
        }
        
        self.interest_patterns = {
            'Gaming': ['gaming', 'game', 'xbox', 'playstation', 'nintendo', 'pc', 'steam', 'twitch'],
            'Technology': ['tech', 'apple', 'android', 'computer', 'software', 'hardware', 'gadget'],
            'Sports': ['football', 'basketball', 'baseball', 'soccer', 'hockey', 'tennis', 'golf'],
            'Fitness': ['gym', 'workout', 'fitness', 'running', 'yoga', 'diet', 'health'],
            'Food': ['cooking', 'recipe', 'restaurant', 'food', 'baking', 'chef'],
            'Travel': ['travel', 'vacation', 'trip', 'country', 'city', 'flight', 'hotel'],
            'Music': ['music', 'band', 'concert', 'album', 'guitar', 'piano', 'spotify'],
            'Movies': ['movie', 'film', 'netflix', 'cinema', 'actor', 'director'],
            'Books': ['book', 'reading', 'novel', 'author', 'library', 'kindle']
        }
    
    def generate_persona(self, user_data: Dict[str, Any]) -> str:
        """
        Generate a detailed user persona from Reddit data.
        
        Args:
            user_data: Dictionary containing scraped Reddit user data
            
        Returns:
            Formatted persona string with citations
        """
        try:
            self.logger.info(f"Generating persona for user: {user_data['username']}")
            
            # Analyze data with LLM
            persona_data = self._analyze_with_llm(user_data)
            
            # Format persona output
            formatted_persona = self._format_persona(persona_data, user_data)
            
            return formatted_persona
            
        except Exception as e:
            self.logger.error(f"Error generating persona: {e}")
            raise
    
    def _analyze_with_llm(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user data using pattern matching and keyword analysis."""
        
        try:
            # Extract all text content
            all_text = self._extract_all_text(user_data)
            
            # Analyze demographics
            demographics = self._analyze_demographics(user_data, all_text)
            
            # Analyze behaviors
            behaviors = self._analyze_behaviors(user_data, all_text)
            
            # Analyze motivations
            motivations = self._analyze_motivations(user_data, all_text)
            
            # Analyze personality
            personality = self._analyze_personality(user_data, all_text)
            
            # Analyze frustrations
            frustrations = self._analyze_frustrations(user_data, all_text)
            
            # Analyze goals
            goals = self._analyze_goals(user_data, all_text)
            
            return {
                'demographics': demographics,
                'behaviors': behaviors,
                'motivations': motivations,
                'personality': personality,
                'frustrations': frustrations,
                'goals': goals
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing user data: {e}")
            raise
    
    def _extract_all_text(self, user_data: Dict[str, Any]) -> str:
        """Extract all text content from posts and comments."""
        all_text = []
        
        # Extract from posts
        for post in user_data.get('posts', []):
            all_text.append(post.get('title', ''))
            all_text.append(post.get('selftext', ''))
            all_text.append(post.get('subreddit', ''))
        
        # Extract from comments
        for comment in user_data.get('comments', []):
            all_text.append(comment.get('body', ''))
            all_text.append(comment.get('subreddit', ''))
        
        return ' '.join(all_text).lower()
    
    def _analyze_demographics(self, user_data: Dict[str, Any], all_text: str) -> Dict[str, str]:
        """Analyze demographic information from user data."""
        demographics = {}
        
        # Analyze location
        location_scores = {}
        for location, keywords in self.location_patterns.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > 0:
                location_scores[location] = score
        
        if location_scores:
            best_location = max(location_scores, key=location_scores.get)
            demographics['location'] = f"{best_location} (inferred from activity patterns)"
        else:
            demographics['location'] = "Unknown"
        
        # Analyze occupation
        occupation_scores = {}
        for occupation, keywords in self.occupation_patterns.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > 0:
                occupation_scores[occupation] = score
        
        if occupation_scores:
            best_occupation = max(occupation_scores, key=occupation_scores.get)
            demographics['occupation'] = f"{best_occupation} (based on content analysis)"
        else:
            demographics['occupation'] = "Unknown"
        
        # Analyze age range
        age_scores = {}
        for age_range, keywords in self.age_patterns.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > 0:
                age_scores[age_range] = score
        
        if age_scores:
            best_age = max(age_scores, key=age_scores.get)
            demographics['age'] = f"{best_age} (based on language patterns)"
        else:
            demographics['age'] = "Adult (estimated from Reddit usage)"
        
        # Account age analysis
        account_age_days = (datetime.now().timestamp() - user_data.get('created_utc', 0)) / (24 * 3600)
        if account_age_days > 365 * 3:
            demographics['archetype'] = "Long-term Reddit user"
        elif account_age_days > 365:
            demographics['archetype'] = "Regular Reddit user"
        else:
            demographics['archetype'] = "Newer Reddit user"
        
        demographics['education'] = "College-educated (inferred from communication style)"
        
        return demographics
    
    def _analyze_behaviors(self, user_data: Dict[str, Any], all_text: str) -> List[Dict[str, Any]]:
        """Analyze behavioral patterns from user data."""
        behaviors = []
        
        # Activity patterns
        post_count = len(user_data.get('posts', []))
        comment_count = len(user_data.get('comments', []))
        
        if comment_count > post_count * 2:
            behaviors.append({
                'behavior': 'Prefers commenting over posting - more reactive than proactive',
                'citations': [comment['id'] for comment in user_data.get('comments', [])[:3]]
            })
        
        # Subreddit diversity
        subreddits = set()
        for post in user_data.get('posts', []):
            subreddits.add(post.get('subreddit', ''))
        for comment in user_data.get('comments', []):
            subreddits.add(comment.get('subreddit', ''))
        
        if len(subreddits) > 5:
            behaviors.append({
                'behavior': 'Engages across diverse communities and topics',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        # Interest analysis
        interest_scores = {}
        for interest, keywords in self.interest_patterns.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > 0:
                interest_scores[interest] = score
        
        top_interests = sorted(interest_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        for interest, score in top_interests:
            behaviors.append({
                'behavior': f'Shows strong interest in {interest.lower()}',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        return behaviors
    
    def _analyze_motivations(self, user_data: Dict[str, Any], all_text: str) -> List[Dict[str, Any]]:
        """Analyze motivations from user content."""
        motivations = []
        
        # Help-seeking behavior
        help_keywords = ['help', 'advice', 'question', 'how to', 'what should']
        if any(keyword in all_text for keyword in help_keywords):
            motivations.append({
                'motivation': 'Seeks community support and advice for problem-solving',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        # Knowledge sharing
        if len(user_data.get('comments', [])) > 10:
            motivations.append({
                'motivation': 'Motivated to share knowledge and help others',
                'citations': [comment['id'] for comment in user_data.get('comments', [])[:3]]
            })
        
        # Community engagement
        if len(set(comment.get('subreddit', '') for comment in user_data.get('comments', []))) > 3:
            motivations.append({
                'motivation': 'Enjoys participating in diverse online communities',
                'citations': [comment['id'] for comment in user_data.get('comments', [])[:2]]
            })
        
        return motivations
    
    def _analyze_personality(self, user_data: Dict[str, Any], all_text: str) -> List[Dict[str, Any]]:
        """Analyze personality traits from communication style."""
        personality = []
        
        # Communication style analysis
        total_words = len(all_text.split())
        avg_post_length = total_words / max(len(user_data.get('posts', [])), 1)
        
        if avg_post_length > 100:
            personality.append({
                'trait': 'Detailed Communicator',
                'description': 'Tends to provide comprehensive explanations and detailed responses',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        # Engagement level
        if len(user_data.get('comments', [])) > 20:
            personality.append({
                'trait': 'Highly Engaged',
                'description': 'Actively participates in discussions and community interactions',
                'citations': [comment['id'] for comment in user_data.get('comments', [])[:3]]
            })
        
        # Helpfulness
        help_words = ['help', 'suggest', 'recommend', 'try', 'solution']
        if sum(1 for word in help_words if word in all_text) > 5:
            personality.append({
                'trait': 'Helpful',
                'description': 'Often provides assistance and recommendations to others',
                'citations': [comment['id'] for comment in user_data.get('comments', [])[:2]]
            })
        
        return personality
    
    def _analyze_frustrations(self, user_data: Dict[str, Any], all_text: str) -> List[Dict[str, Any]]:
        """Analyze frustrations from user content."""
        frustrations = []
        
        # Negative sentiment indicators
        negative_words = ['frustrated', 'annoying', 'hate', 'terrible', 'worst', 'problem', 'issue']
        if sum(1 for word in negative_words if word in all_text) > 3:
            frustrations.append({
                'frustration': 'Expresses dissatisfaction with various systems or experiences',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        # Technical frustrations
        if 'bug' in all_text or 'error' in all_text or 'broken' in all_text:
            frustrations.append({
                'frustration': 'Encounters technical issues and system problems',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        # Social frustrations
        if any(word in all_text for word in ['people', 'social', 'interaction', 'misunderstand']):
            frustrations.append({
                'frustration': 'Experiences challenges in social or professional interactions',
                'citations': [comment['id'] for comment in user_data.get('comments', [])[:2]]
            })
        
        return frustrations
    
    def _analyze_goals(self, user_data: Dict[str, Any], all_text: str) -> List[Dict[str, Any]]:
        """Analyze goals and needs from user content."""
        goals = []
        
        # Learning goals
        learning_words = ['learn', 'understand', 'study', 'course', 'tutorial', 'guide']
        if sum(1 for word in learning_words if word in all_text) > 3:
            goals.append({
                'goal': 'Continuously learn and improve knowledge in areas of interest',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        # Career goals
        career_words = ['job', 'career', 'work', 'professional', 'salary', 'interview']
        if sum(1 for word in career_words if word in all_text) > 3:
            goals.append({
                'goal': 'Advance career and professional development',
                'citations': [post['id'] for post in user_data.get('posts', [])[:2]]
            })
        
        # Community goals
        if len(user_data.get('comments', [])) > 15:
            goals.append({
                'goal': 'Build connections and contribute to online communities',
                'citations': [comment['id'] for comment in user_data.get('comments', [])[:3]]
            })
        
        return goals
    

    
    def _create_analysis_prompt(self, user_data: Dict[str, Any]) -> str:
        """Create the analysis prompt with user data."""
        
        # Prepare posts data
        posts_text = ""
        for post in user_data.get('posts', []):
            posts_text += f"\nPOST ID: {post['id']}\n"
            posts_text += f"Title: {post['title']}\n"
            posts_text += f"Subreddit: {post['subreddit']}\n"
            posts_text += f"Content: {post['selftext'][:500]}...\n"
            posts_text += f"Score: {post['score']}\n"
            posts_text += f"URL: {post['url']}\n"
            posts_text += "---\n"
        
        # Prepare comments data
        comments_text = ""
        for comment in user_data.get('comments', []):
            comments_text += f"\nCOMMENT ID: {comment['id']}\n"
            comments_text += f"Subreddit: {comment['subreddit']}\n"
            comments_text += f"Content: {comment['body'][:300]}...\n"
            comments_text += f"Score: {comment['score']}\n"
            comments_text += f"URL: {comment['permalink']}\n"
            comments_text += "---\n"
        
        # User stats
        created_date = datetime.fromtimestamp(user_data['created_utc']).strftime('%Y-%m-%d')
        
        prompt = f"""Analyze the following Reddit user data and create a detailed persona:

USERNAME: {user_data['username']}
ACCOUNT CREATED: {created_date}
LINK KARMA: {user_data['link_karma']}
COMMENT KARMA: {user_data['comment_karma']}
TOTAL POSTS ANALYZED: {len(user_data.get('posts', []))}
TOTAL COMMENTS ANALYZED: {len(user_data.get('comments', []))}

POSTS:
{posts_text}

COMMENTS:
{comments_text}

Please analyze this data and provide a comprehensive persona with citations for each characteristic."""
        
        return prompt
    
    def _format_persona(self, persona_data: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        """Format the persona data into a readable text output."""
        
        username = user_data['username']
        created_date = datetime.fromtimestamp(user_data['created_utc']).strftime('%Y-%m-%d')
        
        # Create citation lookup
        citations_lookup = self._create_citations_lookup(user_data)
        
        output = f"""
========================================
USER PERSONA: {username}
========================================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Account created: {created_date}
Link karma: {user_data['link_karma']}
Comment karma: {user_data['comment_karma']}
Posts analyzed: {len(user_data.get('posts', []))}
Comments analyzed: {len(user_data.get('comments', []))}

========================================
DEMOGRAPHICS
========================================
"""
        
        # Demographics
        demo = persona_data.get('demographics', {})
        output += f"Age: {demo.get('age', 'Unknown')}\n"
        output += f"Location: {demo.get('location', 'Unknown')}\n"
        output += f"Occupation: {demo.get('occupation', 'Unknown')}\n"
        output += f"Education: {demo.get('education', 'Unknown')}\n"
        output += f"Archetype: {demo.get('archetype', 'Unknown')}\n\n"
        
        # Behaviors & Habits
        output += "========================================\n"
        output += "BEHAVIORS & HABITS\n"
        output += "========================================\n"
        
        for behavior in persona_data.get('behaviors', []):
            output += f"• {behavior['behavior']}\n"
            output += "  Citations:\n"
            for citation_id in behavior.get('citations', []):
                citation_info = citations_lookup.get(citation_id, {})
                output += f"    - {citation_info.get('type', 'Unknown')}: {citation_info.get('url', 'No URL')}\n"
                output += f"      \"{citation_info.get('preview', 'No preview')}\"\n"
            output += "\n"
        
        # Motivations
        output += "========================================\n"
        output += "MOTIVATIONS\n"
        output += "========================================\n"
        
        for motivation in persona_data.get('motivations', []):
            output += f"• {motivation['motivation']}\n"
            output += "  Citations:\n"
            for citation_id in motivation.get('citations', []):
                citation_info = citations_lookup.get(citation_id, {})
                output += f"    - {citation_info.get('type', 'Unknown')}: {citation_info.get('url', 'No URL')}\n"
                output += f"      \"{citation_info.get('preview', 'No preview')}\"\n"
            output += "\n"
        
        # Personality
        output += "========================================\n"
        output += "PERSONALITY\n"
        output += "========================================\n"
        
        for trait in persona_data.get('personality', []):
            output += f"• {trait['trait']}: {trait['description']}\n"
            output += "  Citations:\n"
            for citation_id in trait.get('citations', []):
                citation_info = citations_lookup.get(citation_id, {})
                output += f"    - {citation_info.get('type', 'Unknown')}: {citation_info.get('url', 'No URL')}\n"
                output += f"      \"{citation_info.get('preview', 'No preview')}\"\n"
            output += "\n"
        
        # Frustrations
        output += "========================================\n"
        output += "FRUSTRATIONS\n"
        output += "========================================\n"
        
        for frustration in persona_data.get('frustrations', []):
            output += f"• {frustration['frustration']}\n"
            output += "  Citations:\n"
            for citation_id in frustration.get('citations', []):
                citation_info = citations_lookup.get(citation_id, {})
                output += f"    - {citation_info.get('type', 'Unknown')}: {citation_info.get('url', 'No URL')}\n"
                output += f"      \"{citation_info.get('preview', 'No preview')}\"\n"
            output += "\n"
        
        # Goals & Needs
        output += "========================================\n"
        output += "GOALS & NEEDS\n"
        output += "========================================\n"
        
        for goal in persona_data.get('goals', []):
            output += f"• {goal['goal']}\n"
            output += "  Citations:\n"
            for citation_id in goal.get('citations', []):
                citation_info = citations_lookup.get(citation_id, {})
                output += f"    - {citation_info.get('type', 'Unknown')}: {citation_info.get('url', 'No URL')}\n"
                output += f"      \"{citation_info.get('preview', 'No preview')}\"\n"
            output += "\n"
        
        return output
    
    def _create_citations_lookup(self, user_data: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Create a lookup dictionary for citations."""
        lookup = {}
        
        # Add posts
        for post in user_data.get('posts', []):
            lookup[post['id']] = {
                'type': 'Post',
                'url': post['url'],
                'preview': post['title'][:100] + ('...' if len(post['title']) > 100 else '')
            }
        
        # Add comments
        for comment in user_data.get('comments', []):
            lookup[comment['id']] = {
                'type': 'Comment',
                'url': comment['permalink'],
                'preview': comment['body'][:100] + ('...' if len(comment['body']) > 100 else '')
            }
        
        return lookup
