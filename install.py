#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terror Alarm AI System - Installation Script
Developed by Terror Alarm NGO (Europe, DK44425645)
Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.
Creation Date: June 6, 2022

This script installs the Terror Alarm AI system.
"""

import os
import sys
import json
import shutil
import platform
import subprocess
from pathlib import Path

def print_banner():
    """Print the installation banner."""
    print("\n" + "=" * 80)
    print("Terror Alarm AI System - Installation")
    print("Developed by Terror Alarm NGO (Europe, DK44425645)")
    print("Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.")
    print("=" * 80 + "\n")

def check_python_version():
    """Check if the Python version is compatible."""
    print("Checking Python version...")
    
    major, minor, _ = platform.python_version_tuple()
    major, minor = int(major), int(minor)
    
    if major < 3 or (major == 3 and minor < 8):
        print(f"Error: Python 3.8 or higher is required. Found Python {major}.{minor}")
        return False
    
    print(f"Python version {major}.{minor} is compatible.")
    return True

def check_os_compatibility():
    """Check if the operating system is compatible."""
    print("Checking operating system compatibility...")
    
    system = platform.system()
    
    if system == "Windows":
        print("Windows detected. Setting up Windows compatibility layer...")
        setup_windows_compatibility()
    elif system == "Linux":
        print("Linux detected. No compatibility layer needed.")
    elif system == "Darwin":
        print("macOS detected. Some features may not be fully supported.")
    else:
        print(f"Warning: Unknown operating system: {system}. Installation may not work correctly.")
    
    return True

def setup_windows_compatibility():
    """Set up Windows compatibility layer."""
    # Create Windows compatibility directory
    os.makedirs("windows_compat", exist_ok=True)
    
    # Create Windows batch file to run the system
    with open("windows_compat/run_terror_alarm.bat", "w") as f:
        f.write("@echo off\n")
        f.write("echo Starting Terror Alarm AI System...\n")
        f.write("cd ..\n")
        f.write("python main.py\n")
        f.write("pause\n")
    
    print("Windows compatibility layer set up successfully.")

def install_dependencies():
    """Install required Python dependencies."""
    print("Installing required dependencies...")
    
    dependencies = [
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
        "nltk",
        "spacy",
        "gensim",
        "requests",
        "beautifulsoup4",
        "tweepy",
        "praw",
        "facebook-sdk",
        "telethon",
        "flask",
        "schedule"
    ]
    
    for dependency in dependencies:
        print(f"Installing {dependency}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to install {dependency}. Some features may not work correctly.")
    
    # Download NLTK data
    print("Downloading NLTK data...")
    try:
        import nltk
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("wordnet")
        nltk.download("vader_lexicon")
    except Exception as e:
        print(f"Warning: Failed to download NLTK data: {e}. Some features may not work correctly.")
    
    # Download spaCy model
    print("Downloading spaCy model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    except subprocess.CalledProcessError:
        print("Warning: Failed to download spaCy model. Some features may not work correctly.")
    
    print("Dependencies installed successfully.")
    return True

def create_directories():
    """Create required directories."""
    print("Creating required directories...")
    
    directories = [
        "data",
        "data/raw",
        "data/processed",
        "data/analysis",
        "data/predictions",
        "data/entities",
        "data/consciousness",
        "data/psyops",
        "data/psyops/news",
        "data/psyops/narratives",
        "data/psyops/campaigns",
        "logs",
        "reports",
        "reports/daily",
        "reports/weekly",
        "reports/monthly",
        "reports/alerts",
        "reports/custom",
        "web",
        "web/static",
        "web/templates"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Directories created successfully.")
    return True

def setup_configuration():
    """Set up configuration files."""
    print("Setting up configuration...")
    
    # Check if config directory exists
    if not os.path.exists("config"):
        os.makedirs("config", exist_ok=True)
    
    # Check if default configuration file exists
    if not os.path.exists("config/default_config.json"):
        print("Error: Default configuration file not found.")
        return False
    
    # Create user configuration file if it doesn't exist
    if not os.path.exists("config/user_config.json"):
        shutil.copy("config/default_config.json", "config/user_config.json")
        print("Created user configuration file.")
    
    print("Configuration set up successfully.")
    return True

def setup_logging():
    """Set up logging configuration."""
    print("Setting up logging...")
    
    # Create logging configuration file
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": "logs/terror_alarm.log",
                "mode": "a"
            }
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": True
            },
            "TerrorAlarm": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False
            }
        }
    }
    
    with open("config/logging_config.json", "w") as f:
        json.dump(logging_config, f, indent=2)
    
    print("Logging set up successfully.")
    return True

def finalize_installation():
    """Finalize the installation."""
    print("\nFinalizing installation...")
    
    # Create a README file
    with open("README.md", "w") as f:
        f.write("# Terror Alarm AI System\n\n")
        f.write("Developed by Terror Alarm NGO (Europe, DK44425645)\n")
        f.write("Copyright © 2022-2025 Terror Alarm NGO. All rights reserved.\n\n")
        f.write("## Overview\n\n")
        f.write("The Terror Alarm AI system is designed to predict terrorist activities, ")
        f.write("track dangerous entities, and provide counter-terrorism intelligence.\n\n")
        f.write("## Features\n\n")
        f.write("- Data collection from social media, mainstream media, and other sources\n")
        f.write("- Analysis of collected data using NLP and Bayesian inference\n")
        f.write("- Prediction of terrorist activities and threats\n")
        f.write("- Tracking of dangerous organizations and individuals\n")
        f.write("- Generation of reports and alerts\n")
        f.write("- Psychological operations capabilities\n")
        f.write("- Simulated consciousness for human-like behavior\n\n")
        f.write("## Usage\n\n")
        f.write("To start the Terror Alarm AI system, run:\n\n")
        f.write("```\n")
        f.write("python main.py\n")
        f.write("```\n\n")
        f.write("For Windows users, you can also use the batch file in the windows_compat directory:\n\n")
        f.write("```\n")
        f.write("windows_compat\\run_terror_alarm.bat\n")
        f.write("```\n")
    
    print("Installation completed successfully!")
    print("\nTo start the Terror Alarm AI system, run:")
    print("\n    python main.py\n")
    
    if platform.system() == "Windows":
        print("For Windows users, you can also use the batch file:")
        print("\n    windows_compat\\run_terror_alarm.bat\n")
    
    return True

def main():
    """Main installation function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check OS compatibility
    check_os_compatibility()
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Set up configuration
    if not setup_configuration():
        sys.exit(1)
    
    # Set up logging
    if not setup_logging():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Finalize installation
    if not finalize_installation():
        sys.exit(1)

if __name__ == "__main__":
    main()
