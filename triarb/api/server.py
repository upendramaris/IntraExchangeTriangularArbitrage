from fastapi import FastAPI
from prometheus_client import make_asgi_app

from . import routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Triangular Arbitrage Bot",
        description="An API for monitoring and controlling the tri-arb bot.",
        version="0.1.0",
    )

    # Add prometheus asgi middleware to route /metrics requests
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    app.include_router(routes.router)

    return app
