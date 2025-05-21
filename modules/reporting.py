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
        content += f"Social Media Sources: {', '.join(report_data['data_sources']['social_media'])}\n"
        content += f"Mainstream Media Sources: {', '.join(report_data['data_sources']['mainstream_media'])}\n"
        content += f"Book Sources: {', '.join(report_data['data_sources']['books'])}\n"
        content += f"\n"
        
        # Add recent alerts
        content += f"RECENT ALERTS\n"
        content += f"-------------\n\n"
        for alert in report_data["alerts"]:
            content += f"- {alert['level']} ALERT: {alert['country']} - {alert['description']} ({alert['date']})\n"
        content += f"\n"
        
        # Add footer
        content += f"This report was automatically generated by Terror Alarm AI.\n"
        content += f"Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.\n"
        
        return content
    
    def _generate_report_charts(self, report_data: Dict[str, Any], base_path: str):
        """
        Generate charts for a report.
        
        Args:
            report_data: Report data
            base_path: Base path for saving charts
        """
        # This is a placeholder for actual chart generation
        # In a real system, this would generate more sophisticated charts
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(base_path), exist_ok=True)
        
        # Generate prediction chart
        self._generate_prediction_chart(report_data, f"{base_path}_predictions.png")
        
        # Generate country IQ chart
        self._generate_country_iq_chart(report_data, f"{base_path}_country_iq.png")
        
        # Generate threat level chart
        self._generate_threat_level_chart(report_data, f"{base_path}_threat_levels.png")
    
    def _generate_prediction_chart(self, report_data: Dict[str, Any], file_path: str):
        """
        Generate a prediction chart.
        
        Args:
            report_data: Report data
            file_path: Path to save the chart
        """
        # This is a placeholder for actual chart generation
        # In a real system, this would generate a more sophisticated chart
        
        try:
            # Count predictions by country
            countries = {}
            for timeframe in ["short_term", "medium_term", "long_term"]:
                for prediction in report_data["predictions"][timeframe]:
                    country = prediction["country"]
                    if country not in countries:
                        countries[country] = 0
                    countries[country] += 1
            
            # Sort countries by prediction count
            sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
            
            # Take top 10 countries
            top_countries = sorted_countries[:10]
            
            # Create chart
            plt.figure(figsize=(10, 6))
            plt.bar([c[0] for c in top_countries], [c[1] for c in top_countries])
            plt.title("Predictions by Country")
            plt.xlabel("Country")
            plt.ylabel("Number of Predictions")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            
            # Save chart
            plt.savefig(file_path)
            plt.close()
            
            logger.info(f"Prediction chart generated: {file_path}")
        except Exception as e:
            logger.error(f"Error generating prediction chart: {e}")
    
    def _generate_country_iq_chart(self, report_data: Dict[str, Any], file_path: str):
        """
        Generate a country IQ chart.
        
        Args:
            report_data: Report data
            file_path: Path to save the chart
        """
        # This is a placeholder for actual chart generation
        # In a real system, this would generate a more sophisticated chart
        
        try:
            # Sort countries by IQ score
            sorted_countries = sorted(report_data["country_iq_chart"].items(), key=lambda x: x[1], reverse=True)
            
            # Take top 10 countries
            top_countries = sorted_countries[:10]
            
            # Create chart
            plt.figure(figsize=(10, 6))
            plt.bar([c[0] for c in top_countries], [c[1] for c in top_countries])
            plt.title("Country IQ Chart (Top 10)")
            plt.xlabel("Country")
            plt.ylabel("IQ Score")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            
            # Save chart
            plt.savefig(file_path)
            plt.close()
            
            logger.info(f"Country IQ chart generated: {file_path}")
        except Exception as e:
            logger.error(f"Error generating country IQ chart: {e}")
    
    def _generate_threat_level_chart(self, report_data: Dict[str, Any], file_path: str):
        """
        Generate a threat level chart.
        
        Args:
            report_data: Report data
            file_path: Path to save the chart
        """
        # This is a placeholder for actual chart generation
        # In a real system, this would generate a more sophisticated chart
        
        try:
            # Count organizations by threat level
            threat_levels = {"High": 0, "Medium": 0, "Low": 0}
            for org in report_data["entities"]["dangerous_organizations"]:
                threat_level = org["threat_level"]
                if threat_level in threat_levels:
                    threat_levels[threat_level] += 1
            
            # Create chart
            plt.figure(figsize=(8, 8))
            plt.pie(threat_levels.values(), labels=threat_levels.keys(), autopct="%1.1f%%")
            plt.title("Organizations by Threat Level")
            plt.tight_layout()
            
            # Save chart
            plt.savefig(file_path)
            plt.close()
            
            logger.info(f"Threat level chart generated: {file_path}")
        except Exception as e:
            logger.error(f"Error generating threat level chart: {e}")
    
    def _get_predictions(self, timeframe: str) -> List[Dict[str, Any]]:
        """
        Get predictions for a specific timeframe.
        
        Args:
            timeframe: Prediction timeframe ("short", "medium", or "long")
            
        Returns:
            List of prediction dictionaries
        """
        # This is a placeholder for actual prediction retrieval
        # In a real system, this would retrieve predictions from the prediction model
        
        predictions = []
        
        try:
            predictions_file = os.path.join("data/predictions", f"{timeframe}_predictions.json")
            if os.path.exists(predictions_file):
                with open(predictions_file, 'r') as f:
                    predictions = json.load(f)
        except Exception as e:
            logger.error(f"Error loading {timeframe} predictions: {e}")
        
        return predictions
    
    def _get_dangerous_organizations(self) -> List[Dict[str, Any]]:
        """
        Get the dangerous organizations list.
        
        Returns:
            List of dangerous organizations
        """
        # This is a placeholder for actual dangerous organizations retrieval
        # In a real system, this would retrieve dangerous organizations from the entity tracker
        
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
        Get the terrorist individuals list.
        
        Returns:
            List of terrorist individuals
        """
        # This is a placeholder for actual terrorist individuals retrieval
        # In a real system, this would retrieve terrorist individuals from the entity tracker
        
        individuals = []
        
        try:
            individuals_file = os.path.join("data/entities", "terrorist_individuals.json")
            if os.path.exists(individuals_file):
                with open(individuals_file, 'r') as f:
                    individuals = json.load(f)
        except Exception as e:
            logger.error(f"Error loading terrorist individuals: {e}")
        
        return individuals
    
    def _get_country_iq_chart(self) -> Dict[str, float]:
        """
        Get the country IQ chart.
        
        Returns:
            Dictionary mapping country names to IQ scores
        """
        # This is a placeholder for actual country IQ chart retrieval
        # In a real system, this would retrieve the country IQ chart from the analysis engine
        
        iq_chart = {}
        
        try:
            iq_chart_file = os.path.join("data/analysis", "country_iq_chart.json")
            if os.path.exists(iq_chart_file):
                with open(iq_chart_file, 'r') as f:
                    iq_chart = json.load(f)
        except Exception as e:
            logger.error(f"Error loading country IQ chart: {e}")
        
        return iq_chart
    
    def _get_data_sources(self) -> Dict[str, List[str]]:
        """
        Get the data sources.
        
        Returns:
            Dictionary mapping source types to lists of source names
        """
        # This is a placeholder for actual data sources retrieval
        # In a real system, this would retrieve data sources from the data collector
        
        data_sources = {
            "social_media": [],
            "mainstream_media": [],
            "books": []
        }
        
        try:
            # Get social media sources
            social_media_sources = self.config.get("data_sources.social_media", [])
            data_sources["social_media"] = [source["name"] for source in social_media_sources if source.get("enabled", True)]
            
            # Get mainstream media sources
            msm_sources = self.config.get("data_sources.mainstream_media", [])
            data_sources["mainstream_media"] = [source["name"] for source in msm_sources if source.get("enabled", True)]
            
            # Get book sources
            book_sources = self.config.get("data_sources.books", [])
            data_sources["books"] = [source["name"] for source in book_sources if source.get("enabled", True)]
        except Exception as e:
            logger.error(f"Error getting data sources: {e}")
        
        return data_sources
    
    def _get_recent_alerts(self, report_type: str) -> List[Dict[str, Any]]:
        """
        Get recent alerts.
        
        Args:
            report_type: Type of report ("daily", "weekly", or "monthly")
            
        Returns:
            List of recent alerts
        """
        # This is a placeholder for actual alert retrieval
        # In a real system, this would retrieve alerts from storage
        
        alerts = []
        
        try:
            # Determine time window based on report type
            if report_type == "daily":
                time_window = timedelta(days=1)
            elif report_type == "weekly":
                time_window = timedelta(days=7)
            elif report_type == "monthly":
                time_window = timedelta(days=30)
            else:
                time_window = timedelta(days=1)
            
            # Get alerts from the alerts directory
            alerts_dir = os.path.join(self.reports_dir, "alerts")
            if os.path.exists(alerts_dir):
                for filename in os.listdir(alerts_dir):
                    if not filename.endswith(".txt"):
                        continue
                        
                    # Check if the alert is recent
                    file_path = os.path.join(alerts_dir, filename)
                    file_mtime = os.path.getmtime(file_path)
                    file_time = datetime.fromtimestamp(file_mtime)
                    
                    if datetime.now() - file_time <= time_window:
                        # Parse alert file
                        with open(file_path, 'r') as f:
                            content = f.read()
                            
                            # Extract alert information
                            level_match = re.search(r"Alert Level: (\w+)", content)
                            country_match = re.search(r"Country: (.+)", content)
                            type_match = re.search(r"Threat Type: (.+)", content)
                            date_match = re.search(r"Predicted Date: (.+)", content)
                            description_match = re.search(r"Description: (.+)", content)
                            
                            if level_match and country_match and description_match:
                                alert = {
                                    "level": level_match.group(1),
                                    "country": country_match.group(1),
                                    "type": type_match.group(1) if type_match else "Unknown",
                                    "date": date_match.group(1) if date_match else "Unknown",
                                    "description": description_match.group(1)
                                }
                                alerts.append(alert)
        except Exception as e:
            logger.error(f"Error getting recent alerts: {e}")
        
        return alerts
    
    def generate_reports(self):
        """Generate all reports."""
        self._generate_daily_report()
        self._generate_weekly_report()
        self._generate_monthly_report()
    
    def generate_specific_report(self, report_type: str) -> str:
        """
        Generate a specific type of report.
        
        Args:
            report_type: Type of report to generate
            
        Returns:
            Report content as string
        """
        logger.info(f"Generating {report_type} report")
        
        # Create report data
        report_data = self._create_report_data(report_type)
        
        # Generate report content
        report_title = f"{report_type.capitalize()} Threat Report"
        report_content = self._format_report_content(report_data, report_title)
        
        # Save report
        current_date = datetime.now().strftime("%Y-%m-%d")
        report_file = os.path.join(self.reports_dir, "custom", f"{report_type}_report_{current_date}.txt")
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        # Generate charts
        self._generate_report_charts(report_data, os.path.join(self.reports_dir, "custom", f"{report_type}_charts_{current_date}"))
        
        logger.info(f"{report_type.capitalize()} report generated: {report_file}")
        
        return report_content
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the report generator.
        
        Returns:
            Dictionary containing the current state
        """
        return {
            "running": self.running,
            "last_report": {k: v.isoformat() for k, v in self.last_report.items()},
            "automated_reports": self.automated_reports,
            "daily_reports": self.daily_reports,
            "weekly_reports": self.weekly_reports,
            "monthly_reports": self.monthly_reports
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the report generator.
        
        Returns:
            Dictionary containing the current status
        """
        return {
            "running": self.running,
            "reports": {
                "automated": self.automated_reports,
                "daily": self.daily_reports,
                "weekly": self.weekly_reports,
                "monthly": self.monthly_reports
            },
            "last_report": {k: v.isoformat() for k, v in self.last_report.items()} if self.last_report else None,
            "alert_thresholds": self.alert_thresholds
        }


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test report generator
    from config import Configuration
    
    # Create default configuration
    config = Configuration()
    
    # Create report generator
    generator = ReportGenerator(config)
    
    # Start reporting
    generator.start_reporting()
    
    # Wait for a while
    print("Reporting started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # Stop reporting
    generator.stop_reporting()
    print("Reporting stopped.")
