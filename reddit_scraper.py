"""
Reddit Scraper Module

This module handles scraping Reddit user profiles using PRAW (Python Reddit API Wrapper).
It collects posts and comments from users while respecting API rate limits.
"""

import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

import praw
from praw.exceptions import RedditAPIException
from prawcore.exceptions import NotFound, Forbidden
from praw.models import Redditor


class RedditScraper:
    """Scrapes Reddit user profiles and collects posts and comments."""
    
    def __init__(self, max_posts: int = 100, max_comments: int = 200):
        """
        Initialize Reddit scraper.
        
        Args:
            max_posts: Maximum number of posts to scrape
            max_comments: Maximum number of comments to scrape
        """
        self.max_posts = max_posts
        self.max_comments = max_comments
        self.logger = logging.getLogger(__name__)
        
        # Initialize Reddit API client
        self.reddit = self._initialize_reddit()
    
    def _initialize_reddit(self) -> praw.Reddit:
        """Initialize PRAW Reddit instance with credentials."""
        try:
            reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID", ""),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
                user_agent=os.getenv("REDDIT_USER_AGENT", "PersonaGenerator/1.0"),
                username=os.getenv("REDDIT_USERNAME", ""),
                password=os.getenv("REDDIT_PASSWORD", "")
            )
            
            # Test connection
            reddit.user.me()
            self.logger.info("Successfully connected to Reddit API")
            return reddit
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Reddit API: {e}")
            self.logger.info("Trying read-only mode...")
            
            # Try read-only mode
            try:
                reddit = praw.Reddit(
                    client_id=os.getenv("REDDIT_CLIENT_ID", ""),
                    client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
                    user_agent=os.getenv("REDDIT_USER_AGENT", "PersonaGenerator/1.0")
                )
                self.logger.info("Connected to Reddit API in read-only mode")
                return reddit
            except Exception as e2:
                self.logger.error(f"Failed to connect to Reddit API: {e2}")
                raise
    
    def scrape_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a Reddit user's profile data.
        
        Args:
            username: Reddit username to scrape
            
        Returns:
            Dictionary containing user data or None if failed
        """
        try:
            user = self.reddit.redditor(username)
            
            # Check if user exists
            try:
                user.id  # This will raise NotFound if user doesn't exist
            except NotFound:
                self.logger.error(f"User not found: {username}")
                return None
            except Forbidden:
                self.logger.error(f"User profile is private or suspended: {username}")
                return None
            
            self.logger.info(f"Scraping user: {username}")
            
            # Collect user data
            user_data = {
                "username": username,
                "created_utc": user.created_utc,
                "link_karma": getattr(user, 'link_karma', 0),
                "comment_karma": getattr(user, 'comment_karma', 0),
                "posts": self._scrape_posts(user),
                "comments": self._scrape_comments(user)
            }
            
            self.logger.info(f"Scraped {len(user_data['posts'])} posts and {len(user_data['comments'])} comments")
            return user_data
            
        except Exception as e:
            self.logger.error(f"Error scraping user {username}: {e}")
            return None
    
    def _scrape_posts(self, user: Redditor) -> List[Dict[str, Any]]:
        """Scrape user's posts."""
        posts = []
        
        try:
            self.logger.info(f"Scraping posts for user: {user.name}")
            
            for submission in user.submissions.new(limit=self.max_posts):
                try:
                    post_data = {
                        "id": submission.id,
                        "title": submission.title,
                        "selftext": submission.selftext,
                        "subreddit": str(submission.subreddit),
                        "score": submission.score,
                        "created_utc": submission.created_utc,
                        "url": f"https://reddit.com{submission.permalink}",
                        "num_comments": submission.num_comments,
                        "upvote_ratio": getattr(submission, 'upvote_ratio', None)
                    }
                    posts.append(post_data)
                    
                    # Rate limiting
                    time.sleep(0.05)
                    
                except Exception as e:
                    self.logger.warning(f"Error scraping post {submission.id}: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error scraping posts: {e}")
        
        return posts
    
    def _scrape_comments(self, user: Redditor) -> List[Dict[str, Any]]:
        """Scrape user's comments."""
        comments = []
        
        try:
            self.logger.info(f"Scraping comments for user: {user.name}")
            
            for comment in user.comments.new(limit=self.max_comments):
                try:
                    comment_data = {
                        "id": comment.id,
                        "body": comment.body,
                        "subreddit": str(comment.subreddit),
                        "score": comment.score,
                        "created_utc": comment.created_utc,
                        "permalink": f"https://reddit.com{comment.permalink}",
                        "submission_title": comment.submission.title if hasattr(comment, 'submission') else None,
                        "submission_id": comment.submission.id if hasattr(comment, 'submission') else None
                    }
                    comments.append(comment_data)
                    
                    # Rate limiting
                    time.sleep(0.05)
                    
                except Exception as e:
                    self.logger.warning(f"Error scraping comment {comment.id}: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error scraping comments: {e}")
        
        return comments
    
    def get_user_stats(self, username: str) -> Optional[Dict[str, Any]]:
        """Get basic user statistics."""
        try:
            user = self.reddit.redditor(username)
            
            return {
                "username": username,
                "created_utc": user.created_utc,
                "link_karma": getattr(user, 'link_karma', 0),
                "comment_karma": getattr(user, 'comment_karma', 0),
                "is_gold": getattr(user, 'is_gold', False),
                "is_mod": getattr(user, 'is_mod', False),
                "has_verified_email": getattr(user, 'has_verified_email', False)
            }
        except Exception as e:
            self.logger.error(f"Error getting user stats for {username}: {e}")
            return None
