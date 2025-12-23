import numpy as np
from dataclasses import dataclass

@dataclass
class Model:
    model: np.ndarray

class ModelReader:
    @staticmethod
    def read(path: str) -> Model:
        return Model(model=np.load(path))