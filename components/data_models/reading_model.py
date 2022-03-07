from dataclasses import dataclass

@dataclass
class Reading:
    """Container for readings returned from device"""
    raw_freq: float
    temp: float
    freq_comp: float
    sg: float