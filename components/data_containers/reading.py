from dataclasses import dataclass, field
from datetime import datetime
import time

@dataclass(frozen=False)
class Reading:

    __slots__ = ("frequency", "temperature", "compensated", "sg")

    frequency : str
    temperature : str
    compensated : str
    sg : str
    gmt : str = field(init=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    unix_seconds : int = field(init=False, default=int(time.time()))