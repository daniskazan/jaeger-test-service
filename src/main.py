import aiohttp
from aiocache import RedisCache
from fastapi import FastAPI, Request, Depends
import uvicorn
from loguru import logger
import logging

from api.v1.router import router as v1_router
from core.resolver import container, register_deps, stop_services, get_redis_client
from core.tracer import setup_tracer
from core.settings import settings
from core.middleware import LoggingMiddleware

app = FastAPI()
app.include_router(v1_router)

app.add_middleware(LoggingMiddleware)
@app.on_event("startup")
async def startup():
    await register_deps()
    logger.info("App started succefully")


@app.on_event("shutdown")
async def shutdown():
    await stop_services()
    logger.info(f"Gracefully shutdown all services {container.registrations.__dict__}")
    logger.info("Stopped the server")



if settings.JAEGER_ENABLED:
    setup_tracer(service_name="fastapi-app", app=app)
    logger.info("Instrumentation started successfully")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8001, log_level=logging.DEBUG, reload=True
    )
