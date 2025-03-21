import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class SaltPepperNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('density', 'Density', 'float', 0.05),
            ('salt_ratio', 'Salt Ratio', 'float', 0.5)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise = np.full((height, width), 128, dtype=np.uint8)  # ��ɫ����
        total_pixels = width * height
        num_corrupted = int(total_pixels * kwargs['density'])
        salt_pixels = int(num_corrupted * kwargs['salt_ratio'])
        
        # ��������������ɫ��
        salt_coords = np.random.choice(total_pixels, salt_pixels, replace=False)
        noise.flat[salt_coords] = 255
        
        # ���ɺ�����������ɫ��
        pepper_coords = np.random.choice(total_pixels, num_corrupted - salt_pixels, replace=False)
        noise.flat[pepper_coords] = 0
        
        return noise