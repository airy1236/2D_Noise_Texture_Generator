import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class WoodNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('ring_freq', 'Ring Frequency', 'float', 15.0),  # 年轮频率
            ('grain_freq', 'Grain Frequency', 'float', 1.0), # 纹理频率
            ('turbulence', 'Turbulence', 'float', 0.5)       # 湍流强度
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
               
        # 生成标准化坐标网格（向量化计算）
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # 计算极坐标参数
        radius = np.sqrt(xx**2 + yy**2)
        angle = np.arctan2(yy, xx)
        
        # 添加湍流效果（向量化实现）
        @np.vectorize  # 关键修正：添加向量化装饰器
        def calculate_turbulence(x, y):
            return snoise2(x*10, y*10, 1) * kwargs['turbulence']
        
        turbulence = calculate_turbulence(xx, yy)
        
        # 合成最终噪声
        noise = np.sin(
            radius * kwargs['ring_freq'] + 
            angle * kwargs['grain_freq'] + 
            turbulence
        )
        
        return self.normalize(noise)