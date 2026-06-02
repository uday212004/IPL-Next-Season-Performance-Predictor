# IPL-Next-Season-Performance-Predictor
IPL Next Season Performance Predictor is a Machine Learning-powered sports analytics dashboard that predicts whether an IPL player is likely to become a high performer in the next season using historical batting and bowling statistics.

#  IPL Next Season Performance Predictor

An end-to-end Machine Learning project that predicts whether an IPL player is likely to become a **High Performer in the Next Season** using historical IPL batting and bowling statistics.

---

##  Project Overview

This project leverages IPL player performance data from multiple seasons to build a predictive analytics system capable of forecasting future player success.

The application analyzes player statistics such as:

- Runs
- Balls Faced
- Batting Average
- Strike Rate
- Economy Rate
- Wickets Per Match
- Matches Played
- Runs Per Match
- Balls Per Match
- Batting Impact

and predicts whether a player is likely to perform at a high level in the upcoming IPL season.

---

##  Problem Statement

IPL franchises invest heavily in player auctions and team selection.

The objective of this project is to use historical player performance data to identify players who are most likely to become high performers in the next season.

This can help teams, analysts, and cricket enthusiasts make data-driven decisions.

---

##  Dataset

The dataset contains IPL player statistics collected across multiple seasons.

### Features

| Feature | Description |
|----------|-------------|
| Runs | Total Runs Scored |
| Balls | Total Balls Faced |
| Batting_Avg | Batting Average |
| Strike_Rate | Batting Strike Rate |
| Economy | Bowling Economy |
| Wickets_Per_Match | Average Wickets Per Match |
| Matches | Total Matches Played |
| Runs_Per_Match | Engineered Feature |
| Balls_Per_Match | Engineered Feature |
| Batting_Impact | Engineered Feature |

### Target Variable

**High_Performer_Next_Season**

- 1 = Player scores 300+ runs in next season
- 0 = Player scores less than 300 runs in next season

---

##  Feature Engineering

The following features were engineered to improve predictive performance:

### Runs Per Match

Runs / Matches

### Balls Per Match

Balls / Matches

### Batting Impact

(Batting Average × Strike Rate) / 100

---

##  Machine Learning Model

### Algorithm Used

- Logistic Regression

### Train-Test Split

- 80% Training Data
- 20% Testing Data

### Evaluation Metrics

| Metric | Score |
|----------|----------|
| Accuracy | 85% |
| Precision | 59% |
| Recall | 55% |
| F1 Score | 57% |

---

##  Project Features

### Player Performance Prediction

Select any IPL player and predict future performance.

### Confidence Score

Displays prediction confidence percentage.

### Interactive Dashboard

Built using Streamlit.

### Top 10 Predicted Players Leaderboard

Ranks players most likely to perform well next season.

### Player Analytics

Displays latest season statistics and engineered metrics.

---

##  Streamlit Dashboard

Features:

- Player Selection Dropdown
- Latest Season Statistics
- High Performer Prediction
- Confidence Score
- Model Performance Metrics
- Top 10 Future Performers Leaderboard

---

##  Tech Stack

### Programming Language

- Python

### Libraries

- Pandas
- NumPy
- Scikit-Learn
- Joblib
- Streamlit

### Machine Learning

- Logistic Regression

### Deployment

- Streamlit
- Hugging Face Spaces

---

##  Project Structure

```text
IPL-Next-Season-Performance-Predictor/
│
├── app.py
├── player_stats.csv
├── ipl_next_season_predictor.pkl
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── Player_names.json
```

##  Run Locally

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/IPL-Next-Season-Performance-Predictor.git
```

### Move into Project Folder

```bash
cd IPL-Next-Season-Performance-Predictor
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Launch Streamlit App

```bash
streamlit run app.py
```

---

##  Future Improvements

- Player Comparison Dashboard
- Advanced Feature Engineering
- Random Forest & XGBoost Models
- SHAP Explainability
- Interactive Visualizations
- IPL Team Recommendation System
- Auction Value Prediction

---

##  Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Machine Learning
- Model Evaluation
- Sports Analytics
- Streamlit Development
- Model Deployment
- Git & GitHub

---

##  Author

**Uday Deshmukh**

linkedIN : https://www.linkedin.com/in/deshmukh-ud/

Aspiring Data Scientist | Machine Learning Enthusiast | Sports Analytics Explorer

---

##  If you found this project useful, consider giving it a star!
