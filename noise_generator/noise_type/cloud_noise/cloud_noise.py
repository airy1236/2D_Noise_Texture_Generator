import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class CloudNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('octaves', 'Octaves', 'int', 6),
            ('persistence', 'Persistence', 'float', 0.7)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                value = 0.0
                amplitude = 1.0
                freq = 0.01
                for _ in range(kwargs['octaves']):
                    value += snoise2(i*freq, j*freq) * amplitude
                    freq *= 2
                    amplitude *= kwargs['persistence']
                noise[i,j] = value
        return self.normalize(noise)