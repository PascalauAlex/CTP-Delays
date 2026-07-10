import asyncio
import logging
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert

from .config import settings
from .database import SessionLocal
from .models import Route, VehiclePosition
from .tranzy import TranzyClient

log = logging.getLogger("poller")


def _parse_ts(value: str | int | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):  # epoch seconds
        return datetime.fromtimestamp(value, tz=None)
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


async def sync_routes(client: TranzyClient) -> None:
    routes = await client.get_routes()
    if not routes:
        return
    rows = [
        {
            "route_id": r["route_id"],
            "route_short_name": str(r.get("route_short_name", "")),
            "route_long_name": r.get("route_long_name") or "",
            "route_type": r.get("route_type"),
            "route_color": r.get("route_color"),
        }
        for r in routes
    ]
    stmt = insert(Route).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=[Route.route_id],
        set_={
            "route_short_name": stmt.excluded.route_short_name,
            "route_long_name": stmt.excluded.route_long_name,
            "route_type": stmt.excluded.route_type,
            "route_color": stmt.excluded.route_color,
        },
    )
    async with SessionLocal() as session:
        await session.execute(stmt)
        await session.commit()
    log.info("Synced %d routes", len(rows))


async def poll_vehicles_once(client: TranzyClient) -> None:
    vehicles = await client.get_vehicles()
    rows = []
    for v in vehicles:
        ts = _parse_ts(v.get("timestamp"))
        lat, lon = v.get("latitude"), v.get("longitude")
        if ts is None or lat is None or lon is None:
            continue
        rows.append(
            {
                "vehicle_id": str(v.get("id")),
                "label": v.get("label"),
                "route_id": v.get("route_id"),
                "trip_id": v.get("trip_id"),
                "latitude": lat,
                "longitude": lon,
                "speed": v.get("speed"),
                "timestamp": ts,
            }
        )
    if not rows:
        log.warning("No usable vehicle positions in this poll")
        return

    stmt = insert(VehiclePosition).values(rows)
    stmt = stmt.on_conflict_do_nothing(constraint="uq_vehicle_ts")
    async with SessionLocal() as session:
        await session.execute(stmt)
        await session.commit()
    log.info("Inserted up to %d positions", len(rows))


async def polling_loop(stop_event: asyncio.Event) -> None:
    client = TranzyClient()
    try:
        try:
            await sync_routes(client)
        except Exception:
            log.exception("Initial route sync failed")

        while not stop_event.is_set():
            try:
                await poll_vehicles_once(client)
            except Exception:
                log.exception("Vehicle poll failed; will retry next cycle")

            try:
                await asyncio.wait_for(
                    stop_event.wait(),
                    timeout=settings.poll_interval_seconds,
                )
            except asyncio.TimeoutError:
                pass  # a expirat intervalul → următorul ciclu
    finally:
        await client.aclose()