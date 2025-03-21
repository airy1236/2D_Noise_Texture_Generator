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
        noise = np.full((height, width), 128, dtype=np.uint8)  # 灰色背景
        total_pixels = width * height
        num_corrupted = int(total_pixels * kwargs['density'])
        salt_pixels = int(num_corrupted * kwargs['salt_ratio'])
        
        # 生成盐噪声（白色）
        salt_coords = np.random.choice(total_pixels, salt_pixels, replace=False)
        noise.flat[salt_coords] = 255
        
        # 生成胡椒噪声（黑色）
        pepper_coords = np.random.choice(total_pixels, num_corrupted - salt_pixels, replace=False)
        noise.flat[pepper_coords] = 0
        
        return noise