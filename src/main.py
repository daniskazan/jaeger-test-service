import aiohttp
from fastapi import FastAPI, Request
import uvicorn
from loguru import logger
import logging

from api.v1.router import router as v1_router
from core.resolver import container, register_deps, stop_services
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


@app.get("/test")
async def tmp():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://google.com") as resp:
            return await resp.text()
@app.get('/excp')
async def excp(r: Request):
    return

if settings.JAEGER_ENABLED:
    setup_tracer(service_name="fastapi-app", app=app)
    logger.info("Instrumentation started successfully")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8001, log_level=logging.DEBUG, reload=True
    )
