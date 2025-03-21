import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class PorousNoise(BaseNoise):
    # 多孔噪声     生成泡沫、海绵等多孔结构
    @classmethod
    def get_parameters(cls):
        return [
            ('density', 'Density', 'float', 0.4),
            ('threshold', 'Threshold', 'float', 0.5),
            ('smoothness', 'Smoothness', 'float', 0.3),
            ('scale', 'scale', 'float', 0.1)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 10, height)
        xx, yy = np.meshgrid(x, y)
        
        # 向量化基础噪声计算
        @np.vectorize
        def calc_base(x, y):
            return snoise2(x * kwargs['scale'],
                          y * kwargs['scale'],
                          octaves=3)
        
        base = calc_base(xx, yy)
        
        # 孔洞生成算法
        mask = np.random.rand(*base.shape)
        porous = np.where(mask < kwargs['density'],
                         base - kwargs['threshold'],
                         base + kwargs['smoothness'])
        
        # 增强型平滑过渡
        return self.normalize(np.tanh(porous * 5))