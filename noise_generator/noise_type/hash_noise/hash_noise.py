import hashlib
import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class HashNoise(BaseNoise):
    # ɢ������
    @classmethod
    def get_parameters(cls):
        return [('scale', 'Noise Scale', 'float', 0.1)]

    @staticmethod
    def _hash(x, y):
        return int(hashlib.sha256(f"{x:.2f}_{y:.2f}".encode()).hexdigest(), 16) % 1000/1000.0

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        scale = kwargs['scale']
        
        # ʹ��meshgrid��������
        x = np.arange(width) * scale
        y = np.arange(height) * scale
        xx, yy = np.meshgrid(x, y)
        
        # ��������ϣ����
        vector_hash = np.vectorize(self._hash)
        noise = vector_hash(xx, yy)
        return (noise * 255).astype(np.uint8)