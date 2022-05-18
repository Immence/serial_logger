import time
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=False)
class BathReading:

    __slots__ = ("temperature", "sg")

    temperature : str
    sg : str
    gmt : str = field(init=False, default=datetime.now().strftime("%d/%m/%Y-%H:%M:%S"))
    unix_seconds : int = field(init=False, default=int(time.time()))

    def get_sg(self) -> float:
        return float(self.sg)

    def get_temperature(self) -> float:
        return float(self.temperature)
            
    def to_dict(self) -> dict:
        return {"bath_temperature" : self.temperature, "bath_sg": self.sg}

    def validate(self) -> bool:
        return self.temperature is not None and self.sg is not None
