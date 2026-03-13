from __future__ import annotations

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger


def init_sentry() -> None:
    if not settings.SENTRY_DSN:
        return
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.SENTRY_ENVIRONMENT or settings.APP_ENV,
            traces_sample_rate=float(settings.SENTRY_TRACES_SAMPLE_RATE),
            profiles_sample_rate=float(settings.SENTRY_PROFILES_SAMPLE_RATE),
            integrations=[FastApiIntegration(), SqlalchemyIntegration()],
            send_default_pii=False,
        )
        logger.info("Sentry telemetry enabled")
    except Exception as exc:
        logger.warning("Sentry initialization skipped: %s", str(exc))


def init_opentelemetry(app: FastAPI) -> None:
    if not settings.OTEL_ENABLED:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

        resource = Resource.create({SERVICE_NAME: settings.OTEL_SERVICE_NAME})
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)

        if settings.OTEL_EXPORTER_OTLP_ENDPOINT:
            exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
        else:
            exporter = ConsoleSpanExporter()

        provider.add_span_processor(BatchSpanProcessor(exporter))

        FastAPIInstrumentor.instrument_app(app)
        HTTPXClientInstrumentor().instrument()
        try:
            from app.db.postgres import engine

            SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)
        except Exception:
            pass
        logger.info("OpenTelemetry tracing enabled")
    except Exception as exc:
        logger.warning("OpenTelemetry initialization skipped: %s", str(exc))


def init_telemetry(app: FastAPI) -> None:
    init_sentry()
    init_opentelemetry(app)
