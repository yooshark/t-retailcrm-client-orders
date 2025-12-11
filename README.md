# RetailCRM-client-orders application

---

## Overview

This project provides a FastAPI-based service that integrates with RetailCRM API v5 to manage customers, orders, and
payments. It exposes REST endpoints for retrieving and filtering customers, creating customers and orders, and attaching
payments to existing orders.

The application uses asynchronous HTTP requests via httpx, clean dependency injection with aioinject, and
environment-based configuration.
It is fully containerized with Docker and docker-compose, allowing quick setup and easy local development. Swagger
documentation is available in development mode.

---

## Technologies

- FastAPI
- httpx
- aioinject
- Uvicorn
- Docker & docker-compose

---

## Configuration

Configuration is stored in `.env`, for examples see `.env.example`


## Run server locally:
### Install requirements:

```bash
pip install -r requirements.txt
```

```bash
python run.py
```

## Docker
Then run the following command in the same directory as the `docker-compose.yml` file to start the container.
`docker compose up -d`
