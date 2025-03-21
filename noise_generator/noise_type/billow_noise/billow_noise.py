import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class BillowNoise(BaseNoise):
    # �������������Ʋ�Ч��������
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
        
        # ���ɱ�׼�����꣨�ؼ�������
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # ��������������
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
        
        return self.normalize(noise * 2 - 1)  # ���ֶԱȶ���ǿ