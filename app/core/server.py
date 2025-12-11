import contextlib
import logging
from collections.abc import AsyncIterator

import fastapi
from core import di
from core import settings

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi.middleware.cors import CORSMiddleware

from adapters.api.router import api_router

logger = logging.getLogger('app')


@contextlib.asynccontextmanager
async def lifespan(_: fastapi.FastAPI) -> AsyncIterator[None]:
    logger.info('Application is starting')
    yield
    logger.info('Application has stopped')


def new_server(
        app_cfg: settings.AppSettings,
) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        debug=app_cfg.DEBUG,
        title=f'Swagger: App - {app_cfg.ENVIRONMENT}',
        docs_url='/api/docs' if app_cfg.DEBUG else None,
        version=app_cfg.VERSION,
        lifespan=lifespan,
    )

    app.add_middleware(AioInjectMiddleware, container=di.container)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_cfg.ALLOW_ORIGINS,
        allow_origin_regex=app_cfg.ALLOW_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(api_router)

    return app
