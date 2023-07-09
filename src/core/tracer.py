from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

from core.settings import settings


def setup_tracer(service_name: str, app: FastAPI):
    sampler = TraceIdRatioBased(1 / 20)
    trace_provider = TracerProvider(resource=Resource(attributes={SERVICE_NAME: service_name}), sampler=sampler)
    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.JAEGER_HOST, agent_port=settings.JAEGER_PORT, udp_split_oversized_batches=True
    )

    trace_provider.add_span_processor(span_processor=BatchSpanProcessor(jaeger_exporter))
    trace_provider.add_span_processor(span_processor=BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(trace_provider)

    FastAPIInstrumentor.instrument_app(app, excluded_urls="/openapi.json,/docs")

    SQLAlchemyInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    RedisInstrumentor().instrument()


    return trace_provider
