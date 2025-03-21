import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class CurlNoise(BaseNoise):
    # 生成矢量场用于流体模拟
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Scale', 'float', 0.02),
            ('time', 'Time', 'float', 0.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        
        # 向量化噪声计算函数
        @np.vectorize
        def calc_dx(x, y):
            return snoise2(x * kwargs['scale'], 
                          (y * kwargs['scale']) + 1000 + kwargs['time'],
                          octaves=3)
        
        @np.vectorize
        def calc_dy(x, y):
            return snoise2((x * kwargs['scale']) - 1000 - kwargs['time'],
                          y * kwargs['scale'],
                          octaves=3)
        
        # 计算矢量场分量
        dx = calc_dx(x, y)
        dy = calc_dy(x, y)
        
        # 计算旋度场
        curl = np.gradient(dy, axis=1) - np.gradient(dx, axis=0)
        return self.normalize(curl)