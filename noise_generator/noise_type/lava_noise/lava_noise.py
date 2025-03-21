import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class LavaNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('turbulence', 'Turbulence', 'float', 3.0),
            ('octaves', 'Octaves', 'int', 5)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        
        # ���ɱ�׼���������񣨹ؼ�������
        x = np.linspace(0, 10, width)  # �Ŵ����귶Χ����ǿϸ��
        y = np.linspace(0, 10, height)
        xx, yy = np.meshgrid(x, y)
        
        # ��������������
        @np.vectorize  # ʹ��������װ����������������
        def lava_noise(x, y):
            return np.abs(snoise2(x, y, kwargs['octaves']))
        
        # ���ɻ���������
        noise = lava_noise(xx, yy)
        
        # �������Ť��
        for _ in range(3):
            noise = np.sin(noise * kwargs['turbulence'])
        
        return self.normalize(noise)