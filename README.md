# FastAPI Cryptocurrency Price API

This is a FastAPI-based application that provides real-time cryptocurrency prices from multiple exchanges, including Binance and Kraken. The application features a WebSocket for real-time price updates and a RESTful API for querying current prices.

## Features

- Provides real-time cryptocurrency prices from Binance and Kraken.
- Supports WebSocket connections for live price updates.
- Allows filtering by currency pair and exchange.
- Returns prices in the Binance format, even for Kraken pairs.
- Deployed using Docker.


## Getting Started

### 1. Clone the repository

First, clone this repository to your local machine:

```bash
git clone
```

### 2. Build the Docker image

```bash
docker build -t my-fastapi-app .
```

### 3. Run the Docker container

```bash
docker run -d -p 8000:8000 my-fastapi-app
```

### 4. Access the Application

http://localhost:8000


## Project Structure

- app/: Contains the backend code for the FastAPI application.

- frontend/: Contains the frontend files (HTML, CSS, JavaScript).

- Dockerfile: Docker configuration for building the image.

- requirements.txt: Python dependencies for the project.