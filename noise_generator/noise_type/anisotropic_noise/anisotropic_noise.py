import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class AnisotropicNoise(BaseNoise):
    # 模拟木材纹理、织物等方向性材质
    @classmethod
    def get_parameters(cls):
        return [
            ('direction', 'Direction', 'float', 45.0),
            ('stretch', 'Stretch', 'float', 5.0),
            ('frequency', 'Freuency', 'float', 0.02),
            ('octaves', 'Octaves', 'int', 3)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        theta = np.deg2rad(kwargs['direction'])
        rot_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        
        # 生成网格坐标系统（优化实现）
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 10, height)
        xx, yy = np.meshgrid(x, y)
        coords = np.stack([xx, yy], axis=-1)
        
        # 应用坐标变换
        stretched_coords = (coords @ rot_matrix) * [1, kwargs['stretch']]
        
        # 向量化噪声计算
        @np.vectorize
        def calc_noise(x, y):
            return snoise2(x * kwargs['frequency'],
                          y * kwargs['frequency'],
                          octaves=kwargs['octaves'])
        
        noise = calc_noise(stretched_coords[...,0], stretched_coords[...,1])
        return self.normalize(noise)