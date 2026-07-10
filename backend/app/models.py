from datetime import datetime

from sqlalchemy import DateTime, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[int] = mapped_column(primary_key=True)  # ID-ul Tranzy
    route_short_name: Mapped[str] = mapped_column(String(16))       # "25", "43B"
    route_long_name: Mapped[str] = mapped_column(String(255), default="")
    route_type: Mapped[int | None]        # GTFS: 0=tramvai, 3=autobuz, 11=troleu
    route_color: Mapped[str | None] = mapped_column(String(16))


class VehiclePosition(Base):
    __tablename__ = "vehicle_positions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vehicle_id: Mapped[str] = mapped_column(String(32), index=True)
    label: Mapped[str | None] = mapped_column(String(32))
    route_id: Mapped[int | None] = mapped_column(index=True)
    trip_id: Mapped[str | None] = mapped_column(String(64))
    latitude: Mapped[float]
    longitude: Mapped[float]
    speed: Mapped[float | None]
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("vehicle_id", "timestamp", name="uq_vehicle_ts"),
        Index("ix_positions_route_time", "route_id", "timestamp"),
    )


class Trips(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction_id : Mapped[int | None]
    route_id : Mapped[int | None]
    trip_id : Mapped[str] = mapped_column(String(255),unique=True)
    trip_headsign : Mapped[str | None] = mapped_column(String(255))
    block_id : Mapped[int | None]
    shape_id : Mapped[str | None] = mapped_column(String(255))
    wheelchair_accessible : Mapped[int | None]
    bikes_allowed : Mapped[int | None]

class Stops(Base):
    __tablename__ = "stops"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stop_id : Mapped[int] = mapped_column(unique=True)
    stop_name : Mapped[str] = mapped_column(String(255))
    stop_desc : Mapped[str | None] = mapped_column(String(255))
    stop_lat : Mapped[float]
    stop_lon : Mapped[float]
    location_type : Mapped[int | None]
    stop_code : Mapped[str | None] = mapped_column(String(255))

    def __str__(self):
        return "Stop"

class StopTimes(Base):
    __tablename__ = "stop_times"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_id : Mapped[str] = mapped_column(String(255), index=True)
    arrival_time : Mapped[str | None] = mapped_column(String(255))
    departure_time : Mapped[str | None] = mapped_column(String(255))
    stop_id : Mapped[int]
    stop_sequence : Mapped[int]
    stop_headsign : Mapped[str | None] = mapped_column(String(255))
    pickup_type : Mapped[int | None]
    drop_off_type : Mapped[int | None]
    shape_dist_traveled : Mapped[float | None]
    timepoint : Mapped[int | None]

    __table_args__ = (
        UniqueConstraint("trip_id", "stop_sequence", name="uq_trip_stp_seq"),
    )















