import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class EMINoise(BaseNoise):
    # 电磁干扰噪声     模拟电子设备干扰效果
    @classmethod
    def get_parameters(cls):
        return [
            ('interference', 'Interference', 'float', 0.5),
            ('carrier_freq', 'Carrier_freq', 'float', 0.02),
            ('modulation', 'Modulation', 'float', 0.3)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 10, height)
        xx, yy = np.meshgrid(x, y)
        
        # 生成载波信号
        carrier = np.sin(xx * kwargs['carrier_freq'] * 2*np.pi)
        
        # 向量化调幅噪声计算
        @np.vectorize
        def calc_am_noise(x, y):
            return snoise2(x*0.1, y*0.1, octaves=3)
        
        am_noise = calc_am_noise(xx, yy) * kwargs['modulation']
        emi = (1 + am_noise) * carrier * kwargs['interference']
        return self.normalize(emi * 2)  # 增强对比度