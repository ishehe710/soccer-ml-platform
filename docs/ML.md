# Machine Learning

## Overview

Briefly explain the purpose of the machine learning system.

The machine learning component predicts upcoming soccer matches using only
information available before each match.

For each match, the system produces:

Home team win: x%
Draw: y%
Away team win: z%
Predicted score: a-b

The milestone compares multiple modeling approaches before selecting a
production model for inference.


## 1. ML Objective

### 1.1 Match Outcome Prediction

Define the three-class classification problem:

- Home win
- Draw
- Away win

Explain that the output should be probabilities rather than only a predicted
class.

### 1.2 Score Prediction

Define the goal prediction problem:

- Home goals
- Away goals

Explain how the predicted final score is generated.

### 1.3 Constraints

- Only pre-match information may be used.
- Future information must never influence historical predictions.
- Training and evaluation must preserve chronological ordering.
- Production predictions must use the same feature-generation process used
  during training.


## 2. ML Architecture

Describe the overall ML workflow.

PostgreSQL
    ↓
ML Data Processing
    ↓
Feature Engineering
    ↓
Training Dataset
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Model Selection
    ↓
Production Model
    ↓
Inference

## 3. Exploratory Data Analysis

### 3.1 Dataset Overview
- Number of competitions
- Number of seasons
- Number of matches
- Number of teams
- Date range

### 3.2 Data Completeness
- Missing values
- Missing match statistics
- Missing player statistics
- Coverage by season and competition

### 3.3 Match Outcome Distribution
- Home wins
- Draws
- Away wins
- Class balance

### 3.4 Goal Distribution
- Home goals
- Away goals
- Total goals
- Common scorelines

### 3.5 Feature Availability
Determine which historical variables are sufficiently complete to use
for feature engineering.

### 3.6 Data Quality
- Duplicates
- Invalid scores
- Incomplete matches
- Postponed/cancelled matches
- Unexpected values

### 3.7 EDA Findings
Summarize findings that affect data processing, feature engineering,
and model selection.

## 4. ML Data Processing

### 4.1 Data Sources

Document which PostgreSQL tables are used.

Examples:

- matches
- teams
- standings
- match_stats
- player_stats

### 4.2 Historical Match Dataset

Explain how database records are transformed into one observation per match.

### 4.3 Data Cleaning

Document:

- Missing values
- Invalid/incomplete matches
- Postponed/cancelled matches
- Duplicate records
- Required historical data

### 4.4 Target Construction

Define:

outcome:
- HOME_WIN
- DRAW
- AWAY_WIN

score:
- home_goals
- away_goals


## 5. Feature Engineering

### 5.1 Feature Engineering Objective

Explain that features represent information known immediately before kickoff.

### 5.2 Team Form Features

Examples:

- Points over previous N matches
- Wins over previous N matches
- Draws over previous N matches
- Losses over previous N matches
- Form streak

### 5.3 Attacking Features

Examples:

- Average goals scored
- Shots
- Shots on target
- Expected goals (if available)

### 5.4 Defensive Features

Examples:

- Average goals conceded
- Shots allowed
- Expected goals against
- Clean sheets

### 5.5 Home/Away Features

Examples:

- Home team's home performance
- Away team's away performance
- Home win rate
- Away win rate

### 5.6 League / Standing Features

Examples:

- League position
- Points
- Goal difference
- Games played

### 5.7 Additional Features

Possible future features:

- Rest days
- Head-to-head performance
- Player availability
- Roster strength

### 5.8 Data Leakage Prevention

Document exactly how features are prevented from using the current match or
future matches.

For rolling statistics, historical values must be shifted so that match M_t
uses only matches before M_t.


## 6. Dataset Construction

### 6.1 Final Feature Dataset

Document the final columns used for training.

### 6.2 Train / Validation / Test Split

Explain the chronological split.

Past --------------------------------------------> Future

Training              Validation              Test

Explain why random splitting is inappropriate for this problem.

### 6.3 Feature Scaling / Encoding

Document:

- Numerical scaling
- Categorical encoding
- Missing-value handling
- Any model-specific preprocessing


## 7. Baseline Models

### 7.1 Outcome Baseline

Examples:

- Majority-class prediction
- Logistic Regression

### 7.2 Score Baseline

Examples:

- League-average goals
- Simple Poisson model

Explain that more complex models must outperform these baselines to justify
their additional complexity.


## 8. Approach A — Independent Models

### 8.1 Architecture

Pre-match Features
        ↓
   ┌────┴────┐
   ↓         ↓
Classifier  Goal Model
   ↓         ↓
H/D/A %    Score

### 8.2 Outcome Classification

Models to evaluate:

- Logistic Regression
- Random Forest
- Gradient Boosting / XGBoost

### 8.3 Goal Regression

Models to evaluate for:

- Home goals
- Away goals

### 8.4 Prediction Consistency

Explain that independently trained outcome and score models can produce
contradictory predictions.

Define a contradiction / consistency metric.


## 9. Approach B — Probabilistic Goal Model

### 9.1 Architecture

Pre-match Features
        ↓
Goal Distribution Model
        ↓
Home/Away Goal Distributions
        ↓
Score Probability Matrix
      ↙     ↘
 H/D/A %   Most Likely Score

### 9.2 Poisson Model

Document the initial Poisson formulation for home and away goals.

### 9.3 Score Probability Matrix

Explain how probabilities for possible scorelines are calculated.

### 9.4 Outcome Probabilities

Explain how score probabilities are aggregated into:

- P(Home Win)
- P(Draw)
- P(Away Win)

### 9.5 Possible Extensions

Examples:

- Dixon-Coles
- Correlated goal models


## 10. Approach C — Multi-Task Neural Network

### 10.1 Architecture

                    Pre-match Features
                           ↓
                     Shared Layers
                           ↓
                    ┌──────┴──────┐
                    ↓             ↓
              Outcome Head     Goal Head
                    ↓             ↓
                 H/D/A %      Home/Away
                                Goals

### 10.2 Input Features

Document the features supplied to the neural network.

### 10.3 Network Architecture

Document:

- Number of layers
- Hidden dimensions
- Activation functions
- Regularization
- Output heads

### 10.4 Multi-Task Loss

Document the classification and goal-prediction losses and how they are
combined.

### 10.5 Training

Document:

- Optimizer
- Learning rate
- Batch size
- Epochs
- Early stopping
- Random seed


## 11. Model Evaluation

### 11.1 Outcome Metrics

- Accuracy
- Macro F1
- Log Loss
- Brier Score / Calibration

### 11.2 Score Metrics

- Home Goal MAE
- Away Goal MAE
- RMSE
- Exact Score Accuracy

### 11.3 Consistency Metrics

For models that independently generate outcome and score predictions:

- Consistency rate
- Contradiction rate

### 11.4 Temporal Evaluation

Document chronological testing and any walk-forward validation procedure.


## 12. Model Comparison

Maintain the final experimental comparison here.

| Metric | Approach A | Approach B | Approach C |
|--------|------------|------------|------------|
| Accuracy | | | |
| Macro F1 | | | |
| Log Loss | | | |
| Brier Score | | | |
| Home Goal MAE | | | |
| Away Goal MAE | | | |
| Exact Score Accuracy | | | |
| Contradiction Rate | | 0% / N/A | |

Discuss the strengths and weaknesses observed for each approach.


## 13. Model Selection

Document:

- Selected production approach
- Selected model
- Hyperparameters
- Evaluation results
- Reason for selection
- Model/version identifier

Explain why the selected model is preferable to the alternatives.


## 14. Model Inference

### 14.1 Inference Interface

All production models should expose a common prediction interface.

Input:

Pre-match features

Output:

{
    "home_win_probability": ...,
    "draw_probability": ...,
    "away_win_probability": ...,
    "predicted_home_goals": ...,
    "predicted_away_goals": ...
}

### 14.2 Backend Integration

Describe how the backend interacts with the production inference system.

Backend
    ↓
Feature Generation
    ↓
Production Model
    ↓
Prediction
    ↓
Backend Response

The backend should not contain model-training logic.


## 15. Model Artifacts

Document:

- Model artifact format
- Preprocessing artifacts
- Model metadata
- Model version
- Feature definitions
- Storage location

Do not commit large model artifacts to Git unless intentionally supported by
the repository strategy.


## 16. Retraining Strategy

Describe the intended retraining workflow.

New Match Data
      ↓
ETL Update
      ↓
ML Dataset Update
      ↓
Candidate Model Training
      ↓
Evaluation
      ↓
Model Promotion

For Milestone 2, retraining may remain manually triggered.

Automatic scheduling, model registry, deployment, and monitoring can be
implemented during the MLOps milestone.


## 17. Testing

Document tests for:

- Feature calculations
- Leakage prevention
- Dataset construction
- Model input/output shapes
- Probability validation
- Inference
- Model serialization/loading

Important invariants include:

- Outcome probabilities sum to approximately 1.
- Predictions never use post-match information.
- Goal predictions cannot be negative.
- Training and inference use identical feature definitions.


## 18. Running the ML Pipeline

Document the final commands once implemented.

Example:

Train:

python -m src.ml.train

Evaluate:

python -m src.ml.evaluate

Predict:

python -m src.ml.predict


## 19. Future Improvements

Potential improvements after Milestone 2:

- Automated retraining
- MLflow experiment tracking
- Model registry
- Automated model promotion
- Data drift detection
- Model performance monitoring
- Cloud model storage
- CI/CD for ML
- Additional leagues
- Player availability / injury features
- More advanced probabilistic models