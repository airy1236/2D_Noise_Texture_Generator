import numpy as np
from noise import snoise2
from scipy.signal import convolve2d

from ..noise_base import BaseNoise

class ErosionNoise(BaseNoise):
    # 模拟自然腐蚀效果
    @classmethod
    def get_parameters(cls):
        return [
            ('iterations', 'Iterations', 'int', 5),
            ('hardness', 'Hardness', 'float', 0.7)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        base = np.random.rand(height, width)
        
        # 腐蚀过程模拟
        kernel = np.array([[0.1, 0.2, 0.1],
                          [0.2, 1.0, 0.2],
                          [0.1, 0.2, 0.1]])
        
        for _ in range(kwargs['iterations']):
            eroded = convolve2d(base, kernel, mode='same')
            mask = (eroded > kwargs['hardness']).astype(float)
            base = base * mask
            
        return self.normalize(base)