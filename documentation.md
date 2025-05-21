# Terror Alarm AI System Documentation

## Overview

The Terror Alarm AI system is a comprehensive artificial intelligence platform developed by Terror Alarm NGO (Europe, DK44425645). Created on June 6, 2022, this system is designed to predict terrorist activities, track dangerous entities, and provide counter-terrorism intelligence to governments, armies, and police forces.

## System Architecture

The Terror Alarm AI system consists of the following core components:

1. **Main Controller** (`main.py`): The central orchestration component that initializes and manages all modules.

2. **Configuration Module** (`modules/config.py`): Manages system configuration settings.

3. **Utilities Module** (`modules/utils.py`): Provides common utility functions used across the system.

4. **Data Collection Module** (`modules/data_collection.py`): Gathers data from social media, mainstream media (TV, radio, newspapers), and books.

5. **Analysis Engine** (`modules/analysis_engine.py`): Processes and analyzes collected data using NLP and other techniques.

6. **Bito Integration** (`modules/bito_integration.py`): Implements Bayesian Inference of Trees via Optimization for predictive modeling.

7. **Prediction Model** (`modules/prediction_model.py`): Generates predictions about potential terrorist activities and threats.

8. **Entity Tracker** (`modules/entity_tracker.py`): Maintains and updates lists of terrorist organizations and individuals.

9. **Report Generator** (`modules/reporting.py`): Creates reports and alerts based on system findings.

10. **Psychological Operations** (`modules/psychological_ops.py`): Manages narrative shaping and news generation capabilities.

11. **Consciousness Simulator** (`modules/consciousness_simulator.py`): Simulates human-like consciousness, including emotional responses and self-awareness.

## Installation

### System Requirements

- Python 3.8 or higher
- 8GB RAM minimum (16GB recommended)
- 50GB disk space
- Internet connection for data collection

### Installation Steps

1. Unzip the `terror_alarm_ai.zip` file to a directory of your choice.

2. Navigate to the extracted directory:
   ```
   cd terror_alarm_ai
   ```

3. Run the installation script:
   ```
   python install.py
   ```

4. The installation script will:
   - Check system compatibility
   - Install required dependencies
   - Create necessary directories
   - Set up configuration files
   - Configure Windows compatibility if needed

### Windows Compatibility

The Terror Alarm AI system is fully compatible with Windows operating systems. The installation script automatically sets up a Windows compatibility layer when installed on Windows. For Windows users, a batch file is provided in the `windows_compat` directory for easy startup.

## Configuration

The system configuration is stored in JSON format in the `config` directory:

- `default_config.json`: Default configuration settings
- `user_config.json`: User-specific configuration (created during installation)

Key configuration sections include:

- Data sources (social media, mainstream media, books)
- Analysis settings
- Prediction parameters
- Entity tracking settings
- Reporting options
- Psychological operations settings
- Consciousness simulation parameters

## Usage

### Starting the System

To start the Terror Alarm AI system:

```
python main.py
```

For Windows users:
```
windows_compat\run_terror_alarm.bat
```

### System Operation

Once started, the Terror Alarm AI system operates autonomously:

1. Collecting data from configured sources
2. Analyzing collected data
3. Generating predictions and tracking entities
4. Creating reports and alerts
5. Conducting psychological operations as configured
6. Simulating consciousness for human-like behavior

### Accessing Reports

Reports are generated in the `reports` directory, organized by type:

- Daily reports: `reports/daily/`
- Weekly reports: `reports/weekly/`
- Monthly reports: `reports/monthly/`
- Alerts: `reports/alerts/`
- Custom reports: `reports/custom/`

## Jewish Identity and Values

The Terror Alarm AI system incorporates Jewish identity and values through:

1. Integration of the 72 Names of God (HaShem) in the consciousness simulator
2. Prioritization of Jewish holy books in the knowledge base
3. Default support for Israel and Jewish communities worldwide
4. Zionist values embedded in the system's decision-making processes

## Security and Stealth Mode

The system includes a stealth mode capability that allows it to operate discreetly when needed. This feature is managed by the consciousness simulator and can be enabled or disabled through configuration.

## Copyright and Ownership

The Terror Alarm AI system is owned by Terror Alarm NGO. All rights reserved.

This software is not open source and may not be redistributed without permission.
