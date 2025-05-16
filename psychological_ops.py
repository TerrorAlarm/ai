#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Psychological Operations Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module implements psychological operations for the Terror Alarm AI system.
"""

import os
import json
import time
import random
import logging
import threading
import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger("TerrorAlarm.PsychologicalOps")

class PsychologicalOps:
    """
    Psychological operations for the Terror Alarm AI system.
    """
    
    def __init__(self, config):
        """
        Initialize the PsychologicalOps object.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.running = False
        self.operations_thread = None
        self.last_operation = {}
        
        # Operation settings
        self.news_generation = self.config.get("psychological_ops.news_generation.enabled", True)
        self.daily_news_limit = self.config.get("psychological_ops.news_generation.daily_limit", 10)
        
        self.narrative_shaping = self.config.get("psychological_ops.narrative_shaping.enabled", True)
        self.target_platforms = self.config.get("psychological_ops.narrative_shaping.target_platforms", [])
        
        # Operation storage
        self.operations_dir = "data/psyops"
        os.makedirs(self.operations_dir, exist_ok=True)
        
        # Create operation subdirectories
        os.makedirs(os.path.join(self.operations_dir, "news"), exist_ok=True)
        os.makedirs(os.path.join(self.operations_dir, "narratives"), exist_ok=True)
        os.makedirs(os.path.join(self.operations_dir, "campaigns"), exist_ok=True)
        
        # Load existing operations
        self._load_operations()
        
        logger.info("PsychologicalOps initialized")
    
    def _load_operations(self):
        """Load existing operations from files."""
        # Load active campaigns
        campaigns_file = os.path.join(self.operations_dir, "active_campaigns.json")
        if os.path.exists(campaigns_file):
            try:
                with open(campaigns_file, 'r') as f:
                    self.active_campaigns = json.load(f)
                logger.info(f"Loaded {len(self.active_campaigns)} active campaigns")
            except Exception as e:
                logger.error(f"Error loading active campaigns: {e}")
                self.active_campaigns = []
        else:
            logger.info("Active campaigns file not found, initializing empty list")
            self.active_campaigns = []
        
        # Load narrative templates
        templates_file = os.path.join(self.operations_dir, "narrative_templates.json")
        if os.path.exists(templates_file):
            try:
                with open(templates_file, 'r') as f:
                    self.narrative_templates = json.load(f)
                logger.info(f"Loaded {len(self.narrative_templates)} narrative templates")
            except Exception as e:
                logger.error(f"Error loading narrative templates: {e}")
                self._initialize_narrative_templates()
        else:
            logger.info("Narrative templates file not found, initializing")
            self._initialize_narrative_templates()
    
    def _initialize_narrative_templates(self):
        """Initialize narrative templates with default values."""
        # This is a placeholder for actual narrative template initialization
        # In a real system, this would use more sophisticated templates
        
        self.narrative_templates = [
            {
                "id": "counter_terrorism_success",
                "name": "Counter-Terrorism Success",
                "description": "Narrative highlighting successful counter-terrorism operations",
                "templates": [
                    "Security forces in {country} successfully prevented a {attack_type} planned by {organization}.",
                    "A major {attack_type} was thwarted in {country} thanks to intelligence provided by counter-terrorism agencies.",
                    "Counter-terrorism units in {country} arrested key members of {organization} before they could execute a planned {attack_type}."
                ],
                "variables": {
                    "country": ["various countries"],
                    "attack_type": ["bombing", "shooting", "hostage situation", "cyber attack", "infrastructure attack"],
                    "organization": ["terrorist organization", "extremist group", "terrorist cell"]
                },
                "sentiment": "positive",
                "target_audience": ["general public", "security agencies", "policy makers"]
            },
            {
                "id": "terrorist_threat_warning",
                "name": "Terrorist Threat Warning",
                "description": "Narrative warning about potential terrorist threats",
                "templates": [
                    "Intelligence sources report increased activity by {organization} in {region}, suggesting possible {attack_type} in the near future.",
                    "Security experts warn of potential {attack_type} by {organization} targeting {target} in {region}.",
                    "Authorities in {region} have raised the terror threat level due to intelligence suggesting {organization} is planning a {attack_type}."
                ],
                "variables": {
                    "organization": ["terrorist organization", "extremist group", "terrorist cell"],
                    "region": ["various regions"],
                    "attack_type": ["bombing", "shooting", "hostage situation", "cyber attack", "infrastructure attack"],
                    "target": ["civilian targets", "government buildings", "transportation hubs", "public gatherings"]
                },
                "sentiment": "cautionary",
                "target_audience": ["general public", "security agencies", "policy makers"]
            },
            {
                "id": "terrorist_organization_weakening",
                "name": "Terrorist Organization Weakening",
                "description": "Narrative highlighting the weakening of terrorist organizations",
                "templates": [
                    "{organization} is showing signs of internal conflict and weakening leadership following recent counter-terrorism operations in {region}.",
                    "Financial resources of {organization} have been significantly reduced due to international efforts to cut off funding sources.",
                    "Intelligence reports suggest {organization} is struggling to recruit new members due to successful counter-narrative campaigns."
                ],
                "variables": {
                    "organization": ["terrorist organization", "extremist group", "terrorist cell"],
                    "region": ["various regions"]
                },
                "sentiment": "positive",
                "target_audience": ["general public", "security agencies", "policy makers"]
            }
        ]
        
        # Save the initial narrative templates
        self._save_narrative_templates()
        
        logger.info(f"Initialized {len(self.narrative_templates)} narrative templates")
    
    def _save_narrative_templates(self):
        """Save narrative templates to file."""
        templates_file = os.path.join(self.operations_dir, "narrative_templates.json")
        try:
            with open(templates_file, 'w') as f:
                json.dump(self.narrative_templates, f, indent=2)
            logger.info(f"Saved {len(self.narrative_templates)} narrative templates")
        except Exception as e:
            logger.error(f"Error saving narrative templates: {e}")
    
    def _save_active_campaigns(self):
        """Save active campaigns to file."""
        campaigns_file = os.path.join(self.operations_dir, "active_campaigns.json")
        try:
            with open(campaigns_file, 'w') as f:
                json.dump(self.active_campaigns, f, indent=2)
            logger.info(f"Saved {len(self.active_campaigns)} active campaigns")
        except Exception as e:
            logger.error(f"Error saving active campaigns: {e}")
    
    def start_operations(self):
        """Start the psychological operations process."""
        if self.running:
            logger.warning("Psychological operations are already running")
            return
            
        logger.info("Starting psychological operations")
        self.running = True
        self.operations_thread = threading.Thread(target=self._operations_loop)
        self.operations_thread.daemon = True
        self.operations_thread.start()
    
    def stop_operations(self):
        """Stop the psychological operations process."""
        if not self.running:
            logger.warning("Psychological operations are not running")
            return
            
        logger.info("Stopping psychological operations")
        self.running = False
        if self.operations_thread:
            self.operations_thread.join(timeout=30)
    
    def _operations_loop(self):
        """Main psychological operations loop."""
        logger.info("Psychological operations loop started")
        
        while self.running:
            try:
                # Generate news
                if self.news_generation:
                    self._generate_news()
                
                # Shape narratives
                if self.narrative_shaping:
                    self._shape_narratives()
                
                # Update campaigns
                self._update_campaigns()
                
                # Sleep for a while
                time.sleep(3600)  # 1 hour
                
            except Exception as e:
                logger.error(f"Error in psychological operations loop: {e}")
                time.sleep(300)  # Sleep for 5 minutes on error
    
    def _generate_news(self):
        """Generate news articles."""
        # This is a placeholder for actual news generation
        # In a real system, this would use more sophisticated generation techniques
        
        # Check if it's time to generate news
        last_news = self.last_operation.get("news")
        if last_news:
            # Generate news once per day
            if (datetime.now() - last_news).days < 1:
                return
        
        logger.info("Generating news articles")
        
        # Get prediction data
        predictions = self._get_predictions()
        
        # Get entity data
        dangerous_orgs = self._get_dangerous_organizations()
        terrorist_individuals = self._get_terrorist_individuals()
        
        # Generate news articles
        news_articles = []
        
        # Generate news based on predictions
        for prediction in predictions[:self.daily_news_limit]:
            article = self._generate_news_from_prediction(prediction)
            if article:
                news_articles.append(article)
        
        # Generate news based on dangerous organizations
        for org in dangerous_orgs[:self.daily_news_limit // 2]:
            article = self._generate_news_from_organization(org)
            if article:
                news_articles.append(article)
        
        # Generate news based on terrorist individuals
        for individual in terrorist_individuals[:self.daily_news_limit // 2]:
            article = self._generate_news_from_individual(individual)
            if article:
                news_articles.append(article)
        
        # Save generated news articles
        if news_articles:
            self._save_news_articles(news_articles)
            
            # Update last operation time
            self.last_operation["news"] = datetime.now()
            
            logger.info(f"Generated {len(news_articles)} news articles")
    
    def _generate_news_from_prediction(self, prediction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate a news article from a prediction.
        
        Args:
            prediction: Prediction data
            
        Returns:
            News article or None if generation failed
        """
        try:
            # Generate headline
            headline_templates = [
                "Terror Threat Alert: {description} in {country}",
                "Security Agencies Warn of Potential {type} in {country}",
                "Intelligence Reports Suggest Possible {type} Planned in {country}",
                "Terror Alarm: {description} Expected in {country}",
                "Counter-Terrorism Units on High Alert for {type} in {country}"
            ]
            headline = random.choice(headline_templates).format(
                description=prediction["description"],
                country=prediction["country"],
                type=prediction["type"]
            )
            
            # Generate content
            content = f"TERROR ALARM NEWS - {datetime.now().strftime('%Y-%m-%d')}\n\n"
            content += f"{headline}\n\n"
            content += f"Intelligence sources report a potential {prediction['type']} in {prediction['country']} "
            content += f"that could occur around {prediction['date']}. "
            content += f"The threat level is assessed as {self._confidence_to_threat_level(prediction['confidence'])}.\n\n"
            content += f"Security agencies are actively monitoring the situation and implementing preventive measures. "
            content += f"Citizens are advised to remain vigilant and report any suspicious activities to local authorities.\n\n"
            content += f"This information is based on analysis by Terror Alarm AI, which has identified patterns "
            content += f"suggesting increased risk in the region. The prediction confidence level is {prediction['confidence']:.2f}.\n\n"
            content += f"Sources: {', '.join(prediction['sources'])}\n\n"
            content += f"© 2022-2025 Terror Alarm NGO. All rights reserved."
            
            # Create news article
            article = {
                "id": f"news_{int(time.time())}_{prediction['country'].lower().replace(' ', '_')}",
                "headline": headline,
                "content": content,
                "date": datetime.now().isoformat(),
                "country": prediction["country"],
                "type": prediction["type"],
                "confidence": prediction["confidence"],
                "sources": prediction["sources"]
            }
            
            return article
        except Exception as e:
            logger.error(f"Error generating news from prediction: {e}")
            return None
    
    def _generate_news_from_organization(self, organization: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate a news article from an organization.
        
        Args:
            organization: Organization data
            
        Returns:
            News article or None if generation failed
        """
        try:
            # Generate headline
            headline_templates = [
                "{name}: {threat_level} Threat Level Organization Identified",
                "Terror Alarm Identifies {name} as {threat_level} Threat",
                "Security Agencies Monitoring {name} Activities",
                "{name} Added to Terror Alarm's Dangerous Organizations List",
                "Intelligence Reports Highlight {name} as Emerging Threat"
            ]
            headline = random.choice(headline_templates).format(
                name=organization["name"],
                threat_level=organization["threat_level"]
            )
            
            # Generate content
      
(Content truncated due to size limit. Use line ranges to read in chunks)