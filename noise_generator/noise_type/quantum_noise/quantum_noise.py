import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class QuantumNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('entanglement', 'Entanglement', 'float', 0.7),
            ('decoherence', 'Decoherence', 'float', 0.2)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        phase = np.random.rand(height, width) * 2*np.pi
        entangled = np.zeros((height, width))
        
        # 量子态演化
        for i in range(height):
            for j in range(width):
                if np.random.rand() < kwargs['entanglement']:
                    # 纠缠相邻像素
                    neighbors = [(i+di,j+dj) for di in [-1,0,1] for dj in [-1,0,1]]
                    for ni, nj in neighbors:
                        if 0<=ni<height and 0<=nj<width:
                            phase[ni,nj] = (phase[i,j] + np.random.normal(0, 0.1)) % (2*np.pi)
                
                # 退相干效应
                phase[i,j] += np.random.normal(0, kwargs['decoherence'])
                entangled[i,j] = np.abs(np.cos(phase[i,j]))
        
        return self.normalize(entangled)