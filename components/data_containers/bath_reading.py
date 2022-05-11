from dataclasses import dataclass, field
from datetime import datetime
import time

@dataclass(frozen=False)
class BathReading:

    __slots__ = ("temperature", "sg")

    temperature : str
    sg : str
    gmt : str = field(init=False, default=datetime.now().strftime("%d/%m/%Y-%H:%M:%S"))
    unix_seconds : int = field(init=False, default=int(time.time()))

    def to_dict(self) -> dict:
        return {"bath_temperature" : self.temperature, "bath_sg": self.sg}