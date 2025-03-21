import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class BillowNoise(BaseNoise):
    # 用于生成蓬松云层效果的噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('octaves', 'Octaves', 'int', 6),
            ('frequency', 'Frequency', 'float', 0.005),
            ('lacunarity', 'Lacunarity', 'float', 2.0),
            ('persistence', 'Persistence', 'float', 0.5)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise = np.zeros((height, width))
        
        # 生成标准化坐标（关键修正）
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # 向量化噪声函数
        @np.vectorize
        def billow_noise(x, y):
            return np.abs(snoise2(x, y))
        
        freq = kwargs['frequency']
        amp = 1.0
        for _ in range(kwargs['octaves']):
            layer = billow_noise(xx * freq, yy * freq) * amp
            noise += layer
            freq *= kwargs['lacunarity']
            amp *= kwargs['persistence']
        
        return self.normalize(noise * 2 - 1)  # 保持对比度增强