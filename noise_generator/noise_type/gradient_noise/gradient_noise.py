import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class GradientNoise(BaseNoise):
    # 梯度噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Noise Scale', 'float', 0.1),
            ('angle', 'Gradient Angle', 'float', 45.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        angle_rad = np.deg2rad(kwargs['angle'])
        
        # 生成二维坐标网格（关键修正）
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # 计算梯度场（向量化操作）
        grad = xx * np.cos(angle_rad) + yy * np.sin(angle_rad)
        
        # 生成噪声层（使用二维坐标输入）
        @np.vectorize
        def noise_func(x, y):
            return snoise2(x * kwargs['scale'], 
                          y * kwargs['scale'])
        
        noise_layer = noise_func(xx, yy)
        
        # 合成最终噪声
        combined = grad + noise_layer
        return self.normalize(combined)