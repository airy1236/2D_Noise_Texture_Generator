import numpy as np
from noise import snoise2
from scipy.spatial import Voronoi

from ..noise_base import BaseNoise

class CellularNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('num_points', 'Number of Points', 'int', 50),
            ('distance_type', 'Distance Type', 'choice', ['Euclidean', 'Manhattan', 'Chebyshev'])
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        num_points = kwargs['num_points']
        points = np.random.rand(num_points, 2) * [width, height]
        
        # 生成Voronoi图
        vor = Voronoi(points)
        
        # 创建距离场
        x = np.arange(width)
        y = np.arange(height)
        xx, yy = np.meshgrid(x, y)
        grid_points = np.column_stack([xx.ravel(), yy.ravel()])
        
        distances = []
        for p in grid_points:
            if kwargs['distance_type'] == 'Euclidean':
                d = np.sqrt(np.sum((points - p)**2, axis=1))
            elif kwargs['distance_type'] == 'Manhattan':
                d = np.sum(np.abs(points - p), axis=1)
            else:  # Chebyshev
                d = np.max(np.abs(points - p), axis=1)
            distances.append(np.min(d))
        
        noise = np.array(distances).reshape(height, width)
        return self.normalize(noise)