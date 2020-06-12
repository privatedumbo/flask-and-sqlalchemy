# Smart Steel Technologies GmbH Challenge

Functional example for a process to upload data into a relational database and serve it from a Flask app.

I didn't found a straightforward way of using a `SQLAlchemy` model from a Flask API while keeping the advantages of using `flask-sqlalchemy` to query that model.

Here is what I found out after some reading and trying.

## System requirements to run the example

- Docker compose (for the db)
- Python>=3.6 

## Setting up the environment

1. Create a virtual environment with python>=3.6

2. Start the database container by running

    > ./commands/run.sh

3. Install requirements

    > pip install -r requirements.txt

## Common observations

- The example configuration is defined in the `src.core.config.ini` file. The configuration for both parts (loading the database and serving the data) is defined in one file because, although the application was designed to work as decoupled as possible, having different config files is, in my opinion, error prone.

## Loading the database

### Notes

- Database data is never dropped on initialization. If the loading script is run more than once with the same data, it will exit with the corresponding exception.

### Running the script

    > python runner.py batch

## Serving loaded data

### Starting the web server

    > python runner.py server

### Endpoints

> /temperature/

> /temperature/:id

### Status Codes

| Status Code   | Description           
| ------------- |------------- |
| 200      | Existing temperature measurement retrieved successfully |
| 404      | Unable to found requested temperature measurement |

## Contact Info

Issues are welcome :) , both for questions and improvement suggestions.
