import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class WoodNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('ring_freq', 'Ring Frequency', 'float', 15.0),  # ����Ƶ��
            ('grain_freq', 'Grain Frequency', 'float', 1.0), # ����Ƶ��
            ('turbulence', 'Turbulence', 'float', 0.5)       # ����ǿ��
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
               
        # ���ɱ�׼�������������������㣩
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # ���㼫�������
        radius = np.sqrt(xx**2 + yy**2)
        angle = np.arctan2(yy, xx)
        
        # �������Ч����������ʵ�֣�
        @np.vectorize  # �ؼ����������������װ����
        def calculate_turbulence(x, y):
            return snoise2(x*10, y*10, 1) * kwargs['turbulence']
        
        turbulence = calculate_turbulence(xx, yy)
        
        # �ϳ���������
        noise = np.sin(
            radius * kwargs['ring_freq'] + 
            angle * kwargs['grain_freq'] + 
            turbulence
        )
        
        return self.normalize(noise)