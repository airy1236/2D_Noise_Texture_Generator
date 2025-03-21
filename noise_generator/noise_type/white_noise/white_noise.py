import numpy as np
from noise import pnoise2

from ..noise_base import BaseNoise

class WhiteNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return []

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        return np.random.randint(0, 255, (height, width))