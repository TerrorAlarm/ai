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
   
(Content truncated due to size limit. Use line ranges to read in chunks)