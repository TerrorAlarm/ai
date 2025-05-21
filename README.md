# ai
# TERROR ALARM - Predictive Analytics AI
## Short Description: Terror Alarm is a cutting-edge, AI-driven platform developed by Terror Alarm nonprofit NGO to combat terrorism and promote global security. Its proprietary Strategist Predictive AI aggregates and analyzes vast data from diverse sources—news, social media, and intelligence feeds—to generate real-time news, predictions, and insights. Focused on preventing terror acts and supporting Israel and Jewish values, it operates independently, free from external agendas, and serves as a vital tool for safer communities in NATO states and allied nations.


## Overview
Terror Alarm is the world’s first “Strategist” and “anti-terror” agentic predictive AI that covers News and creates Views for countries and regions. The proprietary AI developed for each country - aggregates all news from all media sources including news websites, blogs, the Deep Web, the Dark Web, Social Media (X, Telegram, Reddit, Facebook, Instagram, YouTube, TikTok, Bluesky, Threats), newspapers, magazines, TV channels, radio stations and when legally possible, private messages between people. The AI also monitors data from internet-of-things devices, leaked Emails and data, and it uses data from intercepted communications legally obtained and shared by intelligence services.

## Key features:
- Data collection from X and other platforms
- Text preprocessing and feature extraction
- Custom Decision Tree implementation
- Confidence scoring and prediction explanations
- Batch processing capabilities
- Comprehensive API for integration

## Installation

### Requirements
- Python 3.8 or higher
- NumPy
- Pandas
- scikit-learn
- Matplotlib

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/TerrorAlarm/ai
```

2. Install the package:
```bash
pip install -e .
```

Alternatively, you can install directly from the package:
```bash
```

## Usage

### Basic Usage

```python
from terroralarm import AI

# Initialize Terror Alarm
ta = TA()

# Collect data from social media
posts = ta.collect_data("artificial intelligence", count=100)

# Train a model
model_path = ta.train_model(tweets, model_name="ai_model")

# Make predictions
predictions = ta.predict(tweets, model_name="ai_model")

# Analyze a query
analysis = ta.train_model("climate change", model_name="ai_model")
```

### Advanced Usage

#### Custom Configuration

```python
# Update configuration
ta.update_config({
    'max_tweets': 200,
    'model_params': {
        'max_depth': 10,
        'criterion': 'entropy',
        'task': 'classification'
    }
})
```

#### Cross-Validation

```python
import numpy as np

# Split data for cross-validation
n_samples = len(tweets)
n_folds = 5
fold_size = n_samples // n_folds

# Create synthetic labels for demonstration
y = np.random.randint(0, 2, size=n_samples)

# Perform cross-validation
accuracies = []

for fold in range(n_folds):
    # Create train/test split
    test_indices = list(range(fold * fold_size, (fold + 1) * fold_size))
    train_indices = [i for i in range(n_samples) if i not in test_indices]
    
    train_tweets = [tweets[i] for i in train_indices]
    test_tweets = [tweets[i] for i in test_indices]
    
    train_y = y[train_indices]
    test_y = y[test_indices]
    
    # Train model
    ta.train_model(train_tweets, train_y, model_name=f"fold{fold}")
    
    # Make predictions
    predictions = ta.predict(test_tweets, model_name=f"fold{fold}")
    
    # Calculate accuracy
    pred_values = [p['prediction'] for p in predictions]
    accuracy = np.mean([p == t for p, t in zip(pred_values, test_y)])
    accuracies.append(accuracy)

# Print results
print(f"Mean accuracy: {np.mean(accuracies):.4f} ± {np.std(accuracies):.4f}")
```

## Components

### Data Collection Module
- `XDataFetcher`: Interface with Twitter API endpoints
- `DataStorage`: Store collected data in structured format
- `RateLimitHandler`: Manage API rate limits
- `ErrorHandler`: Handle API errors and connection issues

### Preprocessing Module
- `TextCleaner`: Remove noise, special characters, URLs
- `FeatureExtractor`: Extract relevant features from posts
- `Tokenizer`: Convert text to tokens
- `Vectorizer`: Transform tokens into numerical vectors
- `SentimentAnalyzer`: Extract sentiment features

### Decision Tree Model
- `Node`: Basic tree node structure
- `DecisionTree`: Main tree implementation
- `SplitFinder`: Find optimal splits in data
- `TreeBuilder`: Build tree from training data
- `TreeVisualizer`: Visualize decision tree structure
- `Pruner`: Prune tree to prevent overfitting

### Prediction Module
- `Predictor`: Generate predictions for new data
- `ConfidenceCalculator`: Calculate prediction confidence
- `ExplanationGenerator`: Explain prediction path
- `BatchPredictor`: Process multiple predictions efficiently

### Integration API
- `Pipeline`: Connect all components in workflow
- `ModelManager`: Save/load trained models
- `ConfigManager`: Handle configuration settings
- `TA`: Main class providing unified interface

## License

The license for Terror Alarm's Strategist Predictive AI is private. Any use, reproduction, or forking of the source code requires explicit written permission from the copyright holders. Unauthorized use is strictly prohibited.

## Contact

For more information, contact Terror Alarm at info@terroralarm.org.
