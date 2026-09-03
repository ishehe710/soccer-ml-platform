# Data Pipeline

## Overview

The data pipeline retrieves soccer data from the Bzzoiro Sports Data API, validates and transforms the data, and stores it in a PostgreSQL database.

The pipeline is designed as a modular ETL process consisting of three primary stages:

1. **Extraction** — retrieve raw data from the Bzzoiro Sports Data API.
2. **Transformation** — validate and map the raw API data into application models using Pydantic.
3. **Loading** — insert or update the transformed data in PostgreSQL.

The pipeline is implemented in `./src/pipeline/`.

## Data Flow

```text
Bzzoiro Sports API
        |
        v
    Extraction
    extract.py
        |
        v
  Validation /
  Transformation
  transform.py
        |
        v
      Loading
       load.py
        |
        v
    PostgreSQL
        |
        v
ML / Backend / Frontend
```

The pipeline separates data extraction, transformation, and loading so that each stage can be tested and maintained independently.

## Data Sources

### Bzzoiro Sports Data API

The primary data source for the project is the Bzzoiro Sports Data API.

The API provides soccer data used throughout the application, including competitions, seasons, teams, matches, match statistics, players, and player season statistics.

**Provider:** Bzzoiro Sports Data

**API documentation:** https://sports.bzzoiro.com/docs/conventions/

**Authentication:** API requests require an authentication token supplied through the project's environment configuration.

**Primary data used by the project:**

* Competitions
* Seasons
* Teams
* Matches
* Match statistics
* Players
* Player season statistics
* Standings

The project initially focuses on the **Premier League** and **UEFA Champions League**. In the future more competitions will be covered.

API rate limits and authentication requirements are considered when designing the ingestion process.

## Extraction

The extraction stage retrieves raw data from the Bzzoiro Sports Data API.

Extraction is handled by:

```text
./src/pipeline/extract.py
```

The extraction layer is responsible for:

* Building API request URLs
* Supplying API authentication
* Sending requests to the Bzzoiro Sports Data API
* Retrieving raw API responses
* Returning the raw data to the transformation stage

The extraction layer does **not** perform database operations or application-level data modeling.

The types of data extracted by the pipeline include:

* Competitions
* Seasons
* Teams
* Matches
* Match statistics
* Players
* Player season statistics
* Standings

The database schema used to store this data is documented in the [Database Design Documentation](./database_design.md).

## Transformation

The transformation stage takes the raw API responses and converts them into validated application models.

Transformation is handled by:

```text
./src/pipeline/transform.py
```

Pydantic models are used to validate the structure and types of the data before it is passed to the loading stage.

The transformation process is responsible for:

* Mapping API fields to database/application fields
* Validating incoming data
* Converting data into the appropriate types
* Creating application models for the loading stage

The transformation layer does not directly interact with PostgreSQL.

Application models are stored in:

```text
./src/models/
```

## Loading

The loading stage stores transformed data in the PostgreSQL database.

Loading is handled by:

```text
./src/pipeline/load.py
```

The loading process is responsible for:

* Connecting to PostgreSQL
* Inserting transformed records
* Updating existing records when appropriate
* Preventing duplicate records
* Maintaining relationships between database tables

Database connection configuration is managed through the project's environment configuration.

The database uses the PostgreSQL schema documented in the [Database Design Documentation](./database_design.md).

## Pipeline Orchestration

The individual extraction, transformation, and loading stages are coordinated by:

```text
./src/pipeline/run_pipeline.py
```

The pipeline follows the general pattern:

```text
Extract
   |
   v
Transform
   |
   v
Load
```

For each type of data, the pipeline executes the corresponding extraction, transformation, and loading functions.

The pipeline is being implemented incrementally, beginning with competitions and expanding to the remaining database entities.

## Update Strategy

The pipeline must support both historical data ingestion and ongoing updates.

Historical data is initially loaded into PostgreSQL to provide the data required for analytics and machine learning.

For current competitions, the pipeline will periodically retrieve updated match information and update the database as matches are played.

The intended update process is:

```text
Upcoming Matches
       |
       v
Periodic API Update
       |
       v
PostgreSQL
       |
       v
Match Completed
       |
       v
Update Match Data
       |
       v
Update Statistics / Standings
```

The pipeline should use database upserts where appropriate so that running the pipeline multiple times does not create duplicate records.

## Error Handling

The pipeline must account for errors that can occur during extraction, transformation, and loading.

Potential errors include:

* API request failures
* Authentication failures
* API rate limiting
* Missing or incomplete API data
* Invalid data types or values
* Pydantic validation errors
* Database connection failures
* Database constraint violations
* Duplicate records

Errors should be handled at the appropriate pipeline stage so that invalid data is not inserted into the database.

## Testing

Pipeline and application tests are located in:

```text
./tests/
```

Testing will cover individual pipeline stages as well as the interaction between stages.

Examples include:

* Testing API extraction
* Testing data transformation
* Testing Pydantic validation
* Testing database loading
* Testing duplicate/upsert behavior
* Testing database relationships
* Testing the complete pipeline

## Future Improvements

Potential improvements to the data pipeline include:

* Scheduled ingestion
* Automated database updates
* Improved error logging
* Pipeline monitoring
* Retry mechanisms for failed API requests
* More leagues and competitions
* More comprehensive data validation
* Incremental data ingestion
* Automated pipeline execution through CI/CD
