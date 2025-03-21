import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class ValueNoise(BaseNoise):
    # ֵ�������������ֵ�Ĳ�ֵ������
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
        
        # ����������
        grid_w = (width // cell_size) + 2
        grid_h = (height // cell_size) + 2
        grid = rng.random((grid_h, grid_w))
        
        # ��������ӳ��
        x = np.linspace(0, grid_w-1, width)
        y = np.linspace(0, grid_h-1, height)
        xi, yi = np.meshgrid(x, y)
        
        # ��ֵ����
        if kwargs['interp'] == 'linear':
            from scipy.ndimage import map_coordinates
            noise = map_coordinates(grid, [yi, xi], order=1)
        else:
            from scipy.ndimage import map_coordinates
            noise = map_coordinates(grid, [yi, xi], order=3)
        
        return self.normalize(noise)