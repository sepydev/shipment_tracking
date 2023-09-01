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

----


## Discussion Points:

- What were the important design choices and trade-offs you made?
- What would be required to deploy this application to production?
- What would be required to scale this application to handle 1000 requests per second?

### Design Choices and Trade-offs

Choosing Django as the framework for this project was a wise decision. The development time was significantly reduced thanks to the use of the Django Rest Framework and related third-party packages. The Django Rest Framework offers a wealth of useful built-in features, including authentication, serialization, and more. It also provides robust testing tools that were essential for this project.

For the database, I use SQLite during development and testing, but it's not suitable for production use. In a production environment, I would opt for PostgreSQL, MySQL, or NoSQL.

The project follows the MVT (MVC) architecture, with the Django Rest Framework serving as the controller and model layers, as required by the framework. Although I generally prefer Clean Architecture for larger projects, time constraints required this approach for this particular project.

Redis is the caching solution for this project. Its speed and ease of use make it a good choice, especially when considering scalability.

Comprehensive testing covers all aspects of the project. Unit testing is used to evaluate both the models and the API.

### Deployment

For deployment, I relied on Docker and Docker Compose. I also used Nginx as a load balancer. It's worth considering using Gunicorn or even Unicorn instead of Python to run the project. These options offer better support for asynchronous handling, which is crucial for scaling. Using Django ORM's async functionality in such cases can significantly improve performance.

### Scaling

In order to prepare the project for 1000 requests per second, several strategies can be in place:

1. Switch from SQLite to PostgreSQL: Use PostgreSQL as the database and create indexes on the `tracking_number` and `carrier` fields. Additionally, consider extracting city and country information from the address to reduce query execution times.

2. Gunicorn or Unicorn: Switch to using Gunicorn or Unicorn instead of Python to run the project. This transition can be coupled with refactoring the project to take full advantage of Django ORM's async capabilities.

3. Load Balancer: Employ a load balancer like Nginx to distribute incoming requests efficiently.

4. Caching: Integrate Redis to cache data and minimize database queries, which can significantly enhance response times.

5. Serialization: Consider using Pydantic for serialization instead of Django Rest Framework, as Pydantic is known for its faster performance.

6. Framework Alternatives: Explore alternatives to the Django Rest Framework, such as FastAPI or Sanic, as they are known for their superior speed compared to the Django Rest Framework.

