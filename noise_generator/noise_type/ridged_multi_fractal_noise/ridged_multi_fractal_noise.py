import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class RidgedMultifractal(BaseNoise):
    # Ridged多分形噪声    生成尖锐的山脊状结构
    @classmethod
    def get_parameters(cls):
        return [
            ('octaves', 'Octaves', 'int', 6),
            ('lacunarity', 'Lacunarity', 'float', 2.0),
            ('offset', 'Offset', 'float', 1.0),
            ('gain', 'Gain', 'float', 2.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise = np.ones((height, width))
        
        # 生成标准化坐标网格
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # 向量化噪声计算
        @np.vectorize
        def ridged_noise(x, y):
            return kwargs['offset'] - np.abs(snoise2(x, y))
        
        freq = 1.0
        amp = 1.0
        for _ in range(kwargs['octaves']):
            signal = ridged_noise(xx * freq, yy * freq)
            signal **= 2 
            noise += signal * amp
            freq *= kwargs['lacunarity']
            amp *= signal * kwargs['gain']
        
        return self.normalize(noise)
