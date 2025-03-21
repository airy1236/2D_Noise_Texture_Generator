import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class FractalNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Scale', 'float', 50.0),
            ('octaves', 'Octaves', 'int', 6),
            ('persistence', 'Persistence', 'float', 0.5),
            ('lacunarity', 'Lacunarity', 'float', 2.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise = np.zeros((height, width))
        x_offset = seed * 1000
        y_offset = seed * 2000
        
        for i in range(height):
            for j in range(width):
                value = 0.0
                amplitude = 1.0
                frequency = 1.0
                for _ in range(kwargs['octaves']):
                    x = (j/width + x_offset) * frequency * kwargs['scale']
                    y = (i/height + y_offset) * frequency * kwargs['scale']
                    value += amplitude * snoise2(x, y)
                    frequency *= kwargs['lacunarity']
                    amplitude *= kwargs['persistence']
                noise[i][j] = value
        return self.normalize(noise)