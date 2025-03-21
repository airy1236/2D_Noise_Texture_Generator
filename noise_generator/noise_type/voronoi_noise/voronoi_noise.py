import numpy as np
from noise import snoise2
from scipy.spatial import distance

from ..noise_base import BaseNoise

class VoronoiNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('points', 'Feature Points', 'int', 50),
            ('distance_type', 'Distance Type', 'choice', ['euclidean', 'manhattan'])
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        points = np.random.rand(kwargs['points'], 2) * [width-1, height-1]
        
        # 生成坐标网格（修正形状问题）
        y, x = np.mgrid[0:height, 0:width]
        coords = np.column_stack((x.ravel(), y.ravel()))
        
        # 计算距离矩阵
        if kwargs['distance_type'] == 'euclidean':
            dist_matrix = distance.cdist(coords, points, 'euclidean')
        else:
            dist_matrix = distance.cdist(coords, points, 'cityblock')
        
        noise = dist_matrix.min(axis=1).reshape(height, width)
        return self.normalize(noise)