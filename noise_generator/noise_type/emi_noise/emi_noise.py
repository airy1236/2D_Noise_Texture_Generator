import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class EMINoise(BaseNoise):
    # ��Ÿ�������     ģ������豸����Ч��
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
        
        # �����ز��ź�
        carrier = np.sin(xx * kwargs['carrier_freq'] * 2*np.pi)
        
        # ������������������
        @np.vectorize
        def calc_am_noise(x, y):
            return snoise2(x*0.1, y*0.1, octaves=3)
        
        am_noise = calc_am_noise(xx, yy) * kwargs['modulation']
        emi = (1 + am_noise) * carrier * kwargs['interference']
        return self.normalize(emi * 2)  # ��ǿ�Աȶ�