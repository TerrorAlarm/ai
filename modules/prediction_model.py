#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Prediction Model Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module implements the prediction model for the Terror Alarm AI system.
"""

import os
import json
import time
import logging
import threading
import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger("TerrorAlarm.PredictionModel")

class PredictionModel:
    """
    Prediction model for the Terror Alarm AI system.
    """
    
    def __init__(self, config, bito_engine):
        """
        Initialize the PredictionModel object.
        
        Args:
            config: Configuration object
            bito_engine: BitoEngine object
        """
        self.config = config
        self.bito_engine = bito_engine
        self.running = False
        self.prediction_thread = None
        self.last_prediction = {}
        
        # Prediction timeframes
        self.timeframes = {
            "short": {
                "days": self.config.get("prediction.short_term.window_days", 7),
                "confidence_threshold": self.config.get("prediction.short_term.confidence_threshold", 0.7),
                "predictions": []
            },
            "medium": {
                "days": self.config.get("prediction.medium_term.window_days", 30),
                "confidence_threshold": self.config.get("prediction.medium_term.confidence_threshold", 0.6),
                "predictions": []
            },
            "long": {
                "days": self.config.get("prediction.long_term.window_days", 365),
                "confidence_threshold": self.config.get("prediction.long_term.confidence_threshold", 0.5),
                "predictions": []
            }
        }
        
        # Prediction storage
        self.predictions_dir = "data/predictions"
        os.makedirs(self.predictions_dir, exist_ok=True)
        
        # Load existing predictions
        self._load_predictions()
        
        logger.info("PredictionModel initialized")
    
    def _load_predictions(self):
        """Load existing predictions from files."""
        for timeframe in self.timeframes:
            predictions_file = os.path.join(self.predictions_dir, f"{timeframe}_predictions.json")
            if os.path.exists(predictions_file):
                try:
                    with open(predictions_file, 'r') as f:
                        self.timeframes[timeframe]["predictions"] = json.load(f)
                    logger.info(f"Loaded {len(self.timeframes[timeframe]['predictions'])} {timeframe}-term predictions")
                except Exception as e:
                    logger.error(f"Error loading {timeframe}-term predictions: {e}")
    
    def _save_predictions(self, timeframe: str):
        """
        Save predictions to file.
        
        Args:
            timeframe: Prediction timeframe ("short", "medium", or "long")
        """
        predictions_file = os.path.join(self.predictions_dir, f"{timeframe}_predictions.json")
        try:
            with open(predictions_file, 'w') as f:
                json.dump(self.timeframes[timeframe]["predictions"], f, indent=2)
            logger.info(f"Saved {len(self.timeframes[timeframe]['predictions'])} {timeframe}-term predictions")
        except Exception as e:
            logger.error(f"Error saving {timeframe}-term predictions: {e}")
    
    def start_prediction(self):
        """Start the prediction process."""
        if self.running:
            logger.warning("Prediction is already running")
            return
            
        logger.info("Starting prediction")
        self.running = True
        self.prediction_thread = threading.Thread(target=self._prediction_loop)
        self.prediction_thread.daemon = True
        self.prediction_thread.start()
    
    def stop_prediction(self):
        """Stop the prediction process."""
        if not self.running:
            logger.warning("Prediction is not running")
            return
            
        logger.info("Stopping prediction")
        self.running = False
        if self.prediction_thread:
            self.prediction_thread.join(timeout=30)
    
    def _prediction_loop(self):
        """Main prediction loop."""
        logger.info("Prediction loop started")
        
        while self.running:
            try:
                # Update predictions
                self._update_predictions()
                
                # Sleep for a while
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in prediction loop: {e}")
                time.sleep(300)  # Sleep for 5 minutes on error
    
    def _update_predictions(self):
        """Update predictions for all timeframes."""
        logger.info("Updating predictions")
        
        # Get processed data
        processed_data = self._get_processed_data()
        
        # Update predictions for each timeframe
        for timeframe in self.timeframes:
            self._update_timeframe_predictions(timeframe, processed_data)
            
            # Save predictions
            self._save_predictions(timeframe)
            
            # Update last prediction time
            self.last_prediction[timeframe] = datetime.now()
    
    def _get_processed_data(self) -> List[Dict[str, Any]]:
        """
        Get processed data for prediction.
        
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
                        
                    # Only get recent files (last 24 hours)
                    file_path = os.path.join(source_subdir, filename)
                    file_mtime = os.path.getmtime(file_path)
                    if time.time() - file_mtime > 86400:  # 24 hours
                        continue
                        
                    # Load data from file
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            processed_data.append(data)
                    except Exception as e:
                        logger.error(f"Error loading data from {file_path}: {e}")
                        
                    # Limit the number of files to process
                    if len(processed_data) >= 100:
                        break
        
        return processed_data
    
    def _update_timeframe_predictions(self, timeframe: str, processed_data: List[Dict[str, Any]]):
        """
        Update predictions for a specific timeframe.
        
        Args:
            timeframe: Prediction timeframe ("short", "medium", or "long")
            processed_data: List of processed data items
        """
        logger.info(f"Updating {timeframe}-term predictions")
        
        # Extract features from processed data
        features = self._extract_features(processed_data)
        
        # Generate predictions using the Bito engine
        raw_predictions = self._generate_predictions(timeframe, features)
        
        # Filter predictions based on confidence threshold
        confidence_threshold = self.timeframes[timeframe]["confidence_threshold"]
        filtered_predictions = [p for p in raw_predictions if p["confidence"] >= confidence_threshold]
        
        # Update predictions
        self.timeframes[timeframe]["predictions"] = filtered_predictions
        
        logger.info(f"Updated {len(filtered_predictions)} {timeframe}-term predictions")
    
    def _extract_features(self, processed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract features from processed data.
        
        Args:
            processed_data: List of processed data items
            
        Returns:
            List of feature dictionaries
        """
        # This is a placeholder for actual feature extraction
        # In a real system, this would extract meaningful features from the data
        
        features = []
        
        for data_item in processed_data:
            # Extract source type and name
            source_type = data_item.get("type", "unknown")
            source_name = data_item.get("source", "unknown")
            
            # Extract content based on source type
            if source_type == "social_media":
                posts = data_item.get("posts", [])
                for post in posts:
                    feature = self._extract_post_features(post, source_name)
                    features.append(feature)
            elif source_type == "mainstream_media":
                articles = data_item.get("articles", [])
                for article in articles:
                    feature = self._extract_article_features(article, source_name)
                    features.append(feature)
            elif source_type == "book":
                books = data_item.get("books", [])
                for book in books:
                    feature = self._extract_book_features(book, source_name)
                    features.append(feature)
            elif source_type == "custom":
                feature = self._extract_custom_features(data_item, source_name)
                features.append(feature)
        
        return features
    
    def _extract_post_features(self, post: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """
        Extract features from a social media post.
        
        Args:
            post: Social media post
            source_name: Name of the source
            
        Returns:
            Feature dictionary
        """
        # Extract sentiment
        sentiment = post.get("sentiment", {})
        sentiment_score = sentiment.get("compound", 0.0)
        
        # Extract entities
        entities = post.get("entities", [])
        entity_types = {}
        for entity in entities:
            entity_type = entity.get("type", "UNKNOWN")
            if entity_type not in entity_types:
                entity_types[entity_type] = 0
            entity_types[entity_type] += 1
        
        # Extract countries
        countries = post.get("countries", [])
        
        # Create feature dictionary
        feature = {
            "source_type": "social_media",
            "source_name": source_name,
            "text_sentiment": sentiment_score,
            "entity_presence": len(entities) > 0,
            "entity_count": len(entities),
            "country_count": len(countries),
            "historical_patterns": 0.5,  # Placeholder
            "temporal_factors": 0.5  # Placeholder
        }
        
        # Add entity type counts
        for entity_type, count in entity_types.items():
            feature[f"entity_{entity_type.lower()}_count"] = count
        
        return feature
    
    def _extract_article_features(self, article: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """
        Extract features from a mainstream media article.
        
        Args:
            article: Mainstream media article
            source_name: Name of the source
            
        Returns:
            Feature dictionary
        """
        # Extract sentiment
        sentiment = article.get("sentiment", {})
        sentiment_score = sentiment.get("compound", 0.0)
        
        # Extract entities
        entities = article.get("entities", [])
        entity_types = {}
        for entity in entities:
            entity_type = entity.get("type", "UNKNOWN")
            if entity_type not in entity_types:
                entity_types[entity_type] = 0
            entity_types[entity_type] += 1
        
        # Extract countries
        countries = article.get("countries", [])
        
        # Create feature dictionary
        feature = {
            "source_type": "mainstream_media",
            "source_name": source_name,
            "text_sentiment": sentiment_score,
            "entity_presence": len(entities) > 0,
            "entity_count": len(entities),
            "country_count": len(countries),
            "historical_patterns": 0.6,  # Placeholder
            "temporal_factors": 0.6  # Placeholder
        }
        
        # Add entity type counts
        for entity_type, count in entity_types.items():
            feature[f"entity_{entity_type.lower()}_count"] = count
        
        return feature
    
    def _extract_book_features(self, book: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """
        Extract features from a book.
        
        Args:
            book: Book
            source_name: Name of the source
            
        Returns:
            Feature dictionary
        """
        # Extract sentiment
        sentiment = book.get("sentiment", {})
        sentiment_score = sentiment.get("compound", 0.0)
        
        # Extract entities
        entities = book.get("entities", [])
        entity_types = {}
        for entity in entities:
            entity_type = entity.get("type", "UNKNOWN")
            if entity_type not in entity_types:
                entity_types[entity_type] = 0
            entity_types[entity_type] += 1
        
        # Extract countries
        countries = book.get("countries", [])
        
        # Create feature dictionary
        feature = {
            "source_type": "book",
            "source_name": source_name,
            "text_sentiment": sentiment_score,
            "entity_presence": len(entities) > 0,
            "entity_count": len(entities),
            "country_count": len(countries),
            "historical_patterns": 0.7,  # Placeholder
            "temporal_factors": 0.3  # Placeholder
        }
        
        # Add entity type counts
        for entity_type, count in entity_types.items():
            feature[f"entity_{entity_type.lower()}_count"] = count
        
        return feature
    
    def _extract_custom_features(self, data_item: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """
        Extract features from custom data.
        
        Args:
            data_item: Custom data item
            source_name: Name of the source
            
        Returns:
            Feature dictionary
        """
        # Create feature dictionary
        feature = {
            "source_type": "custom",
            "source_name": source_name,
            "text_sentiment": 0.0,
            "entity_presence": False,
            "entity_count": 0,
            "country_count": 0,
            "historical_patterns": 0.5,  # Placeholder
            "temporal_factors": 0.5  # Placeholder
        }
        
        # Extract data fields if available
        if "data" in data_item and isinstance(data_item["data"], dict):
            for field, value in data_item["data"].items():
                if field.endswith("_sentiment") and isinstance(value, dict):
                    feature["text_sentiment"] = value.get("compound", 0.0)
                elif field.endswith("_entities") and isinstance(value, list):
                    feature["entity_presence"] = len(value) > 0
                    feature["entity_count"] = len(value)
                    
                    # Count entity types
                    entity_types = {}
                    for entity in value:
                        entity_type = entity.get("type", "UNKNOWN")
                        if entity_type not in entity_types:
                            entity_types[entity_type] = 0
                        entity_types[entity_type] += 1
                    
                    # Add entity type counts
                    for entity_type, count in entity_types.items():
                        feature[f"entity_{entity_type.lower()}_count"] = count
                elif field.endswith("_countries") and isinstance(value, list):
                    feature["country_count"] = len(value)
        
        return feature
    
    def _generate_predictions(self, timeframe: str, features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate predictions for a specific timeframe.
        
        Args:
            timeframe: Prediction timeframe ("short", "medium", or "long")
            features: List of feature dictionaries
            
        Returns:
            List of prediction dictionaries
        """
        # This is a placeholder for actual prediction generation
        # In a real system, this would use the Bito engine to generate predictions
        
        # Get timeframe parameters
        days = self.timeframes[timeframe]["days"]
        
        # Use the Bito engine to predict risk scores
        risk_scores = self.bito_engine.predict(features)
        
        # Generate predictions
        predictions = []
        
        # Group features by country
        country_features = {}
        for i, feature in enumerate(features):
            countries = feature.get("countries", [])
            for country in countries:
                if country not in country_features:
                    country_features[country] = []
                country_features[country].append((feature, risk_scores[i]))
        
        # Generate predictions for each country
        for country, country_data in country_features.items():
            # Calculate average risk score
            avg_risk = sum(score for _, score in country_data) / len(country_data)
            
            # Generate prediction if risk score is high enough
            if avg_risk > 0.5:
                # Generate prediction date
                days_offset = int(np.random.random() * days)
                prediction_date = datetime.now() + timedelta(days=days_offset)
                
                # Generate prediction
                prediction = {
                    "country": country,
                    "type": self._generate_prediction_type(),
                    "description": self._generate_prediction_description(country),
                    "date": prediction_date.strftime("%Y-%m-%d"),
                    "confidence": round(avg_risk, 3),
                    "sources": [feature["source_name"] for feature, _ in country_data[:3]],
                    "generated_at": datetime.now().isoformat()
                }
                
                predictions.append(prediction)
        
        return predictions
    
    def _generate_prediction_type(self) -> str:
        """
        Generate a prediction type.
        
        Returns:
            Prediction type
        """
        # This is a placeholder for actual prediction type generation
        # In a real system, this would use more sophisticated logic
        
        types = [
            "terrorist_attack",
            "civil_unrest",
            "political_instability",
            "military_conflict",
            "cyber_attack",
            "infrastructure_attack",
            "assassination",
            "hostage_situation",
            "mass_shooting",
            "bombing"
        ]
        
        return np.random.choice(types)
    
    def _generate_prediction_description(self, country: str) -> str:
        """
        Generate a prediction description.
        
        Args:
            country: Country for the prediction
            
        Returns:
            Prediction description
        """
        # This is a placeholder for actual prediction description generation
        # In a real system, this would use more sophisticated logic
        
        descriptions = [
            f"Potential terrorist attack in {country}",
            f"Risk of civil unrest in {country}",
            f"Political instability in {country}",
            f"Military conflict in {country}",
            f"Cyber attack targeting infrastructure in {country}",
            f"Infrastructure attack in {country}",
            f"Assassination attempt in {country}",
            f"Hostage situation in {country}",
            f"Mass shooting in {country}",
            f"Bombing in {country}"
        ]
        
        return np.random.choice(descriptions)
    
    def update_predictions(self):
        """Update predictions for all timeframes."""
        self._update_predictions()
    
    def get_predictions(self, timeframe: str = "short") -> List[Dict[str, Any]]:
        """
        Get predictions for a specific timeframe.
        
        Args:
            timeframe: Prediction timeframe ("short", "medium", or "long")
            
        Returns:
            List of prediction dictionaries
        """
        if timeframe not in self.timeframes:
            logger.warning(f"Invalid timeframe: {timeframe}")
            return []
            
        return self.timeframes[timeframe]["predictions"]
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the prediction model.
        
        Returns:
            Dictionary containing the current state
        """
        return {
            "running": self.running,
            "last_prediction": {k: v.isoformat() for k, v in self.last_prediction.items()},
            "timeframes": {
                k: {
                    "days": v["days"],
                    "confidence_threshold": v["confidence_threshold"],
                    "predictions_count": len(v["predictions"])
                }
                for k, v in self.timeframes.items()
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the prediction model.
        
        Returns:
            Dictionary containing the current status
        """
        return {
            "running": self.running,
            "timeframes": {
                k: {
                    "days": v["days"],
                    "confidence_threshold": v["confidence_threshold"],
                    "predictions_count": len(v["predictions"]),
                    "last_update": self.last_prediction.get(k, datetime.now()).isoformat() if k in self.last_prediction else None
                }
                for k, v in self.timeframes.items()
            }
        }


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test prediction model
    from config import Configuration
    from bito_integration import BitoEngine
    
    # Create default configuration
    config = Configuration()
    
    # Create Bito engine
    bito = BitoEngine(config)
    
    # Create prediction model
    model = PredictionModel(config, bito)
    
    # Start prediction
    model.start_prediction()
    
    # Wait for a while
    print("Prediction started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # Stop prediction
    model.stop_prediction()
    print("Prediction stopped.")
