# Intra-Exchange Triangular Arbitrage System

This is a production-grade Python monorepo for a single-exchange triangular arbitrage system.

## Features

- Connects to a single exchange (Binance by default, extensible to others).
- Monitors three-pair triangles via WebSocket L2 order books.
- Detects and executes profitable arbitrage opportunities.
- Supports paper and live trading modes.
- Persists data to PostgreSQL and Redis.
- Exposes a FastAPI admin interface and Prometheus metrics.

## Quickstart

1.  **Set up environment variables:**

    ```bash
    cp .env.example .env
    ```

    Update `.env` with your exchange API keys if you are not using paper mode.

2.  **Build and run services:**

    ```bash
    docker-compose up -d --build
    ```

3.  **Run the application:**

    ```bash
    make run
    ```

5.  **Access the API:**

    The API is available at `http://localhost:8081/docs`.

## Development

- **Format code:** `make format`
- **Lint code:** `make lint`
- **Run tests:** `make test`
