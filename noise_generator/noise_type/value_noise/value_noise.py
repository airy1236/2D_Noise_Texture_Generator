import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class ValueNoise(BaseNoise):
    # 值噪声（基于随机值的插值噪声）
    @classmethod
    def get_parameters(cls):
        return [
            ('cell_size', 'Cell Size', 'int', 32),
            ('interp', 'Interpolation', 'choice', ['linear', 'cubic'])
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        cell_size = kwargs['cell_size']
        rng = np.random.default_rng(seed)
        
        # 生成随机格点
        grid_w = (width // cell_size) + 2
        grid_h = (height // cell_size) + 2
        grid = rng.random((grid_h, grid_w))
        
        # 生成坐标映射
        x = np.linspace(0, grid_w-1, width)
        y = np.linspace(0, grid_h-1, height)
        xi, yi = np.meshgrid(x, y)
        
        # 插值计算
        if kwargs['interp'] == 'linear':
            from scipy.ndimage import map_coordinates
            noise = map_coordinates(grid, [yi, xi], order=1)
        else:
            from scipy.ndimage import map_coordinates
            noise = map_coordinates(grid, [yi, xi], order=3)
        
        return self.normalize(noise)