# Shipment Tracking

## Description

This is a simple shipment tracking API that allows users to track their shipments. The application is built using the
following technologies:
Python, Django, Django Rest Framework, SQLite, and Redis.

### How to import data

1. Run the following command to import the data into the database:

```commandline
python3 .\manage.py import_data seed_data.csv
```

### How to run the application

Run the following command to start the application:

```commandline
docker compose up --build -d
```

### How to run the tests

Run the following command to run the tests:

```commandline
docker compose -f docker-compose.test.yml up  --abort-on-container-exit
```