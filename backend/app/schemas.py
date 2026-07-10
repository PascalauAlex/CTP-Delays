from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RouteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    route_id: int
    route_short_name: str
    route_long_name: str
    route_type: int | None
    route_color: str | None


class VehicleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle_id: str
    label: str | None
    route_id: int | None
    trip_id: str | None
    latitude: float
    longitude: float
    speed: float | None
    timestamp: datetime