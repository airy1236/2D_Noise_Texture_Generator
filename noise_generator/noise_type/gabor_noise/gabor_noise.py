import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class GaborNoise(BaseNoise):
    # 模拟木材、布料等自然材质的噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('k', 'Num_waves', 'float', 0.5),
            ('a', 'Anisotropic', 'float', 0.8),
            ('F0', 'Frequency', 'float', 0.05),
            ('num_impulses', 'Num_impulses', 'int', 64)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        noise = np.zeros((height, width))
        
        # 生成随机脉冲
        phi = np.random.rand(kwargs['num_impulses']) * 2 * np.pi
        pos = np.random.rand(kwargs['num_impulses'], 2) * [width, height]
        
        # 向量化计算
        for i in range(kwargs['num_impulses']):
            dx = x - pos[i,0]
            dy = y - pos[i,1]
            r = np.sqrt((dx * kwargs['a'])**2 + dy**2)
            noise += np.cos(2 * np.pi * kwargs['F0'] * r + phi[i]) * \
                    np.exp(-(kwargs['k']**2 * r**2)/2)
        
        return self.normalize(noise)