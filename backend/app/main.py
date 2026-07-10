import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base, engine, get_db
from .models import Route, VehiclePosition
from .poller import polling_loop
from .schemas import RouteOut, VehicleOut

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # creează tabelele dacă nu există (MVP; vezi nota despre Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    stop_event = asyncio.Event()
    task = asyncio.create_task(polling_loop(stop_event))
    yield
    stop_event.set()
    await task


app = FastAPI(title="CTP Delays API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/routes", response_model=list[RouteOut])
async def list_routes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Route).order_by(Route.route_short_name))
    return result.scalars().all()


@app.get("/api/vehicles", response_model=list[VehicleOut])
async def latest_vehicles(
    route_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=5)

    query = (
        select(VehiclePosition)
        .where(VehiclePosition.timestamp >= cutoff)
        .distinct(VehiclePosition.vehicle_id)
        .order_by(
            VehiclePosition.vehicle_id,
            VehiclePosition.timestamp.desc(),
        )
    )
    if route_id is not None:
        query = query.where(VehiclePosition.route_id == route_id)

    result = await db.execute(query)
    return result.scalars().all()





@app.get("/health")
async def health():
    return {"status": "ok"}