import numpy as np
from abc import ABC, abstractmethod

# ------------------------- noise abstract base class -------------------------
class BaseNoise(ABC):
    """abstract base class for noise generators"""
    @classmethod
    @abstractmethod
    def get_parameters(cls):
        """return parameter configuration for this noise type"""
        return []

    @abstractmethod
    def generate(self, width, height, seed, **kwargs):
        """generate noise array"""
        pass

    def normalize(self, data):
        """Normalize data to 0-255 range"""
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max - data_min == 0:
            return np.zeros_like(data, dtype=np.uint8)
        return ((data - data_min) / (data_max - data_min) * 255).astype(np.uint8)