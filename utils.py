#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Utilities Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module provides utility functions for the Terror Alarm AI system.
"""

import os
import re
import json
import hashlib
import logging
import datetime
import requests
from typing import Any, Dict, List, Optional, Union, Tuple

logger = logging.getLogger("TerrorAlarm.Utils")

class Utils:
    """
    Utility functions for the Terror Alarm AI system.
    """
    
    def __init__(self):
        """Initialize the Utils object."""
        logger.debug("Utils initialized")
    
    @staticmethod
    def generate_hash(data: str) -> str:
        """
        Generate a SHA-256 hash of the given data.
        
        Args:
            data: Data to hash
            
        Returns:
            SHA-256 hash as a hexadecimal string
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Sanitize text by removing special characters and normalizing whitespace.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-printable characters
        text = ''.join(c for c in text if c.isprintable() or c.isspace())
        
        return text.strip()
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract URLs from text.
        
        Args:
            text: Text to extract URLs from
            
        Returns:
            List of extracted URLs
        """
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        return url_pattern.findall(text)
    
    @staticmethod
    def extract_entities(text: str) -> List[str]:
        """
        Extract named entities from text using simple pattern matching.
        This is a basic implementation and should be replaced with a proper NER model.
        
        Args:
            text: Text to extract entities from
            
        Returns:
            List of extracted entities
        """
        # This is a placeholder for a proper NER implementation
        # In a real system, this would use a trained NER model
        
        # Simple pattern for organization names (capitalized words)
        org_pattern = re.compile(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b')
        
        # Extract potential organizations
        orgs = org_pattern.findall(text)
        
        return list(set(orgs))
    
    @staticmethod
    def download_file(url: str, save_path: str) -> bool:
        """
        Download a file from a URL.
        
        Args:
            url: URL to download from
            save_path: Path to save the file to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            logger.info(f"Downloaded {url} to {save_path}")
            return True
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return False
    
    @staticmethod
    def load_json(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON from a file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Loaded JSON data or None if failed
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON from {file_path}: {e}")
            return None
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> bool:
        """
        Save JSON data to a file.
        
        Args:
            data: JSON data to save
            file_path: Path to save the JSON file to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving JSON to {file_path}: {e}")
            return False
    
    @staticmethod
    def get_timestamp() -> str:
        """
        Get the current timestamp as an ISO 8601 string.
        
        Returns:
            Current timestamp as an ISO 8601 string
        """
        return datetime.datetime.now().isoformat()
    
    @staticmethod
    def parse_timestamp(timestamp: str) -> Optional[datetime.datetime]:
        """
        Parse an ISO 8601 timestamp string.
        
        Args:
            timestamp: ISO 8601 timestamp string
            
        Returns:
            Parsed datetime object or None if failed
        """
        try:
            return datetime.datetime.fromisoformat(timestamp)
        except Exception as e:
            logger.error(f"Error parsing timestamp {timestamp}: {e}")
            return None
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate the similarity between two texts using Jaccard similarity.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        # Tokenize texts
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        
        # Calculate Jaccard similarity
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        if union == 0:
            return 0.0
            
        return intersection / union
    
    @staticmethod
    def format_date(date: datetime.datetime, format_str: str = "%Y-%m-%d") -> str:
        """
        Format a datetime object as a string.
        
        Args:
            date: Datetime object to format
            format_str: Format string
            
        Returns:
            Formatted date string
        """
        return date.strftime(format_str)
    
    @staticmethod
    def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime.datetime]:
        """
        Parse a date string.
        
        Args:
            date_str: Date string to parse
            format_str: Format string
            
        Returns:
            Parsed datetime object or None if failed
        """
        try:
            return datetime.datetime.strptime(date_str, format_str)
        except Exception as e:
            logger.error(f"Error parsing date {date_str}: {e}")
            return None


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test utility functions
    utils = Utils()
    
    # Test hash generation
    text = "Terror Alarm AI"
    hash_value = utils.generate_hash(text)
    print(f"Hash of '{text}': {hash_value}")
    
    # Test text sanitization
    html_text = "<p>This is <b>HTML</b> text with\n\nmultiple\twhitespace.</p>"
    sanitized = utils.sanitize_text(html_text)
    print(f"Sanitized text: '{sanitized}'")
    
    # Test URL extraction
    url_text = "Visit https://example.com and http://test.org for more information."
    urls = utils.extract_urls(url_text)
    print(f"Extracted URLs: {urls}")
    
    # Test timestamp
    timestamp = utils.get_timestamp()
    print(f"Current timestamp: {timestamp}")
    parsed = utils.parse_timestamp(timestamp)
    print(f"Parsed timestamp: {parsed}")
