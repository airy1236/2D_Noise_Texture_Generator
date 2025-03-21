import math
import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class FlowNoise(BaseNoise):
    # 流噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Sacle', 'float', 50.0),
            ('time', 'Time', 'float', 1.0),
            ('curl', 'Curl', 'float', 0.3)
        ]

    def generate(self, width, height, seed, **kwargs):
        x_offset = seed * 1000
        y_offset = seed * 2000
        noise = np.zeros((height, width))
        
        for i in range(height):
            for j in range(width):
                x = (j + x_offset) / width * kwargs['scale']
                y = (i + y_offset) / height * kwargs['scale']
                
                # 计算流场偏移
                dx = snoise2(x, y + kwargs['time']) * kwargs['curl']
                dy = snoise2(x + 1000, y + kwargs['time']) * kwargs['curl']
                
                # 应用流场变形
                val = snoise2(x + dx, y + dy)
                noise[i][j] = val
                
        return self.normalize(noise)
