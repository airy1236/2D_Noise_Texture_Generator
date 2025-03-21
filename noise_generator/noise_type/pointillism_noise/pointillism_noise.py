import numpy as np
from scipy.ndimage import convolve

from ..noise_base import BaseNoise

class PointillismNoise(BaseNoise):
    # 点彩派噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('density', 'Density', 'float', 0.05),
            ('radius', 'Radius', 'int', 3),
            ('jitter', 'Jitter', 'float', 0.3)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        canvas = np.zeros((height, width))
        num_points = int(width * height * kwargs['density'])
        
        # 生成带抖动的点位置
        points = np.column_stack((
            np.random.uniform(0, height, num_points),
            np.random.uniform(0, width, num_points)
        )) + np.random.uniform(-kwargs['jitter'], kwargs['jitter'], (num_points, 2))
        
        # 绘制圆形点
        radius = kwargs['radius']
        for y, x in points:
            yy, xx = np.ogrid[-y:height-y, -x:width-x]
            mask = xx**2 + yy**2 <= radius**2
            canvas[mask] += 1.0
        
        return self.normalize(canvas)



