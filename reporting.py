#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Report Generator Module
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This module implements report generation for the Terror Alarm AI system.
"""

import os
import json
import time
import logging
import threading
import numpy as np
import matplotlib.pyplot as plt
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger("TerrorAlarm.ReportGenerator")

class ReportGenerator:
    """
    Report generation for the Terror Alarm AI system.
    """
    
    def __init__(self, config):
        """
        Initialize the ReportGenerator object.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.running = False
        self.reporting_thread = None
        self.last_report = {}
        
        # Report settings
        self.automated_reports = self.config.get("reporting.automated_reports.enabled", True)
        self.daily_reports = self.config.get("reporting.automated_reports.daily", True)
        self.weekly_reports = self.config.get("reporting.automated_reports.weekly", True)
        self.monthly_reports = self.config.get("reporting.automated_reports.monthly", True)
        
        # Alert thresholds
        self.alert_thresholds = {
            "critical": self.config.get("reporting.alert_thresholds.critical", 0.9),
            "high": self.config.get("reporting.alert_thresholds.high", 0.7),
            "medium": self.config.get("reporting.alert_thresholds.medium", 0.5),
            "low": self.config.get("reporting.alert_thresholds.low", 0.3)
        }
        
        # Report storage
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Create report subdirectories
        os.makedirs(os.path.join(self.reports_dir, "daily"), exist_ok=True)
        os.makedirs(os.path.join(self.reports_dir, "weekly"), exist_ok=True)
        os.makedirs(os.path.join(self.reports_dir, "monthly"), exist_ok=True)
        os.makedirs(os.path.join(self.reports_dir, "alerts"), exist_ok=True)
        os.makedirs(os.path.join(self.reports_dir, "custom"), exist_ok=True)
        
        logger.info("ReportGenerator initialized")
    
    def start_reporting(self):
        """Start the reporting process."""
        if self.running:
            logger.warning("Reporting is already running")
            return
            
        logger.info("Starting reporting")
        self.running = True
        self.reporting_thread = threading.Thread(target=self._reporting_loop)
        self.reporting_thread.daemon = True
        self.reporting_thread.start()
    
    def stop_reporting(self):
        """Stop the reporting process."""
        if not self.running:
            logger.warning("Reporting is not running")
            return
            
        logger.info("Stopping reporting")
        self.running = False
        if self.reporting_thread:
            self.reporting_thread.join(timeout=30)
    
    def _reporting_loop(self):
        """Main reporting loop."""
        logger.info("Reporting loop started")
        
        while self.running:
            try:
                # Check if it's time to generate reports
                current_time = datetime.now()
                
                # Generate daily report at midnight
                if self.automated_reports and self.daily_reports:
                    last_daily = self.last_report.get("daily")
                    if not last_daily or (current_time - last_daily).days >= 1:
                        if current_time.hour == 0:  # Midnight
                            self._generate_daily_report()
                            self.last_report["daily"] = current_time
                
                # Generate weekly report on Mondays
                if self.automated_reports and self.weekly_reports:
                    last_weekly = self.last_report.get("weekly")
                    if not last_weekly or (current_time - last_weekly).days >= 7:
                        if current_time.weekday() == 0 and current_time.hour == 1:  # Monday, 1 AM
                            self._generate_weekly_report()
                            self.last_report["weekly"] = current_time
                
                # Generate monthly report on the 1st of each month
                if self.automated_reports and self.monthly_reports:
                    last_monthly = self.last_report.get("monthly")
                    if not last_monthly or (current_time - last_monthly).days >= 28:
                        if current_time.day == 1 and current_time.hour == 2:  # 1st of month, 2 AM
                            self._generate_monthly_report()
                            self.last_report["monthly"] = current_time
                
                # Check for alerts
                self._check_for_alerts()
                
                # Sleep for a while
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in reporting loop: {e}")
                time.sleep(300)  # Sleep for 5 minutes on error
    
    def _generate_daily_report(self):
        """Generate a daily report."""
        logger.info("Generating daily report")
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create report data
        report_data = self._create_report_data("daily")
        
        # Generate report content
        report_content = self._format_report_content(report_data, "Daily Threat Report")
        
        # Save report
        report_file = os.path.join(self.reports_dir, "daily", f"daily_report_{current_date}.txt")
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        # Generate charts
        self._generate_report_charts(report_data, os.path.join(self.reports_dir, "daily", f"daily_charts_{current_date}"))
        
        logger.info(f"Daily report generated: {report_file}")
    
    def _generate_weekly_report(self):
        """Generate a weekly report."""
        logger.info("Generating weekly report")
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create report data
        report_data = self._create_report_data("weekly")
        
        # Generate report content
        report_content = self._format_report_content(report_data, "Weekly Threat Report")
        
        # Save report
        report_file = os.path.join(self.reports_dir, "weekly", f"weekly_report_{current_date}.txt")
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        # Generate charts
        self._generate_report_charts(report_data, os.path.join(self.reports_dir, "weekly", f"weekly_charts_{current_date}"))
        
        logger.info(f"Weekly report generated: {report_file}")
    
    def _generate_monthly_report(self):
        """Generate a monthly report."""
        logger.info("Generating monthly report")
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create report data
        report_data = self._create_report_data("monthly")
        
        # Generate report content
        report_content = self._format_report_content(report_data, "Monthly Threat Report")
        
        # Save report
        report_file = os.path.join(self.reports_dir, "monthly", f"monthly_report_{current_date}.txt")
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        # Generate charts
        self._generate_report_charts(report_data, os.path.join(self.reports_dir, "monthly", f"monthly_charts_{current_date}"))
        
        logger.info(f"Monthly report generated: {report_file}")
    
    def _check_for_alerts(self):
        """Check for alerts based on prediction data."""
        # This is a placeholder for actual alert checking
        # In a real system, this would check predictions against alert thresholds
        
        # Get prediction data
        try:
            predictions_dir = "data/predictions"
            if not os.path.exists(predictions_dir):
                return
                
            # Check short-term predictions
            short_predictions_file = os.path.join(predictions_dir, "short_predictions.json")
            if os.path.exists(short_predictions_file):
                with open(short_predictions_file, 'r') as f:
                    predictions = json.load(f)
                    
                    # Check for high-confidence predictions
                    for prediction in predictions:
                        confidence = prediction.get("confidence", 0.0)
                        
                        # Generate alerts based on confidence thresholds
                        if confidence >= self.alert_thresholds["critical"]:
                            self._generate_alert(prediction, "CRITICAL")
                        elif confidence >= self.alert_thresholds["high"]:
                            self._generate_alert(prediction, "HIGH")
                        elif confidence >= self.alert_thresholds["medium"]:
                            self._generate_alert(prediction, "MEDIUM")
                        elif confidence >= self.alert_thresholds["low"]:
                            self._generate_alert(prediction, "LOW")
        except Exception as e:
            logger.error(f"Error checking for alerts: {e}")
    
    def _generate_alert(self, prediction: Dict[str, Any], level: str):
        """
        Generate an alert based on a prediction.
        
        Args:
            prediction: Prediction data
            level: Alert level
        """
        # Check if alert already exists
        alert_id = f"{prediction['country']}_{prediction['type']}_{prediction['date']}"
        alert_file = os.path.join(self.reports_dir, "alerts", f"alert_{alert_id}.txt")
        
        if os.path.exists(alert_file):
            # Alert already exists
            return
            
        logger.info(f"Generating {level} alert for {prediction['country']}")
        
        # Create alert content
        alert_content = f"TERROR ALARM AI - {level} ALERT\n"
        alert_content += f"===================================\n\n"
        alert_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        alert_content += f"Alert Level: {level}\n\n"
        alert_content += f"Country: {prediction['country']}\n"
        alert_content += f"Threat Type: {prediction['type']}\n"
        alert_content += f"Predicted Date: {prediction['date']}\n"
        alert_content += f"Confidence: {prediction['confidence']:.2f}\n\n"
        alert_content += f"Description: {prediction['description']}\n\n"
        alert_content += f"Sources: {', '.join(prediction['sources'])}\n\n"
        alert_content += f"This alert was automatically generated by Terror Alarm AI.\n"
        alert_content += f"Please take appropriate action based on the threat level.\n"
        
        # Save alert
        with open(alert_file, 'w') as f:
            f.write(alert_content)
            
        logger.info(f"Alert generated: {alert_file}")
    
    def _create_report_data(self, report_type: str) -> Dict[str, Any]:
        """
        Create data for a report.
        
        Args:
            report_type: Type of report ("daily", "weekly", or "monthly")
            
        Returns:
            Dictionary containing report data
        """
        # This is a placeholder for actual report data creation
        # In a real system, this would gather data from various sources
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "report_type": report_type,
            "predictions": {
                "short_term": self._get_predictions("short"),
                "medium_term": self._get_predictions("medium"),
                "long_term": self._get_predictions("long")
            },
            "entities": {
                "dangerous_organizations": self._get_dangerous_organizations(),
                "terrorist_individuals": self._get_terrorist_individuals()
            },
            "country_iq_chart": self._get_country_iq_chart(),
            "data_sources": self._get_data_sources(),
            "alerts": self._get_recent_alerts(report_type)
        }
        
        return report_data
    
    def _format_report_content(self, report_data: Dict[str, Any], title: str) -> str:
        """
        Format report data as text content.
        
        Args:
            report_data: Report data
            title: Report title
            
        Returns:
            Formatted report content
        """
        # Create report content
        content = f"TERROR ALARM AI - {title}\n"
        content += f"===================================\n\n"
        content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add predictions
        content += f"PREDICTIONS\n"
        content += f"-----------\n\n"
        
        # Short-term predictions
        content += f"Short-term Predictions:\n"
        for prediction in report_data["predictions"]["short_term"]:
            content += f"- {prediction['country']}: {prediction['description']} ({prediction['date']}, confidence: {prediction['confidence']:.2f})\n"
        content += f"\n"
        
        # Medium-term predictions
        content += f"Medium-term Predictions:\n"
        for prediction in report_data["predictions"]["medium_term"]:
            content += f"- {prediction['country']}: {prediction['description']} ({prediction['date']}, confidence: {prediction['confidence']:.2f})\n"
        content += f"\n"
        
        # Long-term predictions
        content += f"Long-term Predictions:\n"
        for prediction in report_data["predictions"]["long_term"]:
            content += f"- {prediction['country']}: {prediction['description']} ({prediction['date']}, confidence: {prediction['confidence']:.2f})\n"
        content += f"\n"
        
        # Add dangerous organizations
        content += f"DANGEROUS ORGANIZATIONS\n"
        content += f"----------------------\n\n"
        for org in report_data["entities"]["dangerous_organizations"]:
            content += f"- {org['name']} ({org['type']}, threat level: {org['threat_level']})\n"
            content += f"  Aliases: {', '.join(org['aliases'])}\n"
            content += f"  Regions: {', '.join(org['regions'])}\n"
            content += f"  Description: {org['description']}\n\n"
        
        # Add terrorist individuals
        content += f"TERRORIST INDIVIDUALS\n"
        content += f"--------------------\n\n"
        for ind in report_data["entities"]["terrorist_individuals"]:
            content += f"- {ind['name']} ({ind['organization']}, threat level: {ind['threat_level']})\n"
            content += f"  Aliases: {', '.join(ind['aliases'])}\n"
            content += f"  Nationality: {ind['nationality']}\n"
            content += f"  Status: {ind['status']}\n"
            content += f"  Description: {ind['description']}\n\n"
        
        # Add country IQ chart
        content += f"COUNTRY IQ CHART\n"
        content += f"---------------\n\n"
        # Sort countries by IQ score (descending)
        sorted_countries = sorted(report_data["country_iq_chart"].items(), key=lambda x: x[1], reverse=True)
        for country, iq in sorted_countries[:20]:  # Top 20 countries
            content += f"- {country}: {iq}\n"
        content += f"\n"
        
        # Add data sources
        content += f"DATA SOURCES\n"
        content += f"-----------\n\n"
        content += f"Social Media Sources: {', '.join(report_data['data_sources']['s
(Content truncated due to size limit. Use line ranges to read in chunks)