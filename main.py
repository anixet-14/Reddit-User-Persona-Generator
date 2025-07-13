#!/usr/bin/env python3
"""
Reddit User Persona Generator

This script scrapes Reddit user profiles and generates detailed user personas
using LLM analysis. It provides a command-line interface for easy usage.

Usage:
    python main.py https://www.reddit.com/user/username/
    python main.py --batch usernames.txt
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from typing import List

from config import setup_logging
from reddit_scraper import RedditScraper
from persona_generator import PersonaGenerator
from utils import validate_reddit_url, extract_username_from_url


def main():
    """Main entry point for the Reddit persona generator."""
    parser = argparse.ArgumentParser(
        description="Generate user personas from Reddit profiles"
    )
    parser.add_argument(
        "url_or_file",
        help="Reddit user profile URL or file containing multiple URLs/usernames"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process multiple users from a file (one per line)"
    )
    parser.add_argument(
        "--output-dir",
        default="./personas",
        help="Directory to save persona files (default: ./personas)"
    )
    parser.add_argument(
        "--max-posts",
        type=int,
        default=100,
        help="Maximum number of posts to analyze (default: 100)"
    )
    parser.add_argument(
        "--max-comments",
        type=int,
        default=200,
        help="Maximum number of comments to analyze (default: 200)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize scrapers
    try:
        reddit_scraper = RedditScraper(
            max_posts=args.max_posts,
            max_comments=args.max_comments
        )
        persona_generator = PersonaGenerator()
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        sys.exit(1)
    
    # Process input
    if args.batch:
        process_batch(args.url_or_file, args.output_dir, reddit_scraper, persona_generator)
    else:
        process_single_user(args.url_or_file, args.output_dir, reddit_scraper, persona_generator)


def process_single_user(url_or_username: str, output_dir: str, reddit_scraper: RedditScraper, persona_generator: PersonaGenerator):
    """Process a single Reddit user."""
    logger = logging.getLogger(__name__)
    
    # Extract username from URL or use directly
    if url_or_username.startswith("http"):
        if not validate_reddit_url(url_or_username):
            logger.error(f"Invalid Reddit URL: {url_or_username}")
            return
        username = extract_username_from_url(url_or_username)
    else:
        username = url_or_username
    
    logger.info(f"Processing user: {username}")
    
    try:
        # Scrape user data
        user_data = reddit_scraper.scrape_user(username)
        
        if not user_data:
            logger.error(f"No data found for user: {username}")
            return
        
        # Generate persona
        persona = persona_generator.generate_persona(user_data)
        
        # Save to file
        output_file = os.path.join(output_dir, f"{username}_persona.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(persona)
        
        logger.info(f"Persona saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error processing user {username}: {e}")


def process_batch(file_path: str, output_dir: str, reddit_scraper: RedditScraper, persona_generator: PersonaGenerator):
    """Process multiple users from a file."""
    logger = logging.getLogger(__name__)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Processing {len(lines)} users from batch file")
        
        for i, line in enumerate(lines, 1):
            logger.info(f"Processing user {i}/{len(lines)}")
            process_single_user(line, output_dir, reddit_scraper, persona_generator)
            
    except FileNotFoundError:
        logger.error(f"Batch file not found: {file_path}")
    except Exception as e:
        logger.error(f"Error processing batch file: {e}")


if __name__ == "__main__":
    main()
