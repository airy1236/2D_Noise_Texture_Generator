import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class MarbleNoise(BaseNoise):
    # 大理石纹理
    @classmethod
    def get_parameters(cls):
        return [
            ('frequency', 'Base Frequency', 'float', 0.02),
            ('turbulence', 'Turbulence', 'float', 5.0),
            ('vein_scale', 'Vein Scale', 'float', 0.1)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        x = np.linspace(0, kwargs['frequency'], width)
        y = np.linspace(0, kwargs['frequency'], height)
        xx, yy = np.meshgrid(x, y)
        
        # 向量化处理
        @np.vectorize
        def turbulence(x, y):
            return snoise2(x*5, y*5) * kwargs['turbulence']
        
        pattern = np.sin((xx + turbulence(xx, yy)) * 2*np.pi * kwargs['vein_scale'])
        return self.normalize(pattern)