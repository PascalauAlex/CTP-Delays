import asyncio
import logging
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert

from .config import settings
from .database import SessionLocal
from .models import Route, VehiclePosition,Trips,Stops,StopTimes
from .tranzy import TranzyClient

log = logging.getLogger("poller")
CHUNK = 1000


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

async def pool_trips_once(client:TranzyClient) ->None:
    trips = await client.get_trips()
    rows = []
    for t in trips:

        rows.append(
            {
                "direction_id":t.get("direction_id"),
                "route_id":t.get("route_id"),
                "trip_id":t.get("trip_id"),
                "trip_headsign":t.get("trip_headsign"),
                "block_id":t.get("block_id"),
                "shape_id":t.get("shape_id"),
                "wheelchair_accessible":t.get("wheelchair_accessible"),
                "bikes_allowed":t.get("bikes_allowed")
            }
        )
    if not rows:
        log.warning("No usable trip in this poll ")
        return
    stmt = insert(Trips).values(rows)
    stmt =stmt.on_conflict_do_nothing()
    async with SessionLocal() as session:
        await session.execute(stmt)
        await session.commit()
    log.info("Inserted up to %d trips",len(rows))

async def pool_stops_once(client:TranzyClient) -> None:
    stops = await client.get_stops()
    rows = []
    for s in stops:
        rows.append({
            "stop_id":s.get("stop_id"),
            "stop_name":s.get("stop_name"),
            "stop_desc":s.get("stop_desc"),
            "stop_lat":s.get("stop_lat"),
            "stop_lon":s.get("stop_lon"),
            "location_type":s.get("location_type"),
            "stop_code":s.get("stop_code")
        })

    if not rows:
        log.warning("No usable stops in this pool")
        return
    stmt = insert(Stops).values(rows)
    stmt = stmt.on_conflict_do_nothing()
    async with SessionLocal() as session:
        await session.execute(stmt)
        await session.commit()
    log.info("Insert up to %d stops",len(rows))

async def pool_stop_times_once(client:TranzyClient) -> None:
    stop_times = await client.get_stop_times()
    rows = []
    for st in stop_times:
        rows.append({
            "trip_id":st.get("trip_id"),
            "arrival_time":st.get("arrival_time"),
            "departure_time":st.get("departure_time"),
            "stop_id":st.get("stop_id"),
            "stop_sequence":st.get("stop_sequence"),
            "stop_headsign":st.get("stop_headsign"),
            "pickup_type":st.get("pickup_type"),
            "drop_off_type":st.get("drop_off_type"),
            "shape_dist_traveled":st.get("shape_dist_traveled"),
            "timepoint":st.get("timepoint")
        })
    if not rows:
        log.warning("No usable stop times in this pool")
        return
    async with SessionLocal() as session:
        for i in range(0,len(rows),CHUNK):
            chunk = rows[i:i+CHUNK]
            stmt = insert(StopTimes).values(chunk).on_conflict_do_nothing(
                index_elements=['trip_id','stop_sequence']
            )
            await session.execute(stmt)
        await session.commit()


    log.info("Insert up to %d stop_times",len(stop_times))



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

