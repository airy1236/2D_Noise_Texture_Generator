import math
import numpy as np
from scipy.ndimage import convolve
from noise import pnoise2, snoise2

from ..noise_base import BaseNoise

class StochasticRotationNoise(BaseNoise):
    # 随机旋转噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('scale', 'Scale', 'float', 50.0),
            ('rot_step', 'rot_step', 'float', 0.5),
            ('octaves', 'Octaves', 'int', 3)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        angles = np.random.uniform(0, 2*np.pi, (height//10+1, width//10+1))
        
        noise = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                x = j / width * kwargs['scale']
                y = i / height * kwargs['scale']
                
                # 双线性插值旋转角度
                gx = x * 0.1
                gy = y * 0.1
                fx = int(gx)
                fy = int(gy)
                
                tx = gx - fx
                ty = gy - fy
                
                angle = (angles[fy, fx] * (1-tx)*(1-ty) +
                        angles[fy, fx+1] * tx*(1-ty) +
                        angles[fy+1, fx] * (1-tx)*ty +
                        angles[fy+1, fx+1] * tx*ty)
                
                # 旋转坐标
                rot_x = x * math.cos(angle) - y * math.sin(angle)
                rot_y = x * math.sin(angle) + y * math.cos(angle)
                
                noise[i][j] = snoise2(rot_x, rot_y, octaves=kwargs['octaves'])
                
        return self.normalize(noise)



