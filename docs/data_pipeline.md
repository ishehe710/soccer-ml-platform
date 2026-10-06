# Data Pipeline

## Overview

The application uses two data pipelines: an initialization pipeline and an incremental update pipeline. Both pipelines follow the ETL framework for data engineering.

ETL stands for **Extract, Transform, and Load**. Extraction retrieves raw data from the Sports Bzzoiro Data API. Transformation selects the relevant data needed by the application and validates it to ensure it is ready to be stored in the database. Loading then inserts or upserts the transformed data into the PostgreSQL database.

The initialization pipeline is responsible for initially populating the database with the data required by the application. The incremental update pipeline updates existing records with new data as it becomes available.

## Architecture

```text
Sports Bzzoiro API
        |
        v
    Extraction
        |
        v
  Transformation
        |
        v
    PostgreSQL
```

## Initial Data Pipeline

The script responsible for the initial population of application data is `src/pipeline/run_initialization.py`.

This pipeline populates the database with the necessary data for the latest six seasons of professional soccer for the competitions covered by the application.

### Load Order

1. Competitions
2. Seasons
3. Teams
4. Matches
5. Match Stats
6. Players / Rosters
7. Player Season Stats
8. Standings

Players and rosters are extracted and processed together because the roster data is used to determine which players need to be retrieved.

## Incremental Update Pipeline

The script responsible for periodically updating database information is `src/pipeline/run_pipeline.py`.

This pipeline looks for records that need to be updated as the soccer season progresses. For example, match results, match statistics, player season statistics, and standings can change as matches are completed.

### Updated Data

- Matches
- Match stats
- Player season stats
- Standings

Teams, rosters, players, competitions, and seasons are not currently included in the incremental update pipeline because they are already populated and do not need to be updated as frequently during the season.

## Match Update Logic

When the incremental pipeline runs, it uses the current date as an inclusive cutoff to determine which matches are candidates for updates.

The database is queried for the API IDs of matches that meet the update criteria. These IDs are then passed to the match update functions in `src/pipeline/run_pipeline.py`.

The pipeline uses these IDs to retrieve the latest match information from the Sports Bzzoiro Data API. The updated data is transformed and then upserted into PostgreSQL. The same match IDs can also be used to retrieve updated match statistics.

This prevents the pipeline from unnecessarily requesting every match in the database during each execution.

## Idempotency

The database uses a combination of SQL `UNIQUE` constraints and `UPSERT` operations to make the pipeline idempotent.

This allows existing records to be updated without creating duplicate records. As a result, the incremental pipeline can be executed repeatedly without duplicating previously loaded data.

## Error Handling

API requests use a Python `Session` configured with a retry strategy for temporary API failures. This helps prevent transient request failures from immediately terminating the pipeline.

The incremental pipeline in `src/pipeline/run_pipeline.py` also contains top-level exception handling. If an unrecoverable error occurs during one of the ETL stages, the error is logged and propagated rather than allowing the pipeline to silently report a successful execution.

## Logging

The application uses Python's built-in `logging` module. Logging configuration is stored in `src/config/logger.py`, which provides the logging configuration used throughout the application.

The pipeline logs important stages of ETL execution, including API extraction progress, transformation operations, the number of records being loaded, and pipeline completion or failure.

These logs make it easier to monitor pipeline executions and diagnose failures, especially when the pipeline is automated in the future.

## Running the Pipeline

The initialization pipeline can be run with:

```bash
python src/pipeline/run_initialization.py
```

The incremental update pipeline can be run with:

```bash
python src/pipeline/run_pipeline.py
```

## Automation

The incremental pipeline is currently executed manually. A future step is to use GitHub Actions to schedule executions of `run_pipeline.py` so that the database can automatically update as new matches are completed and new data becomes available.

## Testing

The following tests have been performed on the data pipeline:

- Successful initialization of the PostgreSQL database
- Repeated execution of the incremental pipeline
- Verification that repeated executions do not create duplicate records
- Verification that real-world data changes are reflected in PostgreSQL
- Successful execution with application logging enabled

A final live-match validation will be performed when new Premier League or Champions League matches are available. This will verify the complete update flow as a match progresses from its existing fixture state to a completed match with updated statistics.