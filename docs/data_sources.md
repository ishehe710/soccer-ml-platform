# Data Sources

I will go over the decision of which APIs to use as data sources for the website. 

---

## Criteria

First they must have data for the appropriate competitions for the current season, or must have historical data of them for training the models.

The data must consist of match data, team data, player data and league data.

---

## API Comparison Table

| API           | Premier League  | Champions League | Historical Data | Player Data | Match Stats | Team Data | Free Plan | Standings | Considered| Decision|
|:------------- | :------------:  | :------------:   | :------------:  | :---------: | :---------: | :-------: | :-------: | :-------: | :---:| :----- |
| The Stats API  | ✅             |  ✅              | ✅             | ✅          | ✅          | ✅       | ❌   |  ✅ |  ❌ | Greate Data but not free |
| RapidAPI       | ✅              | ❌              | ✅              | ✅         | ✅           | ✅      | ✅   | ✅ | ✅ | Missing Champions League data, but good source|
| API Football   | ✅              |✅               | ✅              | ✅          |  ✅        | ✅       | ✅   | ✅ | ✅ | Has it all, but limited free tier |
| The Sports DB  | ✅             | ❌               | ✅              | ✅          | ✅         | ✅       | ✅   | ✅ | ❌ | Too limited, difficult to use| 
| **Bzzoiro Sports** | ✅              | ✅             | ✅               | ✅           | ✅        | ✅        | ✅  | ✅ | ✅ | Has it all, first choice site |

---

## Decision

In the end I will using the Bzzoiro Sports API. It fits all the required data points and it is a free API with unlimited usage.

Link: [Sports Bzzoiro API](https://sports.bzzoiro.com/)

---