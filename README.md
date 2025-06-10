# Football ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline using Apache Airflow to process football data. The pipeline extracts data from the Football API, stores it in MongoDB, transforms it by adding a calculated field, and uploads the results to an AWS S3 bucket.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Pipeline Steps](#pipeline-steps)
- [Environment Variables](#environment-variables)
- [Running the Pipeline](#running-the-pipeline)
- [Directory Structure](#directory-structure)
- [Dependencies](#dependencies)
- [Notes](#notes)

## Overview
The pipeline performs the following tasks daily:
1. **Extract**: Fetches top scorers and top assists data for the 2021 season (league ID 61) from the Football API and saves it as JSON files.
2. **Load**: Inserts the JSON data into a MongoDB database.
3. **Transform**: Adds a `contribution` field (sum of goals and assists) to the top scorers data in MongoDB.
4. **Upload**: Uploads the JSON files to an AWS S3 bucket.

## Prerequisites
- **Apache Airflow**: Installed and configured.
- **MongoDB**: Running locally on port 27017.
- **AWS Account**: With an S3 bucket named `footballstorages3`.
- **Python**: Version 3.8+.
- **API Key**: Access to the Football API via RapidAPI.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Airflow**:
   - Ensure Airflow is installed and the Airflow home directory (`AIRFLOW_HOME`) is set (default: `~/airflow`).
   - Place the DAG file (`football_etl_pipeline.py`) in the Airflow `dags` directory.

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root with the following variables:
   ```bash
   X_RAPIDAPI_HOST=v3.football.api-sports.io
   X_RAPIDAPI_KEY=<your-rapidapi-key>
   AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
   AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
   AWS_REGION=us-east-1
   ```

5. **Start MongoDB**:
   Ensure MongoDB is running locally:
   ```bash
   mongod
   ```

6. **Start Airflow**:
   Initialize the Airflow database and start the webserver and scheduler:
   ```bash
   airflow db init
   airflow webserver --port 8080
   airflow scheduler
   ```

## Pipeline Steps
1. **Extract Data** (`extract_api_data`):
   - Connects to the Football API to fetch top scorers and top assists data.
   - Saves the data as `top_scorers.json` and `top_assists.json` in `/tmp`.

2. **Load Data** (`load_json_to_mongodb`):
   - Reads JSON files and inserts them into the `my_collection` collection in the `football_db` MongoDB database.
   - Handles both list and dictionary JSON structures, replacing existing documents if necessary.

3. **Transform Data** (`transform_add_contribution`):
   - Retrieves the top scorers document from MongoDB.
   - Adds a `contribution` field (goals + assists) to each player's statistics.
   - Updates the document in MongoDB.

4. **Upload to S3** (`upload_to_s3`):
   - Uploads the JSON files to the `footballstorages3` S3 bucket.

## Environment Variables
The pipeline requires the following environment variables in a `.env` file:
- `X_RAPIDAPI_HOST`: Host for the Football API (e.g., `v3.football.api-sports.io`).
- `X_RAPIDAPI_KEY`: Your RapidAPI key for the Football API.
- `AWS_ACCESS_KEY_ID`: AWS access key for S3.
- `AWS_SECRET_ACCESS_KEY`: AWS secret key for S3.
- `AWS_REGION`: AWS region for S3 (default: `us-east-1`).

## Running the Pipeline
1. Access the Airflow web interface at `http://localhost:8080`.
2. Enable the `football_etl_pipeline` DAG.
3. Trigger the DAG manually or wait for the daily schedule (`@daily`).

## Directory Structure
```
<repository-directory>/
├── football_etl_pipeline.py  # Airflow DAG file
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Dependencies
Install the required Python packages:
```bash
pip install apache-airflow pymongo python-dotenv boto3
```

## Notes
- Ensure the `/tmp` directory is writable for JSON file storage.
- The MongoDB database (`football_db`) and collection (`my_collection`) are created automatically if they do not exist.
- The S3 bucket (`footballstorages3`) must be created in your AWS account before running the pipeline.
- The pipeline is set to run daily, starting from January 1, 2025, with no catch-up for missed runs (`catchup=False`).
- Handle API rate limits by checking your RapidAPI subscription plan.