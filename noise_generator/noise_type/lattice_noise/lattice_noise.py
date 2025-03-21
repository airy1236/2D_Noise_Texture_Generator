import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class LatticeNoise(BaseNoise):
    # 生成晶格状规则图案
    @classmethod
    def get_parameters(cls):
        return [
            ('cell_size', 'Cell_size', 'int', 32),
            ('pattern', 'Pattern', 'choice', ['square', 'hex', 'triangle'])
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        
        # 生成基础晶格
        if kwargs['pattern'] == 'square':
            grid = (x//kwargs['cell_size'] + y//kwargs['cell_size']) % 2
        elif kwargs['pattern'] == 'hex':
            dx = x // kwargs['cell_size']
            dy = y // (kwargs['cell_size'] * np.sqrt(3)/2)
            grid = (dx + dy) % 2
        else:  # triangle
            grid = (x//kwargs['cell_size'] + (y//kwargs['cell_size'])*2) % 3
            
        return (grid * 255).astype(np.uint8)