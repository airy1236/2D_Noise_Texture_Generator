import numpy as np
from noise import snoise2, pnoise2

from ..noise_base import BaseNoise

class FBmNoise(BaseNoise):
    # 分形布朗运动
    @classmethod
    def get_parameters(cls):
        return [
            ('base_type', 'Base Noise', 'choice', ['perlin', 'simplex']),
            ('octaves', 'Octaves', 'int', 6),
            ('lacunarity', 'Lacunarity', 'float', 2.0),
            ('persistence', 'Persistence', 'float', 0.5)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise_func = snoise2 if kwargs['base_type'] == 'simplex' else pnoise2
        noise = np.zeros((height, width))
        freq = 1.0
        amp = 1.0
        
        for _ in range(kwargs['octaves']):
            layer = np.zeros((height, width))
            for i in range(height):
                for j in range(width):
                    layer[i,j] = noise_func(i*freq/100, j*freq/100)
            noise += layer * amp
            freq *= kwargs['lacunarity']
            amp *= kwargs['persistence']
        return self.normalize(noise)
