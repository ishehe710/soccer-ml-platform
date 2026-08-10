# Soccer ML Platform

## 1. Project Overview

This a personal project where I make a fullstack website that gives users the most up-to-date soccer data, statistics, and match predictions for games. 

---

## 2. Problem Statement

The website will be able to show the stats on leagues, teams, and players on the current season. This will be done on the Premier League and the Champions League to validate a working sysetm, which then can be scaled to more leagues in the future. 

This will be done by using real data from popular APIs and store that data into the a database. In addition to data and statistics, I will be providing match prediction models for upcoming games as well. 

---

## 3. Goals

The goals of the project is as follows:
- Build a robust data pipeline that takes real world data and stores it in a database that then can be used for other aspect of the application: player stats, match prediction, etc.

- Training machine learing models to predict match outcomes and being able to deploy it as a service.

- Create an API that will be able to take data from database and serve it to frontend and models. In addition, update the database with new match data to keep the website up to date.

- Design a user-friendly frontend that is visually appealing and easy to use.

- Delpoy the website for fellow soccer fans to use. 

---

## 4. MVP

There are three main selling points of the website: **Soccer Data**, **Prediction Models** **Vizualizations**.
- **Soccer Data**: The website will feature data from matches of the current season, teams, players, leagues, and end-of-game statistics. 

- **Prediction Models**: The site wil also feature upcoming match predictions. This will include the score prediction of the game and the percentage for each outcome: % of home team winning, % of draw, and % of away team win.

- **Vizualization**: The site will also provide some vizualizations of the soccer data. For leagues it will have custom league table, with top scorers and assisters as well. For teams it will display all the match record for the season, as well as stats of top performers. Lastly, for players it show a table of their individual stats.

    ```
                  SOCCER ML PLATFORM
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     SOCCER DATA         ML         VISUALIZATIONS
          │              │              │
       Matches       Predictions     Dashboards
       Teams         Win Prob.       Tables
       Players       Score           Charts
       Leagues       xG              Trends
    ```

---

## 5. ML Objective

The machine learning focus of the project are the prediction models. The predictions wll be like this: 
    ```
        Home team win: x%
        Draw: y%
        Away team win: z%
        Predicted score: a - b
    ```
The model will give the predicted final score with the percentage of each possible outcome.

The models will trained on historic data first, so that the models are not trying to cheat by data leakage. Then when a matchday of games pass, the application will automatically train the model periodically with new data.

The model will use only information available prior to the match when generating predictions.

---

## 6. Technology Stack

The following project will likely use the following stack:
- Frotend: React
- Styling: Tailwind CSS
- Backend: FastAPI
- ML: scikit-learn + Pytorch
- Database: Postgres
- Cloud: AWS
- Version Control: Git + GitHub
- CI/CD: GitHub Actions
- Containers: Docker

---

## 7. System Architecture

The sytem architecture is shown below:
    
    ```
                         ┌───────────────┐
                         │   Soccer API  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Python ETL    │
                         │ Data Pipeline │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │  PostgreSQL   │
                         └───────┬───────┘
                                 │
                   ┌─────────────┴─────────────┐
                   │                           │
                   ▼                           ▼
          ┌────────────────┐          ┌────────────────┐
          │   Analytics    │          │ ML Pipeline    │
          └────────────────┘          └───────┬────────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │  ML Model     │
                                      └───────┬───────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │    FastAPI    │
                                      └───────┬───────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │ React.js Web  │
                                      │ Application   │
                                      └───────┬───────┘
                                              │
                                              ▼
                                           AWS
    ```
---

## 8. Data Sources

Yet to be determined

---

## 9. Milestones

There are five milstones:
- Milestone 1 (Data Engineering): This wil be fetch data from public APIs and storing that data neatly into a Postgres database. Where that data can then be used anywhere within the application. In addition, update the database with new data after future games have gone to a close.

- Milestone 2 (Machine Learning): Developing machine learing models to predict match outcome.

- Milestone 3 (Backend): Creating an API to communicate with the database to send data to frontend. 

- Milestone 4 (Frontend): Desigining a wesbite that allows users to see the match stats, current league rankings, and team/player performances with dashboards. In addition, to displaying match predictions.

- Milestone 5 (Delpoyment): Deploy the platform to AWS using Docker and GitHub Actions, with automated CI/CD, production configuration, and basic monitoring.

---

## 10. Future Features

Below I list the future features to be added to the website:
- Model performance
- Predicted goal scorers
- Include data on the the following leagues: Ligue 1, Bundesliga, Serie A, and La Liga
- Custom lineup graphics
- Injury and  team updates
- League finish predictions 
- Expected goals (xG) analytics
- Historical season comparisons
- Head-to-head analysis
- Have a user system, where they can tailor stats, teams, and players to follow.

---