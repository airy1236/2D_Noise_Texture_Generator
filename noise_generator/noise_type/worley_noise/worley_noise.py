import numpy as np
from noise import snoise2
from scipy.spatial import distance_matrix

from ..noise_base import BaseNoise

class WorleyNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('feature_points', 'Feature Points', 'int', 50),
            ('distance_type', 'Distance Type', 'choice', ['F1', 'F2', 'F2-F1'])
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        points = np.random.rand(kwargs['feature_points'], 2) * [width, height]
        grid = np.indices((height, width)).transpose(1,2,0)
        
        distances = distance_matrix(
            grid.reshape(-1, 2), 
            points
        ).reshape(height, width, kwargs['feature_points'])
        
        distances.sort(axis=2)
        
        if kwargs['distance_type'] == 'F1':
            noise = distances[:,:,0]
        elif kwargs['distance_type'] == 'F2':
            noise = distances[:,:,1]
        else:
            noise = distances[:,:,1] - distances[:,:,0]
            
        return self.normalize(noise)