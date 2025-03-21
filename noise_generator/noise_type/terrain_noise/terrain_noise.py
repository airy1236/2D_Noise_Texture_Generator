import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class TerrainNoise(BaseNoise):
    # ����������ɸ��ӵ���
    @classmethod
    def get_parameters(cls):
        return [
            ('continent_freq', 'Land_freq', 'float', 0.001),
            ('mountain_freq', 'Mountain_freq', 'float', 0.03),
            ('erosion', 'Erosion', 'float', 0.5)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        
        # ���ɱ�׼������ϵͳ
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # ��������������
        @np.vectorize
        def terrain_noise(x, y, freq, octaves):
            return snoise2(x * freq, y * freq, octaves=octaves)
        
        # ��½������״
        base = terrain_noise(xx, yy, kwargs['continent_freq'], 3)
        
        # ɽ��ϸ��
        mountains = terrain_noise(xx, yy, kwargs['mountain_freq'], 8) ** 2
        
        # ��ʴЧ��
        erosion = terrain_noise(xx, yy, 0.1, 1) * kwargs['erosion']
        
        combined = base * 0.7 + mountains * 0.3 + erosion
        return self.normalize(combined)