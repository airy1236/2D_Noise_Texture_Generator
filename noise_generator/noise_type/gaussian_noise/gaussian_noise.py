import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class GaussianNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('mean', 'Mean', 'float', 0.0),
            ('std', 'Standard Deviation', 'float', 1.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise = np.random.normal(kwargs['mean'], kwargs['std'], (height, width))
        return self.normalize(noise)