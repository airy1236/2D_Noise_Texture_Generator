import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class LavaNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('turbulence', 'Turbulence', 'float', 3.0),
            ('octaves', 'Octaves', 'int', 5)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        
        # 生成标准化坐标网格（关键修正）
        x = np.linspace(0, 10, width)  # 放大坐标范围以增强细节
        y = np.linspace(0, 10, height)
        xx, yy = np.meshgrid(x, y)
        
        # 向量化噪声函数
        @np.vectorize  # 使用向量化装饰器处理数组输入
        def lava_noise(x, y):
            return np.abs(snoise2(x, y, kwargs['octaves']))
        
        # 生成基础噪声层
        noise = lava_noise(xx, yy)
        
        # 添加湍流扭曲
        for _ in range(3):
            noise = np.sin(noise * kwargs['turbulence'])
        
        return self.normalize(noise)