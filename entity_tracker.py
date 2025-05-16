#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Entity Tracker Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module implements entity tracking for the Terror Alarm AI system.
"""

import os
import json
import time
import logging
import threading
import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger("TerrorAlarm.EntityTracker")

class EntityTracker:
    """
    Entity tracking for the Terror Alarm AI system.
    """
    
    def __init__(self, config):
        """
        Initialize the EntityTracker object.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.running = False
        self.tracking_thread = None
        self.last_update = {}
        
        # Entity lists
        self.supported_entities = []
        self.opposed_entities = []
        self.dangerous_organizations = []
        self.terrorist_individuals = []
        
        # Entity storage
        self.entities_dir = "data/entities"
        os.makedirs(self.entities_dir, exist_ok=True)
        
        # Load entity lists
        self._load_entity_lists()
        
        logger.info("EntityTracker initialized")
    
    def _load_entity_lists(self):
        """Load entity lists from files."""
        # Load supported entities
        supported_file = os.path.join(self.entities_dir, "supported_entities.json")
        if os.path.exists(supported_file):
            try:
                with open(supported_file, 'r') as f:
                    self.supported_entities = json.load(f)
                logger.info(f"Loaded {len(self.supported_entities)} supported entities")
            except Exception as e:
                logger.error(f"Error loading supported entities: {e}")
                self._initialize_supported_entities()
        else:
            logger.info("Supported entities file not found, initializing")
            self._initialize_supported_entities()
        
        # Load opposed entities
        opposed_file = os.path.join(self.entities_dir, "opposed_entities.json")
        if os.path.exists(opposed_file):
            try:
                with open(opposed_file, 'r') as f:
                    self.opposed_entities = json.load(f)
                logger.info(f"Loaded {len(self.opposed_entities)} opposed entities")
            except Exception as e:
                logger.error(f"Error loading opposed entities: {e}")
                self._initialize_opposed_entities()
        else:
            logger.info("Opposed entities file not found, initializing")
            self._initialize_opposed_entities()
        
        # Load dangerous organizations
        dangerous_orgs_file = os.path.join(self.entities_dir, "dangerous_organizations.json")
        if os.path.exists(dangerous_orgs_file):
            try:
                with open(dangerous_orgs_file, 'r') as f:
                    self.dangerous_organizations = json.load(f)
                logger.info(f"Loaded {len(self.dangerous_organizations)} dangerous organizations")
            except Exception as e:
                logger.error(f"Error loading dangerous organizations: {e}")
                self._initialize_dangerous_organizations()
        else:
            logger.info("Dangerous organizations file not found, initializing")
            self._initialize_dangerous_organizations()
        
        # Load terrorist individuals
        terrorist_individuals_file = os.path.join(self.entities_dir, "terrorist_individuals.json")
        if os.path.exists(terrorist_individuals_file):
            try:
                with open(terrorist_individuals_file, 'r') as f:
                    self.terrorist_individuals = json.load(f)
                logger.info(f"Loaded {len(self.terrorist_individuals)} terrorist individuals")
            except Exception as e:
                logger.error(f"Error loading terrorist individuals: {e}")
                self._initialize_terrorist_individuals()
        else:
            logger.info("Terrorist individuals file not found, initializing")
            self._initialize_terrorist_individuals()
    
    def _initialize_supported_entities(self):
        """Initialize the supported entities list with default values."""
        # Get supported entities from config
        self.supported_entities = self.config.get("entities.supported_groups", [])
        
        # Save the initial supported entities list
        self._save_supported_entities()
        
        logger.info(f"Initialized supported entities list with {len(self.supported_entities)} entities")
    
    def _initialize_opposed_entities(self):
        """Initialize the opposed entities list with default values."""
        # Get opposed entities from config
        self.opposed_entities = self.config.get("entities.opposed_entities", [])
        
        # Save the initial opposed entities list
        self._save_opposed_entities()
        
        logger.info(f"Initialized opposed entities list with {len(self.opposed_entities)} entities")
    
    def _initialize_dangerous_organizations(self):
        """Initialize the dangerous organizations list with default values."""
        # This is a placeholder for actual dangerous organizations initialization
        # In a real system, this would use actual data
        
        # Initialize with some known terrorist organizations
        self.dangerous_organizations = [
            {
                "name": "ISIS",
                "aliases": ["Islamic State", "ISIL", "Daesh"],
                "type": "Terrorist Organization",
                "threat_level": "High",
                "regions": ["Middle East", "North Africa", "Europe"],
                "description": "Extremist jihadist group known for violence and territorial claims",
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "Al-Qaeda",
                "aliases": ["The Base", "AQ"],
                "type": "Terrorist Organization",
                "threat_level": "High",
                "regions": ["Middle East", "North Africa", "South Asia", "Europe", "North America"],
                "description": "Global militant Islamist organization founded by Osama bin Laden",
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "Hamas",
                "aliases": ["Islamic Resistance Movement"],
                "type": "Terrorist Organization",
                "threat_level": "High",
                "regions": ["Middle East"],
                "description": "Palestinian Sunni-Islamic fundamentalist organization",
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "Hezbollah",
                "aliases": ["Party of God", "Islamic Jihad Organization"],
                "type": "Terrorist Organization",
                "threat_level": "High",
                "regions": ["Middle East", "South America"],
                "description": "Lebanese Shia Islamist political party and militant group",
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "Boko Haram",
                "aliases": ["Jamā'at Ahl as-Sunnah lid-Da'wah wa'l-Jihād"],
                "type": "Terrorist Organization",
                "threat_level": "High",
                "regions": ["West Africa"],
                "description": "Jihadist terrorist organization based in northeastern Nigeria",
                "last_updated": datetime.now().isoformat()
            }
        ]
        
        # Save the initial dangerous organizations list
        self._save_dangerous_organizations()
        
        logger.info(f"Initialized dangerous organizations list with {len(self.dangerous_organizations)} organizations")
    
    def _initialize_terrorist_individuals(self):
        """Initialize the terrorist individuals list with default values."""
        # This is a placeholder for actual terrorist individuals initialization
        # In a real system, this would use actual data
        
        # Initialize with some known terrorist individuals (using fictional names)
        self.terrorist_individuals = [
            {
                "name": "Abu Mohammed Al-Fiktivi",
                "aliases": ["The Ghost", "Mohammed Al-Shadid"],
                "organization": "ISIS",
                "threat_level": "High",
                "nationality": "Unknown",
                "status": "Active",
                "description": "High-ranking ISIS commander responsible for multiple attacks",
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "Yusuf Al-Imaginary",
                "aliases": ["The Engineer", "Abu Yusuf"],
                "organization": "Al-Qaeda",
                "threat_level": "High",
                "nationality": "Unknown",
                "status": "Active",
                "description": "Al-Qaeda explosives expert and operational planner",
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "Ibrahim Al-Fictional",
                "aliases": ["The Recruiter", "Sheikh Ibrahim"],
                "organization": "Boko Haram",
                "threat_level": "Medium",
                "nationality": "Unknown",
                "status": "Active",
                "description": "Boko Haram recruiter and propagandist",
                "last_updated": datetime.now().isoformat()
            }
        ]
        
        # Save the initial terrorist individuals list
        self._save_terrorist_individuals()
        
        logger.info(f"Initialized terrorist individuals list with {len(self.terrorist_individuals)} individuals")
    
    def _save_supported_entities(self):
        """Save the supported entities list to file."""
        supported_file = os.path.join(self.entities_dir, "supported_entities.json")
        try:
            with open(supported_file, 'w') as f:
                json.dump(self.supported_entities, f, indent=2)
            logger.info(f"Saved {len(self.supported_entities)} supported entities")
        except Exception as e:
            logger.error(f"Error saving supported entities: {e}")
    
    def _save_opposed_entities(self):
        """Save the opposed entities list to file."""
        opposed_file = os.path.join(self.entities_dir, "opposed_entities.json")
        try:
            with open(opposed_file, 'w') as f:
                json.dump(self.opposed_entities, f, indent=2)
            logger.info(f"Saved {len(self.opposed_entities)} opposed entities")
        except Exception as e:
            logger.error(f"Error saving opposed entities: {e}")
    
    def _save_dangerous_organizations(self):
        """Save the dangerous organizations list to file."""
        dangerous_orgs_file = os.path.join(self.entities_dir, "dangerous_organizations.json")
        try:
            with open(dangerous_orgs_file, 'w') as f:
                json.dump(self.dangerous_organizations, f, indent=2)
            logger.info(f"Saved {len(self.dangerous_organizations)} dangerous organizations")
        except Exception as e:
            logger.error(f"Error saving dangerous organizations: {e}")
    
    def _save_terrorist_individuals(self):
        """Save the terrorist individuals list to file."""
        terrorist_individuals_file = os.path.join(self.entities_dir, "terrorist_individuals.json")
        try:
            with open(terrorist_individuals_file, 'w') as f:
                json.dump(self.terrorist_individuals, f, indent=2)
            logger.info(f"Saved {len(self.terrorist_individuals)} terrorist individuals")
        except Exception as e:
            logger.error(f"Error saving terrorist individuals: {e}")
    
    def start_tracking(self):
        """Start the entity tracking process."""
        if self.running:
            logger.warning("Entity tracking is already running")
            return
            
        logger.info("Starting entity tracking")
        self.running = True
        self.tracking_thread = threading.Thread(target=self._tracking_loop)
        self.tracking_thread.daemon = True
        self.tracking_thread.start()
    
    def stop_tracking(self):
        """Stop the entity tracking process."""
        if not self.running:
            logger.warning("Entity tracking is not running")
            return
            
        logger.info("Stopping entity tracking")
        self.running = False
        if self.tracking_thread:
            self.tracking_thread.join(timeout=30)
    
    def _tracking_loop(self):
        """Main entity tracking loop."""
        logger.info("Entity tracking loop started")
        
        while self.running:
            try:
                # Update entity lists
                self._update_entity_lists()
                
                # Sleep for a while
                time.sleep(3600)  # 1 hour
                
            except Exception as e:
                logger.error(f"Error in entity tracking loop: {e}")
                time.sleep(300)  # Sleep for 5 minutes on error
    
    def _update_entity_lists(self):
        """Update entity lists based on recent data."""
        logger.info("Updating entity lists")
        
        # Get processed data
        processed_data = self._get_processed_data()
        
        # Update dangerous organizations
        self._update_dangerous_organizations(processed_data)
        
        # Update terrorist individuals
        self._update_terrorist_individuals(processed_data)
        
        # Save updated entity lists
        self._save_dangerous_organizations()
        self._save_terrorist_individuals()
        
        # Update last update time
        self.last_update["entity_lists"] = datetime.now()
        
        logger.info("Entity lists updated")
    
    def _get_processed_data(self) -> List[Dict[str, Any]]:
        """
        Get processed data for entity tracking.
        
        Returns:
            List of processed data items
        """
        # This is a placeholder for actual data retrieval
        # In a real system, this would retrieve processed data from storage
        
        processed_data = []
        
        # Get data directory
        data_dir = "data/analysis/processed"
        if not os.path.exists(data_dir):
            return processed_data
            
        # Get data from all source directories
        for source_type in ["social_media", "mainstream_media", "book", "custom"]:
            source_dir = os.path.join(data_dir, source_type)
            if not os.path.exists(source_dir):
                continue
                
            # Get data from all source subdirectories
            for source_name in os.listdir(source_dir):
                source_subdir = os.path.join(source_dir, source_name)
                if not os.path.isdir(source_subdir):
                    continue
                    
                # Get data from all files in the source subdirectory
                for filename in sorted(os.listdir(source_subdir), reverse=True):
                    if not filename.endswith(".json"):
                        continue
                        
                    # Only get recent files (last 7 days)
                    file_path = os.path.join(source_subdir, filename)
                    file_mtime = os.path.getmtime(file_path)
                    if time.time() - file_mtime > 604800:  # 7 days
                        continue
                        
                    # Load data from file
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
            
(Content truncated due to size limit. Use line ranges to read in chunks)