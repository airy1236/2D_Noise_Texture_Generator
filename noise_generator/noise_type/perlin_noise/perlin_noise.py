import numpy as np
from noise import pnoise2

from ..noise_base import BaseNoise

class PerlinNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Scale', 'float', 50.0),
            ('octaves', 'Octaves', 'int', 6),
            ('persistence', 'Persistence', 'float', 0.5),
            ('lacunarity', 'Lacunarity', 'float', 2.0),
            ('repeatx', 'X Repeat', 'int', 1024),
            ('repeaty', 'Y Repeat', 'int', 1024)
        ]

    def generate(self, width, height, seed, **kwargs):
        noise = np.zeros((height, width))
        x_offset = seed * 1000
        y_offset = seed * 2000
        
        for i in range(height):
            for j in range(width):
                x = j/width + x_offset
                y = i/height + y_offset
                noise[i][j] = pnoise2(
                    x * kwargs['scale'],
                    y * kwargs['scale'],
                    octaves=kwargs['octaves'],
                    persistence=kwargs['persistence'],
                    lacunarity=kwargs['lacunarity'],
                    repeatx=kwargs['repeatx'],
                    repeaty=kwargs['repeaty'],
                    base=0
                )
        return self.normalize(noise)