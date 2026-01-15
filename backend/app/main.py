from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.dependencies import get_db
from app.routers import auth, hotels, room_types, rate_adjustments
from app.db.session import init_db
from app.seed import seed_admin_user


def create_app() -> FastAPI:
    app = FastAPI(title="Hotel Admin API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(hotels.router, prefix="/hotels", tags=["hotels"])
    app.include_router(room_types.router, tags=["room_types"])
    app.include_router(rate_adjustments.router, tags=["rate_adjustments"])

    @app.on_event("startup")
    async def startup_event():
        init_db()
        seed_admin_user()

    return app


app = create_app()
