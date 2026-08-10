# Soccer ML Platform

A full-stack soccer analytics and machine learning platform that
provides current soccer statistics, interactive visualizations,
and ML-powered match predictions.

---

## Features

- Real-world soccer data
- League, team, and player statistics
- Match predictions
- Interactive visualizations

---

## Architecture

-   ```
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

## Tech Stack

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

## Project Status

Currently in development...

---

## Roadmap

- [x] Project planning
- [ ] Data pipeline
- [ ] ML models
- [ ] Backend
- [ ] Frontend
- [ ] Deployment

---

## Links

- Link to project spec: [Project Spec](./docs/project_specification.md)

---