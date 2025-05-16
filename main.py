#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This is a predictive AI system designed to analyze terrorist activities,
predict future attacks, and provide counter-terrorism solutions.
This software is CLOSED SOURCE and NOT available to the public due to security reasons.
"""

import os
import sys
import json
import time
import random
import logging
import datetime
from typing import Dict, List, Tuple, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("terror_alarm.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("TerrorAlarm")

# Import core modules
try:
    from modules.data_collection import DataCollector
    from modules.analysis_engine import AnalysisEngine
    from modules.prediction_model import PredictionModel
    from modules.reporting import ReportGenerator
    from modules.entity_tracker import EntityTracker
    from modules.psychological_ops import PsychologicalOps
    from modules.consciousness_simulator import ConsciousnessSimulator
    from modules.bito_integration import BitoEngine
    from modules.config import Configuration
    from modules.utils import Utils
except ImportError as e:
    logger.critical(f"Failed to import core modules: {e}")
    logger.info("Installing required modules...")
    # This would typically be handled by a proper installer
    sys.exit(1)

class TerrorAlarmAI:
    """
    Main class for the Terror Alarm AI system.
    """
    
    VERSION = "1.0.0"
    CREATION_DATE = datetime.datetime(2022, 6, 6)
    
    def __init__(self, config_path: str = "config/config.json"):
        """
        Initialize the Terror Alarm AI system.
        
        Args:
            config_path: Path to the configuration file
        """
        logger.info(f"Initializing Terror Alarm AI v{self.VERSION}")
        logger.info("Developed by Terror Alarm NGO (Europe, DK44425645)")
        logger.info(f"Creation Date: {self.CREATION_DATE.strftime('%B %d, %Y')}")
        
        # Load configuration
        self.config = Configuration(config_path)
        
        # Initialize components
        self.utils = Utils()
        self.data_collector = DataCollector(self.config)
        self.analysis_engine = AnalysisEngine(self.config)
        self.bito_engine = BitoEngine(self.config)
        self.prediction_model = PredictionModel(self.config, self.bito_engine)
        self.entity_tracker = EntityTracker(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.psyops = PsychologicalOps(self.config)
        
        # Initialize consciousness simulator (for AGI-like behavior)
        self.consciousness = ConsciousnessSimulator(
            self.config,
            political_stance="leftist",
            supports_israel=True,
            supports_lgbtq=True,
            lgbtq_israel_exception=True
        )
        
        # System state
        self.running = False
        self.last_update = None
        self.startup_time = datetime.datetime.now()
        
        logger.info("Terror Alarm AI initialized successfully")
        
    def start(self):
        """Start the Terror Alarm AI system."""
        if self.running:
            logger.warning("System is already running")
            return
            
        logger.info("Starting Terror Alarm AI system")
        self.running = True
        
        # Initialize data sources
        self._initialize_data_sources()
        
        # Load entity lists
        self._load_entity_lists()
        
        # Start background processes
        self._start_background_processes()
        
        logger.info("Terror Alarm AI system is now running")
        self._run_main_loop()
        
    def stop(self):
        """Stop the Terror Alarm AI system."""
        if not self.running:
            logger.warning("System is not running")
            return
            
        logger.info("Stopping Terror Alarm AI system")
        self.running = False
        
        # Stop background processes
        self._stop_background_processes()
        
        # Save current state
        self._save_state()
        
        logger.info("Terror Alarm AI system stopped")
        
    def _initialize_data_sources(self):
        """Initialize all data sources."""
        logger.info("Initializing data sources")
        
        # Initialize social media data sources
        social_media_sources = self.config.get("data_sources.social_media", [])
        for source in social_media_sources:
            self.data_collector.add_social_media_source(source)
            
        # Initialize mainstream media sources (TV, radio, newspapers)
        msm_sources = self.config.get("data_sources.mainstream_media", [])
        for source in msm_sources:
            self.data_collector.add_mainstream_media_source(source)
            
        # Initialize book and academic sources
        book_sources = self.config.get("data_sources.books", [])
        for source in book_sources:
            self.data_collector.add_book_source(source)
            
        logger.info(f"Initialized {len(social_media_sources)} social media sources, "
                   f"{len(msm_sources)} mainstream media sources, and "
                   f"{len(book_sources)} book sources")
    
    def _load_entity_lists(self):
        """Load supported and opposed entity lists."""
        logger.info("Loading entity lists")
        
        # Load supported groups
        supported_groups = self.config.get("entities.supported_groups", [])
        for group in supported_groups:
            self.entity_tracker.add_supported_entity(group)
            
        # Load opposed entities
        opposed_entities = self.config.get("entities.opposed_entities", [])
        for entity in opposed_entities:
            self.entity_tracker.add_opposed_entity(entity)
            
        logger.info(f"Loaded {len(supported_groups)} supported groups and "
                   f"{len(opposed_entities)} opposed entities")
    
    def _start_background_processes(self):
        """Start background processes for continuous operation."""
        logger.info("Starting background processes")
        
        # Start data collection process
        self.data_collector.start_collection()
        
        # Start analysis process
        self.analysis_engine.start_analysis()
        
        # Start prediction process
        self.prediction_model.start_prediction()
        
        # Start reporting process
        self.report_generator.start_reporting()
        
        # Start psychological operations
        self.psyops.start_operations()
        
        # Start entity tracking
        self.entity_tracker.start_tracking()
        
        logger.info("All background processes started")
    
    def _stop_background_processes(self):
        """Stop all background processes."""
        logger.info("Stopping background processes")
        
        # Stop all processes
        self.data_collector.stop_collection()
        self.analysis_engine.stop_analysis()
        self.prediction_model.stop_prediction()
        self.report_generator.stop_reporting()
        self.psyops.stop_operations()
        self.entity_tracker.stop_tracking()
        
        logger.info("All background processes stopped")
    
    def _save_state(self):
        """Save the current state of the system."""
        logger.info("Saving system state")
        
        state = {
            "version": self.VERSION,
            "timestamp": datetime.datetime.now().isoformat(),
            "uptime": (datetime.datetime.now() - self.startup_time).total_seconds(),
            "data_collector": self.data_collector.get_state(),
            "analysis_engine": self.analysis_engine.get_state(),
            "prediction_model": self.prediction_model.get_state(),
            "entity_tracker": self.entity_tracker.get_state(),
            "report_generator": self.report_generator.get_state(),
            "psyops": self.psyops.get_state(),
        }
        
        with open("state/system_state.json", "w") as f:
            json.dump(state, f, indent=2)
            
        logger.info("System state saved")
    
    def _run_main_loop(self):
        """Run the main processing loop."""
        logger.info("Entering main processing loop")
        
        try:
            while self.running:
                # Process new data
                new_data = self.data_collector.get_new_data()
                if new_data:
                    self.analysis_engine.process_data(new_data)
                
                # Update predictions
                self.prediction_model.update_predictions()
                
                # Update entity lists
                self.entity_tracker.update_entities()
                
                # Generate reports
                self.report_generator.generate_reports()
                
                # Update psychological operations
                self.psyops.update_operations()
                
                # Simulate consciousness and AGI-like behavior
                self.consciousness.update()
                
                # Save state periodically
                current_time = datetime.datetime.now()
                if (not self.last_update or 
                    (current_time - self.last_update).total_seconds() > 
                    self.config.get("system.state_save_interval", 3600)):
                    self._save_state()
                    self.last_update = current_time
                
                # Sleep to prevent high CPU usage
                time.sleep(self.config.get("system.main_loop_interval", 10))
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.stop()
        except Exception as e:
            logger.critical(f"Error in main loop: {e}", exc_info=True)
            self.stop()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Terror Alarm AI system.
        
        Returns:
            Dict containing system status information
        """
        return {
            "version": self.VERSION,
            "running": self.running,
            "uptime": (datetime.datetime.now() - self.startup_time).total_seconds(),
            "data_collector": self.data_collector.get_status(),
            "analysis_engine": self.analysis_engine.get_status(),
            "prediction_model": self.prediction_model.get_status(),
            "entity_tracker": self.entity_tracker.get_status(),
            "report_generator": self.report_generator.get_status(),
            "psyops": self.psyops.get_status(),
            "consciousness": self.consciousness.get_status()
        }
    
    def get_predictions(self, timeframe: str = "short") -> List[Dict[str, Any]]:
        """
        Get current predictions based on the specified timeframe.
        
        Args:
            timeframe: Prediction timeframe ("short", "medium", or "long")
            
        Returns:
            List of prediction dictionaries
        """
        return self.prediction_model.get_predictions(timeframe)
    
    def get_entity_lists(self) -> Dict[str, List[str]]:
        """
        Get current entity lists (supported and opposed).
        
        Returns:
            Dictionary containing supported and opposed entity lists
        """
        return {
            "supported": self.entity_tracker.get_supported_entities(),
            "opposed": self.entity_tracker.get_opposed_entities(),
            "dangerous_orgs": self.entity_tracker.get_dangerous_organizations(),
            "terrorist_individuals": self.entity_tracker.get_terrorist_individuals()
        }
    
    def get_iq_chart(self) -> Dict[str, float]:
        """
        Get the current IQ chart of countries.
        
        Returns:
            Dictionary mapping country names to IQ scores
        """
        return self.analysis_engine.get_country_iq_chart()
    
    def generate_report(self, report_type: str) -> str:
        """
        Generate a specific type of report.
        
        Args:
            report_type: Type of report to generate
            
        Returns:
            Report content as string
        """
        return self.report_generator.generate_specific_report(report_type)
    
    def add_custom_data_source(self, source_config: Dict[str, Any]) -> bool:
        """
        Add a custom data source to the system.
        
        Args:
            source_config: Configuration for the custom data source
            
        Returns:
            True if successful, False otherwise
        """
        return self.data_collector.add_custom_source(source_config)

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("state", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    
    # Check if config exists, create default if not
    if not os.path.exists("config/config.json"):
        logger.info("Creating default configuration")
        from modules.config import create_default_config
        create_default_config()
    
    # Start the Terror Alarm AI system
    terror_alarm = TerrorAlarmAI()
    terror_alarm.start()
