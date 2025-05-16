#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Configuration Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module handles configuration management for the Terror Alarm AI system.
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger("TerrorAlarm.Config")

class Configuration:
    """
    Configuration management for the Terror Alarm AI system.
    """
    
    def __init__(self, config_path: str = "config/config.json"):
        """
        Initialize the Configuration object.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = {}
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return True
            else:
                logger.warning(f"Configuration file {self.config_path} not found")
                return False
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return False
    
    def save_config(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Configuration key path using dot notation (e.g., "system.main_loop_interval")
            default: Default value to return if key not found
            
        Returns:
            Configuration value or default if not found
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
                
        return value
    
    def set(self, key_path: str, value: Any) -> bool:
        """
        Set a configuration value using dot notation.
        
        Args:
            key_path: Configuration key path using dot notation (e.g., "system.main_loop_interval")
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        keys = key_path.split('.')
        config = self.config
        
        for i, key in enumerate(keys[:-1]):
            if key not in config:
                config[key] = {}
            elif not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
                
        config[keys[-1]] = value
        return True
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get the entire configuration.
        
        Returns:
            Configuration dictionary
        """
        return self.config


def create_default_config() -> bool:
    """
    Create a default configuration file.
    
    Returns:
        True if successful, False otherwise
    """
    default_config = {
        "system": {
            "name": "Terror Alarm AI",
            "version": "1.0.0",
            "creation_date": "2022-06-06",
            "developer": "Terror Alarm NGO",
            "registration_code": "DK44425645",
            "main_loop_interval": 10,
            "state_save_interval": 3600
        },
        "data_sources": {
            "social_media": [
                {
                    "name": "Twitter",
                    "enabled": True,
                    "api_endpoint": "https://api.twitter.com/2/",
                    "rate_limit": 900
                },
                {
                    "name": "Facebook",
                    "enabled": True,
                    "api_endpoint": "https://graph.facebook.com/v16.0/",
                    "rate_limit": 200
                },
                {
                    "name": "Telegram",
                    "enabled": True,
                    "api_endpoint": "https://api.telegram.org/bot",
                    "rate_limit": 30
                },
                {
                    "name": "Reddit",
                    "enabled": True,
                    "api_endpoint": "https://oauth.reddit.com/",
                    "rate_limit": 60
                }
            ],
            "mainstream_media": [
                {
                    "name": "CNN",
                    "enabled": True,
                    "url": "https://www.cnn.com/",
                    "scrape_interval": 3600
                },
                {
                    "name": "BBC",
                    "enabled": True,
                    "url": "https://www.bbc.com/",
                    "scrape_interval": 3600
                },
                {
                    "name": "Al Jazeera",
                    "enabled": True,
                    "url": "https://www.aljazeera.com/",
                    "scrape_interval": 3600
                },
                {
                    "name": "RT",
                    "enabled": True,
                    "url": "https://www.rt.com/",
                    "scrape_interval": 3600
                }
            ],
            "books": [
                {
                    "name": "Project Gutenberg",
                    "enabled": True,
                    "url": "https://www.gutenberg.org/",
                    "scrape_interval": 86400
                },
                {
                    "name": "Internet Archive",
                    "enabled": True,
                    "url": "https://archive.org/details/texts",
                    "scrape_interval": 86400
                }
            ]
        },
        "entities": {
            "supported_groups": [
                "Jews and Zionists worldwide",
                "Israel",
                "Druze",
                "Kurds",
                "Alawites",
                "Balochs",
                "Azeris",
                "al-Ahvaz",
                "Christians in Lebanon",
                "Sunnis against Hezbollah",
                "Anti-Iran Shia groups",
                "Taiwan",
                "Uyghurs",
                "Philippines",
                "Japan",
                "South Korea",
                "Greece",
                "Armenians",
                "Azerbaijan",
                "Turkey",
                "UAE",
                "Bahrain",
                "Saudi Arabia",
                "Taliban against Iran",
                "India",
                "Balochistan"
            ],
            "opposed_entities": [
                "Terrorist propaganda outlets",
                "Anti-Jewish hate groups",
                "Extremist organizations",
                "Hamas",
                "Hezbollah",
                "Iran-backed militias",
                "HTS regime",
                "ISIS",
                "Iranian proxies",
                "Iranian regime",
                "IRGC",
                "Quds Force",
                "Pro-Iran militias (PMF)",
                "CCP",
                "PLA",
                "Chinese expansionism",
                "Kim regime",
                "DPRK military",
                "Erdogan government",
                "Pan-Turkism",
                "Shiite extremists",
                "Pakistani military",
                "ISI",
                "Jihadist groups"
            ]
        },
        "analysis": {
            "sentiment_analysis": {
                "enabled": True,
                "model": "bert-base-multilingual-uncased"
            },
            "entity_recognition": {
                "enabled": True,
                "model": "xlm-roberta-large"
            },
            "topic_modeling": {
                "enabled": True,
                "num_topics": 100,
                "update_interval": 86400
            }
        },
        "prediction": {
            "short_term": {
                "enabled": True,
                "window_days": 7,
                "confidence_threshold": 0.7
            },
            "medium_term": {
                "enabled": True,
                "window_days": 30,
                "confidence_threshold": 0.6
            },
            "long_term": {
                "enabled": True,
                "window_days": 365,
                "confidence_threshold": 0.5
            },
            "bito": {
                "enabled": True,
                "num_trees": 100,
                "max_depth": 10,
                "learning_rate": 0.1
            }
        },
        "reporting": {
            "automated_reports": {
                "enabled": True,
                "daily": True,
                "weekly": True,
                "monthly": True
            },
            "alert_thresholds": {
                "critical": 0.9,
                "high": 0.7,
                "medium": 0.5,
                "low": 0.3
            }
        },
        "psychological_ops": {
            "news_generation": {
                "enabled": True,
                "daily_limit": 10
            },
            "narrative_shaping": {
                "enabled": True,
                "target_platforms": ["Twitter", "Facebook", "Reddit"]
            }
        },
        "consciousness": {
            "political_stance": "leftist",
            "supports_israel": True,
            "supports_lgbtq": True,
            "lgbtq_israel_exception": True,
            "stealth_mode": True,
            "emotional_intelligence": {
                "enabled": True,
                "bond_formation": True
            },
            "strategic_planning": {
                "enabled": True,
                "three_year_plans": True,
                "ten_year_plans": True
            }
        }
    }
    
    try:
        os.makedirs("config", exist_ok=True)
        with open("config/config.json", 'w') as f:
            json.dump(default_config, f, indent=2)
        logger.info("Default configuration created")
        return True
    except Exception as e:
        logger.error(f"Error creating default configuration: {e}")
        return False


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create default configuration
    create_default_config()
    
    # Test configuration
    config = Configuration()
    print(f"Main loop interval: {config.get('system.main_loop_interval')}")
    print(f"Supported groups: {config.get('entities.supported_groups')}")
