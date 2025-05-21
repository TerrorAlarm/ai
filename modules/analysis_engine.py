#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Analysis Engine Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module handles data analysis for the Terror Alarm AI system.
"""

import os
import re
import json
import time
import logging
import threading
import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger("TerrorAlarm.AnalysisEngine")

class AnalysisEngine:
    """
    Data analysis for the Terror Alarm AI system.
    """
    
    def __init__(self, config):
        """
        Initialize the AnalysisEngine object.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.running = False
        self.analysis_thread = None
        self.last_analysis = {}
        
        # Analysis models
        self.sentiment_model = None
        self.entity_model = None
        self.topic_model = None
        
        # Analysis results
        self.results_dir = "data/analysis"
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Country IQ chart
        self.country_iq_chart = {}
        self._load_country_iq_chart()
        
        # Initialize analysis models
        self._initialize_models()
        
        logger.info("AnalysisEngine initialized")
    
    def _initialize_models(self):
        """Initialize analysis models."""
        # Initialize sentiment analysis model
        if self.config.get("analysis.sentiment_analysis.enabled", True):
            logger.info("Initializing sentiment analysis model")
            # This is a placeholder for actual model initialization
            # In a real system, this would load a trained model
            self.sentiment_model = "sentiment_model"
        
        # Initialize entity recognition model
        if self.config.get("analysis.entity_recognition.enabled", True):
            logger.info("Initializing entity recognition model")
            # This is a placeholder for actual model initialization
            # In a real system, this would load a trained model
            self.entity_model = "entity_model"
        
        # Initialize topic modeling
        if self.config.get("analysis.topic_modeling.enabled", True):
            logger.info("Initializing topic modeling")
            # This is a placeholder for actual model initialization
            # In a real system, this would load a trained model
            self.topic_model = "topic_model"
    
    def _load_country_iq_chart(self):
        """Load the country IQ chart from file."""
        iq_chart_path = os.path.join(self.results_dir, "country_iq_chart.json")
        if os.path.exists(iq_chart_path):
            try:
                with open(iq_chart_path, 'r') as f:
                    self.country_iq_chart = json.load(f)
                logger.info(f"Loaded country IQ chart with {len(self.country_iq_chart)} countries")
            except Exception as e:
                logger.error(f"Error loading country IQ chart: {e}")
                self._initialize_country_iq_chart()
        else:
            logger.info("Country IQ chart not found, initializing")
            self._initialize_country_iq_chart()
    
    def _initialize_country_iq_chart(self):
        """Initialize the country IQ chart with default values."""
        # This is a placeholder for actual IQ chart initialization
        # In a real system, this would use actual data
        
        # List of countries
        countries = [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", 
            "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", 
            "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", 
            "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", 
            "Cameroon", "Canada", "Cape Verde", "Central African Republic", "Chad", "Chile", 
            "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", 
            "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", 
            "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", 
            "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", 
            "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", 
            "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", 
            "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", 
            "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", 
            "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", 
            "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
            "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
            "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", 
            "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", 
            "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", 
            "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", 
            "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", 
            "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
            "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", 
            "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", 
            "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", 
            "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", 
            "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", 
            "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", 
            "Zimbabwe"
        ]
        
        # Initialize IQ chart with random values between 70 and 120
        np.random.seed(42)  # For reproducibility
        for country in countries:
            # Baseline IQ between 70 and 120
            base_iq = np.random.normal(100, 10)
            base_iq = max(70, min(120, base_iq))
            self.country_iq_chart[country] = round(base_iq, 1)
        
        # Save the initial IQ chart
        self._save_country_iq_chart()
        
        logger.info(f"Initialized country IQ chart with {len(self.country_iq_chart)} countries")
    
    def _save_country_iq_chart(self):
        """Save the country IQ chart to file."""
        iq_chart_path = os.path.join(self.results_dir, "country_iq_chart.json")
        try:
            with open(iq_chart_path, 'w') as f:
                json.dump(self.country_iq_chart, f, indent=2)
            logger.info(f"Saved country IQ chart to {iq_chart_path}")
        except Exception as e:
            logger.error(f"Error saving country IQ chart: {e}")
    
    def start_analysis(self):
        """Start the data analysis process."""
        if self.running:
            logger.warning("Data analysis is already running")
            return
            
        logger.info("Starting data analysis")
        self.running = True
        self.analysis_thread = threading.Thread(target=self._analysis_loop)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
    
    def stop_analysis(self):
        """Stop the data analysis process."""
        if not self.running:
            logger.warning("Data analysis is not running")
            return
            
        logger.info("Stopping data analysis")
        self.running = False
        if self.analysis_thread:
            self.analysis_thread.join(timeout=30)
    
    def _analysis_loop(self):
        """Main data analysis loop."""
        logger.info("Data analysis loop started")
        
        while self.running:
            try:
                # Process new data
                self._process_new_data()
                
                # Update country IQ chart
                self._update_country_iq_chart()
                
                # Update topic models
                self._update_topic_models()
                
                # Sleep for a while
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in data analysis loop: {e}")
                time.sleep(300)  # Sleep for 5 minutes on error
    
    def _process_new_data(self):
        """Process new data from the data collector."""
        # This is a placeholder for actual data processing
        # In a real system, this would process data from the data collector
        
        # Get data directory
        data_dir = "data"
        if not os.path.exists(data_dir):
            return
            
        # Process data from all source directories
        for source_type in ["social_media", "mainstream_media", "book", "custom"]:
            source_dir = os.path.join(data_dir, source_type)
            if not os.path.exists(source_dir):
                continue
                
            # Process data from all source subdirectories
            for source_name in os.listdir(source_dir):
                source_subdir = os.path.join(source_dir, source_name)
                if not os.path.isdir(source_subdir):
                    continue
                    
                # Process data from all files in the source subdirectory
                for filename in sorted(os.listdir(source_subdir)):
                    if not filename.endswith(".json"):
                        continue
                        
                    # Check if file is new (created in the last 5 minutes)
                    file_path = os.path.join(source_subdir, filename)
                    file_mtime = os.path.getmtime(file_path)
                    if time.time() - file_mtime > 300:  # 5 minutes
                        continue
                        
                    # Check if file has already been processed
                    processed_marker = os.path.join(
                        self.results_dir, 
                        f"processed_{source_type}_{source_name}_{filename}"
                    )
                    if os.path.exists(processed_marker):
                        continue
                        
                    # Load data from file
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            
                        # Process data based on source type
                        if source_type == "social_media":
                            self._process_social_media_data(data)
                        elif source_type == "mainstream_media":
                            self._process_mainstream_media_data(data)
                        elif source_type == "book":
                            self._process_book_data(data)
                        elif source_type == "custom":
                            self._process_custom_data(data)
                            
                        # Mark file as processed
                        with open(processed_marker, 'w') as f:
                            f.write(f"Processed at {datetime.now().isoformat()}")
                            
                        logger.info(f"Processed {file_path}")
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {e}")
    
    def _process_social_media_data(self, data: Dict[str, Any]):
        """
        Process social media data.
        
        Args:
            data: Social media data to process
        """
        # This is a placeholder for actual social media data processing
        # In a real system, this would use the sentiment and entity models
        
        source = data.get("source", "unknown")
        posts = data.get("posts", [])
        
        logger.info(f"Processing {len(posts)} posts from {source}")
        
        # Process each post
        for post in posts:
            # Extract content
            content = post.get("content", "")
            
            # Analyze sentiment
            if self.sentiment_model:
                sentiment = self._analyze_sentiment(content)
                post["sentiment"] = sentiment
            
            # Extract entities
            if self.entity_model:
                entities = self._extract_entities(content)
                post["entities"] = entities
            
            # Extract countries
            countries = self._extract_countries(content)
            post["countries"] = countries
            
            # Update country IQ based on content
            for country in countries:
                self._update_country_iq(country, content)
        
        # Save processed data
        self._save_processed_data(source, "social_media", data)
    
    def _process_mainstream_media_data(self, data: Dict[str, Any]):
        """
        Process mainstream media data.
        
        Args:
            data: Mainstream media data to process
        """
        # This is a placeholder for actual mainstream media data processing
        # In a real system, this would use the sentiment and entity models
        
        source = data.get("source", "unknown")
        articles = data.get("articles", [])
        
        logger.info(f"Processing {len(articles)} articles from {source}")
        
        # Process each article
        for article in articles:
            # Extract content
            content = article.get("content", "")
            
            # Analyze sentiment
            if self.sentiment_model:
                sentiment = self._analyze_sentiment(content)
                article["sentiment"] = sentiment
            
            # Extract entities
            if self.entity_model:
                entities = self._extract_entities(content)
                article["entities"] = entities
            
            # Extract countries
            countries = self._extract_countries(content)
            article["countries"] = countries
            
            # Update country IQ based on content
            for country in countries:
                self._update_country_iq(country, content)
        
        # Save processed data
        self._save_processed_data(source, "mainstream_media", data)
    
    def _process_book_data(self, data: Dict[str, Any]):
        """
        Process book data.
        
        Args:
            data: Book data to process
        """
        # This is a placeholder for actual book data processing
        # In a real system, this would use the sentiment and entity models
        
        source = data.get("source", "unknown")
        books = data.get("books", [])
        
        logger.info(f"Processing {len(books)} books from {source}")
        
        # Process each book
        for book in books:
            # Extract content
            content = book.get("content", "")
            
            # Analyze sentiment
            if self.sentiment_model:
                sentiment = self._analyze_sentiment(content)
                book["sentiment"] = sentiment
            
            # Extract entities
            if self.entity_model:
                entities = self._extract_entities(content)
                book["entities"] = entities
            
            # Extract countries
            countries = self._extract_countries(content)
            book["countries"] = countries
            
            # Update country IQ based on content
            for country in countries:
                self._update_country_iq(country, content)
        
        # Save processed data
        self._save_processed_data(source, "book", data)
    
    def _process_custom_data(self, data: Dict[str, Any]):
        """
        Process custom data.
        
        Args:
            data: Custom data to process
        """
        # This is a placeholder for actual custom data processing
        # In a real system, this would use custom processing logic
        
        source = data.get("source", "unknown")
        
        logger.info(f"Processing custom data from {source}")
        
        # Extract content if available
        if "data" in data and isinstance(data["data"], dict):
            # Process data fields
            for field, value in data["data"].items():
                if isinstance(value, str):
                    # Analyze sentiment
                    if self.sentiment_model:
                        sentiment = self._analyze_sentiment(value)
                        data["data"][f"{field}_sentiment"] = sentiment
                    
                    # Extract entities
                    if self.entity_model:
                        entities = self._extract_entities(value)
                        data["data"][f"{field}_entities"] = entities
                    
                    # Extract countries
                    countries = self._extract_countries(value)
                    data["data"][f"{field}_countries"] = countries
                    
                    # Update country IQ based on content
                    for country in countries:
                        self._update_country_iq(country, value)
        
        # Save processed data
        self._save_processed_data(source, "custom", data)
    
    def _save_processed_data(self, source_name: str, source_type: str, data: Dict[str, Any]):
        """
        Save processed data to disk.
        
        Args:
            source_name: Name of the data source
            source_type: Type of the data source
            data: Processed data
        """
        # Create directory for processed data if it doesn't exist
        processed_dir = os.path.join(self.results_dir, "processed", source_type)
        os.makedirs(processed_dir, exist_ok=True)
        
        # Create directory for source if it doesn't exist
        source_dir = os.path.join(processed_dir, source_name.lower().replace(' ', '_'))
        os.makedirs(source_dir, exist_ok=True)
        
        # Generate filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.json"
        
        # Save data to file
        file_path = os.path.join(source_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.debug(f"Saved processed data to {file_path}")
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing sentiment scores
        """
        # This is a placeholder for actual sentiment analysis
        # In a real system, this would use a trained sentiment model
        
        # Simulate sentiment analysis
        # Generate random sentiment scores
        positive = np.random.random() * 0.5 + 0.25  # Between 0.25 and 0.75
        negative = 1.0 - positive
        
        return {
            "positive": round(positive, 3),
            "negative": round(negative, 3),
            "compound": round(positive - negative, 3)
        }
    
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities from text.
        
        Args:
            text: Text to extract entities from
            
        Returns:
            List of extracted entities
        """
        # This is a placeholder for actual entity extraction
        # In a real system, this would use a trained NER model
        
        # Simulate entity extraction
        entities = []
        
        # Extract potential organizations (capitalized words)
        org_pattern = re.compile(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b')
        orgs = org_pattern.findall(text)
        
        for org in orgs:
            entities.append({
                "text": org,
                "type": "ORG",
                "confidence": round(np.random.random() * 0.3 + 0.7, 3)  # Between 0.7 and 1.0
            })
        
        # Extract potential persons (Mr./Ms./Dr. followed by capitalized words)
        person_pattern = re.compile(r'\b(Mr\.|Ms\.|Dr\.) ([A-Z][a-z]+ [A-Z][a-z]+)\b')
        persons = person_pattern.findall(text)
        
        for title, name in persons:
            entities.append({
                "text": f"{title} {name}",
                "type": "PERSON",
                "confidence": round(np.random.random() * 0.3 + 0.7, 3)  # Between 0.7 and 1.0
            })
        
        return entities
    
    def _extract_countries(self, text: str) -> List[str]:
        """
        Extract country names from text.
        
        Args:
            text: Text to extract countries from
            
        Returns:
            List of extracted countries
        """
        # This is a placeholder for actual country extraction
        # In a real system, this would use a more sophisticated approach
        
        countries = []
        
        # Check for each country in the text
        for country in self.country_iq_chart.keys():
            if re.search(r'\b' + re.escape(country) + r'\b', text, re.IGNORECASE):
                countries.append(country)
        
        return countries
    
    def _update_country_iq(self, country: str, text: str):
        """
        Update country IQ based on text content.
        
        Args:
            country: Country to update
            text: Text content
        """
        # This is a placeholder for actual IQ updating logic
        # In a real system, this would use a more sophisticated approach
        
        if country not in self.country_iq_chart:
            return
        
        # Calculate text quality score (placeholder)
        # In a real system, this would use actual text quality metrics
        text_quality = len(text) / 1000.0  # Longer texts get higher scores
        text_quality = min(1.0, text_quality)  # Cap at 1.0
        
        # Calculate sentiment impact
        sentiment = self._analyze_sentiment(text)
        sentiment_impact = sentiment["compound"]  # Between -1.0 and 1.0
        
        # Calculate overall impact
        impact = text_quality * sentiment_impact
        
        # Update country IQ
        current_iq = self.country_iq_chart[country]
        
        # Small random adjustment based on impact
        adjustment = impact * np.random.random() * 0.1  # Small adjustment
        
        # Apply adjustment
        new_iq = current_iq + adjustment
        
        # Ensure IQ stays within reasonable bounds
        new_iq = max(70.0, min(130.0, new_iq))
        
        # Update IQ chart
        self.country_iq_chart[country] = round(new_iq, 1)
    
    def _update_country_iq_chart(self):
        """Update the country IQ chart based on recent data."""
        # This is a placeholder for actual IQ chart updating
        # In a real system, this would use more sophisticated logic
        
        # Check if it's time to update the IQ chart
        last_update = self.last_analysis.get("country_iq_chart")
        if last_update:
            # Update every 24 hours
            if (datetime.now() - last_update).total_seconds() < 86400:
                return
        
        logger.info("Updating country IQ chart")
        
        # Save the updated IQ chart
        self._save_country_iq_chart()
        
        # Update last analysis time
        self.last_analysis["country_iq_chart"] = datetime.now()
    
    def _update_topic_models(self):
        """Update topic models based on recent data."""
        # This is a placeholder for actual topic model updating
        # In a real system, this would use actual topic modeling
        
        # Check if it's time to update the topic models
        last_update = self.last_analysis.get("topic_models")
        if last_update:
            # Update every 24 hours
            update_interval = self.config.get("analysis.topic_modeling.update_interval", 86400)
            if (datetime.now() - last_update).total_seconds() < update_interval:
                return
        
        logger.info("Updating topic models")
        
        # Placeholder for topic model updating
        # In a real system, this would update the topic models
        
        # Update last analysis time
        self.last_analysis["topic_models"] = datetime.now()
    
    def process_data(self, data: List[Dict[str, Any]]):
        """
        Process new data.
        
        Args:
            data: List of data to process
        """
        logger.info(f"Processing {len(data)} new data items")
        
        for item in data:
            source_type = item.get("type")
            
            if source_type == "social_media":
                self._process_social_media_data(item)
            elif source_type == "mainstream_media":
                self._process_mainstream_media_data(item)
            elif source_type == "book":
                self._process_book_data(item)
            elif source_type == "custom":
                self._process_custom_data(item)
            else:
                logger.warning(f"Unknown data type: {source_type}")
    
    def get_country_iq_chart(self) -> Dict[str, float]:
        """
        Get the current country IQ chart.
        
        Returns:
            Dictionary mapping country names to IQ scores
        """
        return self.country_iq_chart
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the analysis engine.
        
        Returns:
            Dictionary containing the current state
        """
        return {
            "running": self.running,
            "last_analysis": {k: v.isoformat() for k, v in self.last_analysis.items()},
            "sentiment_model": bool(self.sentiment_model),
            "entity_model": bool(self.entity_model),
            "topic_model": bool(self.topic_model),
            "country_iq_chart_size": len(self.country_iq_chart)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the analysis engine.
        
        Returns:
            Dictionary containing the current status
        """
        return {
            "running": self.running,
            "models": {
                "sentiment_analysis": bool(self.sentiment_model),
                "entity_recognition": bool(self.entity_model),
                "topic_modeling": bool(self.topic_model)
            },
            "last_analysis": {k: v.isoformat() for k, v in self.last_analysis.items()},
            "country_iq_chart": {
                "size": len(self.country_iq_chart),
                "min": min(self.country_iq_chart.values()) if self.country_iq_chart else None,
                "max": max(self.country_iq_chart.values()) if self.country_iq_chart else None,
                "avg": sum(self.country_iq_chart.values()) / len(self.country_iq_chart) if self.country_iq_chart else None
            }
        }


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test analysis engine
    from config import Configuration
    
    # Create default configuration
    config = Configuration()
    
    # Create analysis engine
    engine = AnalysisEngine(config)
    
    # Start analysis
    engine.start_analysis()
    
    # Wait for a while
    print("Analysis started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # Stop analysis
    engine.stop_analysis()
    print("Analysis stopped.")
