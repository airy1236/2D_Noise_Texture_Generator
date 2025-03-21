import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class GradientNoise(BaseNoise):
    # �ݶ�����
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Noise Scale', 'float', 0.1),
            ('angle', 'Gradient Angle', 'float', 45.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        angle_rad = np.deg2rad(kwargs['angle'])
        
        # ���ɶ�ά�������񣨹ؼ�������
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # �����ݶȳ���������������
        grad = xx * np.cos(angle_rad) + yy * np.sin(angle_rad)
        
        # ���������㣨ʹ�ö�ά�������룩
        @np.vectorize
        def noise_func(x, y):
            return snoise2(x * kwargs['scale'], 
                          y * kwargs['scale'])
        
        noise_layer = noise_func(xx, yy)
        
        # �ϳ���������
        combined = grad + noise_layer
        return self.normalize(combined)