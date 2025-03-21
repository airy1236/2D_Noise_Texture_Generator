import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class PorousNoise(BaseNoise):
    # �������     ������ĭ������ȶ�׽ṹ
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
        
        # ������������������
        @np.vectorize
        def calc_base(x, y):
            return snoise2(x * kwargs['scale'],
                          y * kwargs['scale'],
                          octaves=3)
        
        base = calc_base(xx, yy)
        
        # �׶������㷨
        mask = np.random.rand(*base.shape)
        porous = np.where(mask < kwargs['density'],
                         base - kwargs['threshold'],
                         base + kwargs['smoothness'])
        
        # ��ǿ��ƽ������
        return self.normalize(np.tanh(porous * 5))