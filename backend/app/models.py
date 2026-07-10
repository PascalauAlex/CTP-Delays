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