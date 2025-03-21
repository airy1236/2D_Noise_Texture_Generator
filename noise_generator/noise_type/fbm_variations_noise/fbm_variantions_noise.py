import numpy as np
from scipy.ndimage import convolve
from noise import pnoise2, snoise2

from ..noise_base import BaseNoise

class FBMVariations(BaseNoise):
    # 分形布朗运动变体
    @classmethod
    def get_parameters(cls):
        return [
            ('octaves', 'Octaves', 'int', 6),
            ('lacunarity', 'Lacunarity', 'float', 2.0),
            ('gain', 'Gain', 'float', 0.5),
            ('ridge', 'Ridge', 'float', 0.3)
        ]

    def generate(self, width, height, seed, **kwargs):
        x_offset = seed * 1000
        y_offset = seed * 2000
        noise = np.zeros((height, width))
        
        for i in range(height):
            for j in range(width):
                x = (j + x_offset) / width
                y = (i + y_offset) / height
                
                amplitude = 1.0
                frequency = 1.0
                total = 0.0
                
                for _ in range(kwargs['octaves']):
                    val = snoise2(x * frequency, y * frequency)
                    if kwargs['ridge'] > 0:
                        val = abs(val) * 2 - 1  # 脊化处理
                    total += val * amplitude
                    amplitude *= kwargs['gain']
                    frequency *= kwargs['lacunarity']
                
                noise[i][j] = total
                
        return self.normalize(noise)