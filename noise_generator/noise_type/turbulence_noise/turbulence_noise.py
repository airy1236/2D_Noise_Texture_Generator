import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class TurbulenceNoise(BaseNoise):
    # 湍流噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('octaves', 'Octaves', 'int', 3),
            ('energy_ratio', 'Energy_ratio', 'float', 0.7),
            ('vorticity', 'Vorticity', 'float', 1.2),
            ('time_step', 'Time_step', 'float', 0.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        
        # 生成标准化坐标系统
        x = np.linspace(0, 1, width)  # 标准化到[0,1]范围
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # 向量化噪声生成函数
        @np.vectorize
        def vectorized_snoise(x, y, octaves=1):
            return snoise2(x, y, octaves=octaves)
        
        # 生成速度势场
        @np.vectorize
        def potential(x, y):
            t = kwargs['time_step'] * 0.1
            real_part = vectorized_snoise(x + t, y, octaves=3)
            imag_part = vectorized_snoise(x - t, y + 1.0, octaves=3)
            return real_part + 1j * imag_part
        
        psi = potential(xx * 2*np.pi, yy * 2*np.pi)  # 缩放至[0,2π]
        
        # 计算速度场（使用复数梯度）
        dx, dy = np.gradient(psi)
        vx = dy.real * kwargs['vorticity']
        vy = -dx.imag * kwargs['vorticity']
        
        # 构建湍流场
        turbulence = np.zeros_like(xx)
        freq = 1.0
        energy = 1.0
        
        for _ in range(kwargs['octaves']):
            # 生成当前尺度噪声层
            layer = vectorized_snoise(xx * freq, yy * freq, octaves=1)
            
            # Kolmogorov能量衰减定律
            amp = energy * (freq ** (-5/3))
            layer *= amp
            
            # 旋度场调制（从第三次倍频开始）
            if _ >= 2:
                velocity_mag = np.sqrt(vx**2 + vy**2)
                layer *= velocity_mag
                
            turbulence += layer
            
            # 更新参数
            energy *= kwargs['energy_ratio']
            freq *= 2.0
        
        # 非线性变换增强细节
        turbulence = np.sin(turbulence * np.pi) * np.exp(-0.1 * turbulence**2)
        
        return self.normalize(turbulence)