# this requires python 3.7+
from dataclasses import dataclass


@dataclass
class VehicleInfo:
    vin: str
    environment: str
    km: int = None
    whatever: str = None