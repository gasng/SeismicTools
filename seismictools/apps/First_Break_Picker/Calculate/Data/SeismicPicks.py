import segyio as sio
import numpy as np
from dataclasses import dataclass
import json

@dataclass
class Picks_data:
    trace_index: int
    time : float
    type : str