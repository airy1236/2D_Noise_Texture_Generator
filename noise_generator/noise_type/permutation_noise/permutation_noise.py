import math
import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class PermutationNoise(BaseNoise):
    # 基于排列的噪声

    def __init__(self):
        self.perm = None
        
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Scale', 'float', 50.0),
            ('octaves', 'Octaves', 'int', 3)
        ]

    def generate(self, width, height, seed, **kwargs):
        if self.perm is None:
            np.random.seed(seed)
            self.perm = np.random.permutation(512)
        
        noise = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                x = j / width * kwargs['scale']
                y = i / height * kwargs['scale']
                value = 0.0
                amp = 1.0
                
                for _ in range(kwargs['octaves']):
                    xi = int(x) & 255
                    yi = int(y) & 255
                    grad = self.perm[(self.perm[xi] + yi) & 255] / 255.0 * 2 - 1
                    value += amp * grad
                    x *= 2
                    y *= 2
                    amp *= 0.5
                
                noise[i][j] = value
                
        return self.normalize(noise)




