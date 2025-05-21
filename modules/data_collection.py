#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Data Collection Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module handles data collection from various sources for the Terror Alarm AI system.
"""

import os
import re
import json
import time
import logging
import threading
import requests
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger("TerrorAlarm.DataCollector")

class DataCollector:
    """
    Data collection from various sources for the Terror Alarm AI system.
    """
    
    def __init__(self, config):
        """
        Initialize the DataCollector object.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.running = False
        self.collection_thread = None
        self.last_collection = {}
        
        # Data sources
        self.social_media_sources = []
        self.mainstream_media_sources = []
        self.book_sources = []
        self.custom_sources = []
        
        # Data storage
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data sources from config
        self._initialize_from_config()
        
        logger.info("DataCollector initialized")
    
    def _initialize_from_config(self):
        """Initialize data sources from configuration."""
        # Initialize social media sources
        social_media_sources = self.config.get("data_sources.social_media", [])
        for source in social_media_sources:
            self.add_social_media_source(source)
            
        # Initialize mainstream media sources
        msm_sources = self.config.get("data_sources.mainstream_media", [])
        for source in msm_sources:
            self.add_mainstream_media_source(source)
            
        # Initialize book sources
        book_sources = self.config.get("data_sources.books", [])
        for source in book_sources:
            self.add_book_source(source)
    
    def add_social_media_source(self, source_config: Dict[str, Any]) -> bool:
        """
        Add a social media data source.
        
        Args:
            source_config: Configuration for the social media source
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not source_config.get("enabled", True):
                logger.info(f"Social media source {source_config.get('name')} is disabled")
                return True
                
            self.social_media_sources.append(source_config)
            self.last_collection[source_config["name"]] = datetime.now() - timedelta(days=1)
            logger.info(f"Added social media source: {source_config['name']}")
            return True
        except Exception as e:
            logger.error(f"Error adding social media source: {e}")
            return False
    
    def add_mainstream_media_source(self, source_config: Dict[str, Any]) -> bool:
        """
        Add a mainstream media data source.
        
        Args:
            source_config: Configuration for the mainstream media source
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not source_config.get("enabled", True):
                logger.info(f"Mainstream media source {source_config.get('name')} is disabled")
                return True
                
            self.mainstream_media_sources.append(source_config)
            self.last_collection[source_config["name"]] = datetime.now() - timedelta(days=1)
            logger.info(f"Added mainstream media source: {source_config['name']}")
            return True
        except Exception as e:
            logger.error(f"Error adding mainstream media source: {e}")
            return False
    
    def add_book_source(self, source_config: Dict[str, Any]) -> bool:
        """
        Add a book data source.
        
        Args:
            source_config: Configuration for the book source
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not source_config.get("enabled", True):
                logger.info(f"Book source {source_config.get('name')} is disabled")
                return True
                
            self.book_sources.append(source_config)
            self.last_collection[source_config["name"]] = datetime.now() - timedelta(days=7)
            logger.info(f"Added book source: {source_config['name']}")
            return True
        except Exception as e:
            logger.error(f"Error adding book source: {e}")
            return False
    
    def add_custom_source(self, source_config: Dict[str, Any]) -> bool:
        """
        Add a custom data source.
        
        Args:
            source_config: Configuration for the custom source
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not source_config.get("enabled", True):
                logger.info(f"Custom source {source_config.get('name')} is disabled")
                return True
                
            self.custom_sources.append(source_config)
            self.last_collection[source_config["name"]] = datetime.now() - timedelta(days=1)
            logger.info(f"Added custom source: {source_config['name']}")
            return True
        except Exception as e:
            logger.error(f"Error adding custom source: {e}")
            return False
    
    def start_collection(self):
        """Start the data collection process."""
        if self.running:
            logger.warning("Data collection is already running")
            return
            
        logger.info("Starting data collection")
        self.running = True
        self.collection_thread = threading.Thread(target=self._collection_loop)
        self.collection_thread.daemon = True
        self.collection_thread.start()
    
    def stop_collection(self):
        """Stop the data collection process."""
        if not self.running:
            logger.warning("Data collection is not running")
            return
            
        logger.info("Stopping data collection")
        self.running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=30)
    
    def _collection_loop(self):
        """Main data collection loop."""
        logger.info("Data collection loop started")
        
        while self.running:
            try:
                # Collect data from social media sources
                for source in self.social_media_sources:
                    if self._should_collect(source):
                        self._collect_from_social_media(source)
                
                # Collect data from mainstream media sources
                for source in self.mainstream_media_sources:
                    if self._should_collect(source):
                        self._collect_from_mainstream_media(source)
                
                # Collect data from book sources
                for source in self.book_sources:
                    if self._should_collect(source):
                        self._collect_from_book_source(source)
                
                # Collect data from custom sources
                for source in self.custom_sources:
                    if self._should_collect(source):
                        self._collect_from_custom_source(source)
                
                # Sleep for a while
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in data collection loop: {e}")
                time.sleep(300)  # Sleep for 5 minutes on error
    
    def _should_collect(self, source: Dict[str, Any]) -> bool:
        """
        Check if data should be collected from a source.
        
        Args:
            source: Source configuration
            
        Returns:
            True if data should be collected, False otherwise
        """
        source_name = source.get("name", "unknown")
        
        # Check if source is enabled
        if not source.get("enabled", True):
            return False
        
        # Check if enough time has passed since last collection
        last_time = self.last_collection.get(source_name)
        if not last_time:
            return True
            
        interval = source.get("scrape_interval", 3600)  # Default: 1 hour
        next_time = last_time + timedelta(seconds=interval)
        
        return datetime.now() >= next_time
    
    def _collect_from_social_media(self, source: Dict[str, Any]):
        """
        Collect data from a social media source.
        
        Args:
            source: Social media source configuration
        """
        source_name = source.get("name", "unknown")
        logger.info(f"Collecting data from social media source: {source_name}")
        
        try:
            # This is a placeholder for actual social media API integration
            # In a real system, this would use the appropriate API client
            
            # Simulate data collection
            data = {
                "source": source_name,
                "type": "social_media",
                "timestamp": datetime.now().isoformat(),
                "posts": self._simulate_social_media_data(source_name)
            }
            
            # Save collected data
            self._save_collected_data(source_name, "social_media", data)
            
            # Update last collection time
            self.last_collection[source_name] = datetime.now()
            
            logger.info(f"Collected data from social media source: {source_name}")
        except Exception as e:
            logger.error(f"Error collecting data from social media source {source_name}: {e}")
    
    def _collect_from_mainstream_media(self, source: Dict[str, Any]):
        """
        Collect data from a mainstream media source.
        
        Args:
            source: Mainstream media source configuration
        """
        source_name = source.get("name", "unknown")
        logger.info(f"Collecting data from mainstream media source: {source_name}")
        
        try:
            # This is a placeholder for actual web scraping or API integration
            # In a real system, this would use a web scraper or API client
            
            # Simulate data collection
            data = {
                "source": source_name,
                "type": "mainstream_media",
                "timestamp": datetime.now().isoformat(),
                "articles": self._simulate_mainstream_media_data(source_name)
            }
            
            # Save collected data
            self._save_collected_data(source_name, "mainstream_media", data)
            
            # Update last collection time
            self.last_collection[source_name] = datetime.now()
            
            logger.info(f"Collected data from mainstream media source: {source_name}")
        except Exception as e:
            logger.error(f"Error collecting data from mainstream media source {source_name}: {e}")
    
    def _collect_from_book_source(self, source: Dict[str, Any]):
        """
        Collect data from a book source.
        
        Args:
            source: Book source configuration
        """
        source_name = source.get("name", "unknown")
        logger.info(f"Collecting data from book source: {source_name}")
        
        try:
            # This is a placeholder for actual book data collection
            # In a real system, this would use a web scraper or API client
            
            # Simulate data collection
            data = {
                "source": source_name,
                "type": "book",
                "timestamp": datetime.now().isoformat(),
                "books": self._simulate_book_data(source_name)
            }
            
            # Save collected data
            self._save_collected_data(source_name, "book", data)
            
            # Update last collection time
            self.last_collection[source_name] = datetime.now()
            
            logger.info(f"Collected data from book source: {source_name}")
        except Exception as e:
            logger.error(f"Error collecting data from book source {source_name}: {e}")
    
    def _collect_from_custom_source(self, source: Dict[str, Any]):
        """
        Collect data from a custom source.
        
        Args:
            source: Custom source configuration
        """
        source_name = source.get("name", "unknown")
        logger.info(f"Collecting data from custom source: {source_name}")
        
        try:
            # This is a placeholder for actual custom data collection
            # In a real system, this would use a custom implementation
            
            # Simulate data collection
            data = {
                "source": source_name,
                "type": "custom",
                "timestamp": datetime.now().isoformat(),
                "data": self._simulate_custom_data(source_name)
            }
            
            # Save collected data
            self._save_collected_data(source_name, "custom", data)
            
            # Update last collection time
            self.last_collection[source_name] = datetime.now()
            
            logger.info(f"Collected data from custom source: {source_name}")
        except Exception as e:
            logger.error(f"Error collecting data from custom source {source_name}: {e}")
    
    def _save_collected_data(self, source_name: str, source_type: str, data: Dict[str, Any]):
        """
        Save collected data to disk.
        
        Args:
            source_name: Name of the data source
            source_type: Type of the data source
            data: Collected data
        """
        # Create directory for source type if it doesn't exist
        source_dir = os.path.join(self.data_dir, source_type)
        os.makedirs(source_dir, exist_ok=True)
        
        # Create directory for source if it doesn't exist
        source_dir = os.path.join(source_dir, source_name.lower().replace(' ', '_'))
        os.makedirs(source_dir, exist_ok=True)
        
        # Generate filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.json"
        
        # Save data to file
        file_path = os.path.join(source_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.debug(f"Saved collected data to {file_path}")
    
    def get_new_data(self) -> List[Dict[str, Any]]:
        """
        Get newly collected data.
        
        Returns:
            List of newly collected data
        """
        # This is a placeholder for actual data retrieval
        # In a real system, this would retrieve data from storage
        
        new_data = []
        
        # Collect data from all source directories
        for source_type in ["social_media", "mainstream_media", "book", "custom"]:
            source_dir = os.path.join(self.data_dir, source_type)
            if not os.path.exists(source_dir):
                continue
                
            # Collect data from all source subdirectories
            for source_name in os.listdir(source_dir):
                source_subdir = os.path.join(source_dir, source_name)
                if not os.path.isdir(source_subdir):
                    continue
                    
                # Collect data from all files in the source subdirectory
                for filename in os.listdir(source_subdir):
                    if not filename.endswith(".json"):
                        continue
                        
                    # Check if file is new (created in the last 5 minutes)
                    file_path = os.path.join(source_subdir, filename)
                    file_mtime = os.path.getmtime(file_path)
                    if time.time() - file_mtime > 300:  # 5 minutes
                        continue
                        
                    # Load data from file
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            new_data.append(data)
                    except Exception as e:
                        logger.error(f"Error loading data from {file_path}: {e}")
        
        return new_data
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the data collector.
        
        Returns:
            Dictionary containing the current state
        """
        return {
            "running": self.running,
            "last_collection": {k: v.isoformat() for k, v in self.last_collection.items()},
            "social_media_sources": len(self.social_media_sources),
            "mainstream_media_sources": len(self.mainstream_media_sources),
            "book_sources": len(self.book_sources),
            "custom_sources": len(self.custom_sources)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the data collector.
        
        Returns:
            Dictionary containing the current status
        """
        return {
            "running": self.running,
            "sources": {
                "social_media": [s["name"] for s in self.social_media_sources if s.get("enabled", True)],
                "mainstream_media": [s["name"] for s in self.mainstream_media_sources if s.get("enabled", True)],
                "books": [s["name"] for s in self.book_sources if s.get("enabled", True)],
                "custom": [s["name"] for s in self.custom_sources if s.get("enabled", True)]
            },
            "last_collection": {k: v.isoformat() for k, v in self.last_collection.items()}
        }
    
    # Simulation methods for testing
    def _simulate_social_media_data(self, source_name: str) -> List[Dict[str, Any]]:
        """
        Simulate social media data for testing.
        
        Args:
            source_name: Name of the social media source
            
        Returns:
            List of simulated social media posts
        """
        # This is a placeholder for actual social media data
        # In a real system, this would be replaced with actual data
        
        posts = []
        for i in range(10):
            posts.append({
                "id": f"{source_name.lower()}_post_{i}",
                "user": f"user_{i}",
                "content": f"This is a simulated post from {source_name} #{i}",
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
                "likes": i * 10,
                "shares": i * 5,
                "comments": i * 3
            })
            
        return posts
    
    def _simulate_mainstream_media_data(self, source_name: str) -> List[Dict[str, Any]]:
        """
        Simulate mainstream media data for testing.
        
        Args:
            source_name: Name of the mainstream media source
            
        Returns:
            List of simulated mainstream media articles
        """
        # This is a placeholder for actual mainstream media data
        # In a real system, this would be replaced with actual data
        
        articles = []
        for i in range(5):
            articles.append({
                "id": f"{source_name.lower()}_article_{i}",
                "title": f"Simulated Article {i} from {source_name}",
                "content": f"This is the content of a simulated article from {source_name}. "
                          f"It contains information about various topics and events.",
                "author": f"Author {i}",
                "timestamp": (datetime.now() - timedelta(hours=i * 2)).isoformat(),
                "url": f"https://{source_name.lower().replace(' ', '')}.com/article/{i}"
            })
            
        return articles
    
    def _simulate_book_data(self, source_name: str) -> List[Dict[str, Any]]:
        """
        Simulate book data for testing.
        
        Args:
            source_name: Name of the book source
            
        Returns:
            List of simulated books
        """
        # This is a placeholder for actual book data
        # In a real system, this would be replaced with actual data
        
        books = []
        for i in range(3):
            books.append({
                "id": f"{source_name.lower()}_book_{i}",
                "title": f"Simulated Book {i} from {source_name}",
                "author": f"Author {i}",
                "content": f"This is the content of a simulated book from {source_name}. "
                          f"It contains chapters and information about various topics.",
                "publication_date": f"202{i}-01-01",
                "url": f"https://{source_name.lower().replace(' ', '')}.com/book/{i}"
            })
            
        return books
    
    def _simulate_custom_data(self, source_name: str) -> Dict[str, Any]:
        """
        Simulate custom data for testing.
        
        Args:
            source_name: Name of the custom source
            
        Returns:
            Simulated custom data
        """
        # This is a placeholder for actual custom data
        # In a real system, this would be replaced with actual data
        
        return {
            "id": f"{source_name.lower()}_data",
            "name": source_name,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "field1": "value1",
                "field2": "value2",
                "field3": 123,
                "field4": True
            }
        }


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test data collection
    from config import Configuration
    
    # Create default configuration
    config = Configuration()
    
    # Create data collector
    collector = DataCollector(config)
    
    # Start data collection
    collector.start_collection()
    
    # Wait for a while
    print("Data collection started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # Stop data collection
    collector.stop_collection()
    print("Data collection stopped.")
