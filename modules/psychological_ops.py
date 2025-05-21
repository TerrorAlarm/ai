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
            content = f"TERROR ALARM NEWS - {datetime.now().strftime('%Y-%m-%d')}\n\n"
            content += f"{headline}\n\n"
            content += f"Terror Alarm AI has identified {organization['name']} as a {organization['threat_level']} threat level organization. "
            content += f"The group, also known as {', '.join(organization['aliases'])}, "
            content += f"is primarily active in {', '.join(organization['regions'])}.\n\n"
            content += f"{organization['description']}\n\n"
            content += f"Security agencies are monitoring the organization's activities and implementing appropriate countermeasures. "
            content += f"Citizens in affected regions are advised to remain vigilant and report any suspicious activities to local authorities.\n\n"
            content += f"This information is based on analysis by Terror Alarm AI, which continuously monitors and assesses terrorist threats worldwide.\n\n"
            content += f"© 2022-2025 Terror Alarm NGO. All rights reserved."
            
            # Create news article
            article = {
                "id": f"news_{int(time.time())}_{organization['name'].lower().replace(' ', '_')}",
                "headline": headline,
                "content": content,
                "date": datetime.now().isoformat(),
                "organization": organization["name"],
                "threat_level": organization["threat_level"],
                "regions": organization["regions"]
            }
            
            return article
        except Exception as e:
            logger.error(f"Error generating news from organization: {e}")
            return None
    
    def _generate_news_from_individual(self, individual: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate a news article from an individual.
        
        Args:
            individual: Individual data
            
        Returns:
            News article or None if generation failed
        """
        try:
            # Generate headline
            headline_templates = [
                "{name}: {threat_level} Threat Individual Identified",
                "Terror Alarm Identifies {name} as {threat_level} Threat",
                "Security Agencies Tracking {name}, Member of {organization}",
                "{name} Added to Terror Alarm's Terrorist Individuals List",
                "Intelligence Reports Highlight {name} as Key {organization} Operative"
            ]
            headline = random.choice(headline_templates).format(
                name=individual["name"],
                threat_level=individual["threat_level"],
                organization=individual["organization"]
            )
            
            # Generate content
            content = f"TERROR ALARM NEWS - {datetime.now().strftime('%Y-%m-%d')}\n\n"
            content += f"{headline}\n\n"
            content += f"Terror Alarm AI has identified {individual['name']} as a {individual['threat_level']} threat level individual. "
            content += f"The individual, also known as {', '.join(individual['aliases'])}, "
            content += f"is affiliated with {individual['organization']} and is believed to be of {individual['nationality']} nationality.\n\n"
            content += f"Current status: {individual['status']}\n\n"
            content += f"{individual['description']}\n\n"
            content += f"Security agencies are tracking the individual's activities and implementing appropriate countermeasures. "
            content += f"Citizens are advised to report any sightings or information to local authorities immediately.\n\n"
            content += f"This information is based on analysis by Terror Alarm AI, which continuously monitors and assesses terrorist threats worldwide.\n\n"
            content += f"© 2022-2025 Terror Alarm NGO. All rights reserved."
            
            # Create news article
            article = {
                "id": f"news_{int(time.time())}_{individual['name'].lower().replace(' ', '_')}",
                "headline": headline,
                "content": content,
                "date": datetime.now().isoformat(),
                "individual": individual["name"],
                "organization": individual["organization"],
                "threat_level": individual["threat_level"],
                "status": individual["status"]
            }
            
            return article
        except Exception as e:
            logger.error(f"Error generating news from individual: {e}")
            return None
    
    def _confidence_to_threat_level(self, confidence: float) -> str:
        """
        Convert a confidence score to a threat level.
        
        Args:
            confidence: Confidence score
            
        Returns:
            Threat level
        """
        if confidence >= 0.9:
            return "Critical"
        elif confidence >= 0.7:
            return "High"
        elif confidence >= 0.5:
            return "Medium"
        elif confidence >= 0.3:
            return "Low"
        else:
            return "Minimal"
    
    def _save_news_articles(self, articles: List[Dict[str, Any]]):
        """
        Save news articles to files.
        
        Args:
            articles: List of news articles
        """
        for article in articles:
            # Save article to file
            article_file = os.path.join(self.operations_dir, "news", f"{article['id']}.json")
            try:
                with open(article_file, 'w') as f:
                    json.dump(article, f, indent=2)
                logger.debug(f"Saved news article to {article_file}")
            except Exception as e:
                logger.error(f"Error saving news article: {e}")
            
            # Save article content to text file
            content_file = os.path.join(self.operations_dir, "news", f"{article['id']}.txt")
            try:
                with open(content_file, 'w') as f:
                    f.write(article["content"])
                logger.debug(f"Saved news article content to {content_file}")
            except Exception as e:
                logger.error(f"Error saving news article content: {e}")
    
    def _shape_narratives(self):
        """Shape narratives based on templates."""
        # This is a placeholder for actual narrative shaping
        # In a real system, this would use more sophisticated techniques
        
        # Check if it's time to shape narratives
        last_narrative = self.last_operation.get("narrative")
        if last_narrative:
            # Shape narratives once per day
            if (datetime.now() - last_narrative).days < 1:
                return
        
        logger.info("Shaping narratives")
        
        # Get prediction data
        predictions = self._get_predictions()
        
        # Get entity data
        dangerous_orgs = self._get_dangerous_organizations()
        
        # Generate narratives
        narratives = []
        
        # Select random narrative templates
        selected_templates = random.sample(
            self.narrative_templates,
            min(len(self.narrative_templates), 3)
        )
        
        # Generate narratives from templates
        for template in selected_templates:
            narrative = self._generate_narrative_from_template(template, predictions, dangerous_orgs)
            if narrative:
                narratives.append(narrative)
        
        # Save generated narratives
        if narratives:
            self._save_narratives(narratives)
            
            # Update last operation time
            self.last_operation["narrative"] = datetime.now()
            
            logger.info(f"Generated {len(narratives)} narratives")
    
    def _generate_narrative_from_template(
        self,
        template: Dict[str, Any],
        predictions: List[Dict[str, Any]],
        organizations: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a narrative from a template.
        
        Args:
            template: Narrative template
            predictions: List of predictions
            organizations: List of dangerous organizations
            
        Returns:
            Narrative or None if generation failed
        """
        try:
            # Select a random template text
            template_text = random.choice(template["templates"])
            
            # Prepare variables
            variables = {}
            
            # Fill in variables from predictions and organizations
            for var_name, var_values in template["variables"].items():
                if var_name == "country" and predictions:
                    # Use a country from predictions
                    variables[var_name] = random.choice(predictions)["country"]
                elif var_name == "region" and predictions:
                    # Use a country from predictions as region
                    variables[var_name] = random.choice(predictions)["country"]
                elif var_name == "organization" and organizations:
                    # Use an organization name
                    variables[var_name] = random.choice(organizations)["name"]
                elif var_name == "attack_type" and predictions:
                    # Use a threat type from predictions
                    variables[var_name] = random.choice(predictions)["type"]
                elif var_name == "target":
                    # Use a random target
                    variables[var_name] = random.choice(var_values)
                else:
                    # Use a random value from the template
                    variables[var_name] = random.choice(var_values)
            
            # Format the template text with variables
            narrative_text = template_text.format(**variables)
            
            # Create narrative
            narrative = {
                "id": f"narrative_{int(time.time())}_{template['id']}",
                "template_id": template["id"],
                "template_name": template["name"],
                "text": narrative_text,
                "variables": variables,
                "sentiment": template["sentiment"],
                "target_audience": template["target_audience"],
                "target_platforms": self.target_platforms,
                "date": datetime.now().isoformat()
            }
            
            return narrative
        except Exception as e:
            logger.error(f"Error generating narrative from template: {e}")
            return None
    
    def _save_narratives(self, narratives: List[Dict[str, Any]]):
        """
        Save narratives to files.
        
        Args:
            narratives: List of narratives
        """
        for narrative in narratives:
            # Save narrative to file
            narrative_file = os.path.join(self.operations_dir, "narratives", f"{narrative['id']}.json")
            try:
                with open(narrative_file, 'w') as f:
                    json.dump(narrative, f, indent=2)
                logger.debug(f"Saved narrative to {narrative_file}")
            except Exception as e:
                logger.error(f"Error saving narrative: {e}")
            
            # Save narrative text to text file
            text_file = os.path.join(self.operations_dir, "narratives", f"{narrative['id']}.txt")
            try:
                with open(text_file, 'w') as f:
                    f.write(narrative["text"])
                logger.debug(f"Saved narrative text to {text_file}")
            except Exception as e:
                logger.error(f"Error saving narrative text: {e}")
    
    def _update_campaigns(self):
        """Update active campaigns."""
        # This is a placeholder for actual campaign updating
        # In a real system, this would use more sophisticated techniques
        
        logger.info("Updating campaigns")
        
        # Check for completed campaigns
        completed_campaigns = []
        for campaign in self.active_campaigns:
            end_date = datetime.fromisoformat(campaign["end_date"])
            if datetime.now() >= end_date:
                completed_campaigns.append(campaign)
        
        # Remove completed campaigns
        for campaign in completed_campaigns:
            self.active_campaigns.remove(campaign)
            logger.info(f"Campaign completed: {campaign['name']}")
        
        # Create new campaigns if needed
        if len(self.active_campaigns) < 3:  # Maintain at least 3 active campaigns
            # Get prediction data
            predictions = self._get_predictions()
            
            # Get entity data
            dangerous_orgs = self._get_dangerous_organizations()
            
            # Create new campaigns
            new_campaigns = []
            
            # Create short-term campaign (3 years)
            short_campaign = self._create_campaign(
                "short",
                predictions,
                dangerous_orgs,
                timedelta(days=365 * 3)
            )
            if short_campaign:
                new_campaigns.append(short_campaign)
            
            # Create long-term campaign (10 years)
            long_campaign = self._create_campaign(
                "long",
                predictions,
                dangerous_orgs,
                timedelta(days=365 * 10)
            )
            if long_campaign:
                new_campaigns.append(long_campaign)
            
            # Add new campaigns to active campaigns
            self.active_campaigns.extend(new_campaigns)
            
            # Save active campaigns
            self._save_active_campaigns()
            
            logger.info(f"Created {len(new_campaigns)} new campaigns")
    
    def _create_campaign(
        self,
        campaign_type: str,
        predictions: List[Dict[str, Any]],
        organizations: List[Dict[str, Any]],
        duration: timedelta
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new campaign.
        
        Args:
            campaign_type: Type of campaign ("short" or "long")
            predictions: List of predictions
            organizations: List of dangerous organizations
            duration: Campaign duration
            
        Returns:
            Campaign or None if creation failed
        """
        try:
            # Determine campaign focus
            if campaign_type == "short":
                # Focus on a specific threat
                if predictions:
                    focus_prediction = max(predictions, key=lambda p: p["confidence"])
                    focus = f"Counter-{focus_prediction['type']} in {focus_prediction['country']}"
                    description = f"Short-term campaign focused on countering {focus_prediction['type']} threats in {focus_prediction['country']}"
                else:
                    focus = "Counter-Terrorism Awareness"
                    description = "Short-term campaign focused on raising counter-terrorism awareness"
            else:
                # Focus on a specific organization
                if organizations:
                    focus_org = max(organizations, key=lambda o: o["threat_level"] == "High")
                    focus = f"Counter-{focus_org['name']}"
                    description = f"Long-term campaign focused on countering {focus_org['name']} and similar organizations"
                else:
                    focus = "Global Counter-Terrorism"
                    description = "Long-term campaign focused on global counter-terrorism efforts"
            
            # Create campaign
            campaign = {
                "id": f"campaign_{int(time.time())}_{campaign_type}",
                "name": f"{focus} Campaign",
                "type": campaign_type,
                "focus": focus,
                "description": description,
                "start_date": datetime.now().isoformat(),
                "end_date": (datetime.now() + duration).isoformat(),
                "target_audience": ["general public", "security agencies", "policy makers"],
                "target_platforms": self.target_platforms,
                "narratives": [],
                "status": "active",
                "progress": 0.0
            }
            
            # Save campaign to file
            campaign_file = os.path.join(self.operations_dir, "campaigns", f"{campaign['id']}.json")
            try:
                with open(campaign_file, 'w') as f:
                    json.dump(campaign, f, indent=2)
                logger.debug(f"Saved campaign to {campaign_file}")
            except Exception as e:
                logger.error(f"Error saving campaign: {e}")
            
            return campaign
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            return None
    
    def _get_predictions(self) -> List[Dict[str, Any]]:
        """
        Get predictions for psychological operations.
        
        Returns:
            List of predictions
        """
        # This is a placeholder for actual prediction retrieval
        # In a real system, this would retrieve predictions from the prediction model
        
        predictions = []
        
        try:
            # Try to load short-term predictions
            predictions_file = os.path.join("data/predictions", "short_predictions.json")
            if os.path.exists(predictions_file):
                with open(predictions_file, 'r') as f:
                    predictions = json.load(f)
            
            # If no short-term predictions, try medium-term
            if not predictions:
                predictions_file = os.path.join("data/predictions", "medium_predictions.json")
                if os.path.exists(predictions_file):
                    with open(predictions_file, 'r') as f:
                        predictions = json.load(f)
        except Exception as e:
            logger.error(f"Error loading predictions: {e}")
        
        return predictions
    
    def _get_dangerous_organizations(self) -> List[Dict[str, Any]]:
        """
        Get dangerous organizations for psychological operations.
        
        Returns:
            List of dangerous organizations
        """
        # This is a placeholder for actual organization retrieval
        # In a real system, this would retrieve organizations from the entity tracker
        
        organizations = []
        
        try:
            orgs_file = os.path.join("data/entities", "dangerous_organizations.json")
            if os.path.exists(orgs_file):
                with open(orgs_file, 'r') as f:
                    organizations = json.load(f)
        except Exception as e:
            logger.error(f"Error loading dangerous organizations: {e}")
        
        return organizations
    
    def _get_terrorist_individuals(self) -> List[Dict[str, Any]]:
        """
        Get terrorist individuals for psychological operations.
        
        Returns:
            List of terrorist individuals
        """
        # This is a placeholder for actual individual retrieval
        # In a real system, this would retrieve individuals from the entity tracker
        
        individuals = []
        
        try:
            individuals_file = os.path.join("data/entities", "terrorist_individuals.json")
            if os.path.exists(individuals_file):
                with open(individuals_file, 'r') as f:
                    individuals = json.load(f)
        except Exception as e:
            logger.error(f"Error loading terrorist individuals: {e}")
        
        return individuals
    
    def update_operations(self):
        """Update all psychological operations."""
        self._generate_news()
        self._shape_narratives()
        self._update_campaigns()
    
    def get_news_articles(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent news articles.
        
        Args:
            limit: Maximum number of articles to return
            
        Returns:
            List of news articles
        """
        articles = []
        
        try:
            news_dir = os.path.join(self.operations_dir, "news")
            if os.path.exists(news_dir):
                # Get all JSON files
                json_files = [f for f in os.listdir(news_dir) if f.endswith(".json")]
                
                # Sort by modification time (newest first)
                json_files.sort(key=lambda f: os.path.getmtime(os.path.join(news_dir, f)), reverse=True)
                
                # Load articles
                for filename in json_files[:limit]:
                    file_path = os.path.join(news_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            article = json.load(f)
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error loading news article from {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error getting news articles: {e}")
        
        return articles
    
    def get_narratives(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent narratives.
        
        Args:
            limit: Maximum number of narratives to return
            
        Returns:
            List of narratives
        """
        narratives = []
        
        try:
            narratives_dir = os.path.join(self.operations_dir, "narratives")
            if os.path.exists(narratives_dir):
                # Get all JSON files
                json_files = [f for f in os.listdir(narratives_dir) if f.endswith(".json")]
                
                # Sort by modification time (newest first)
                json_files.sort(key=lambda f: os.path.getmtime(os.path.join(narratives_dir, f)), reverse=True)
                
                # Load narratives
                for filename in json_files[:limit]:
                    file_path = os.path.join(narratives_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            narrative = json.load(f)
                            narratives.append(narrative)
                    except Exception as e:
                        logger.error(f"Error loading narrative from {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error getting narratives: {e}")
        
        return narratives
    
    def get_active_campaigns(self) -> List[Dict[str, Any]]:
        """
        Get active campaigns.
        
        Returns:
            List of active campaigns
        """
        return self.active_campaigns
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the psychological operations.
        
        Returns:
            Dictionary containing the current state
        """
        return {
            "running": self.running,
            "last_operation": {k: v.isoformat() for k, v in self.last_operation.items()},
            "news_generation": self.news_generation,
            "narrative_shaping": self.narrative_shaping,
            "active_campaigns": len(self.active_campaigns)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the psychological operations.
        
        Returns:
            Dictionary containing the current status
        """
        return {
            "running": self.running,
            "operations": {
                "news_generation": self.news_generation,
                "narrative_shaping": self.narrative_shaping,
                "target_platforms": self.target_platforms
            },
            "last_operation": {k: v.isoformat() for k, v in self.last_operation.items()} if self.last_operation else None,
            "active_campaigns": len(self.active_campaigns)
        }


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test psychological operations
    from config import Configuration
    
    # Create default configuration
    config = Configuration()
    
    # Create psychological operations
    psyops = PsychologicalOps(config)
    
    # Start operations
    psyops.start_operations()
    
    # Wait for a while
    print("Psychological operations started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # Stop operations
    psyops.stop_operations()
    print("Psychological operations stopped.")
