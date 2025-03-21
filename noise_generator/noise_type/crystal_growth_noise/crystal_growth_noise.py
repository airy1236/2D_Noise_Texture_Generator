import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class CrystalNoise(BaseNoise):
    # 结晶生长噪声     模拟矿物晶体、冰晶形成
    @classmethod
    def get_parameters(cls):
        return [
            ('branch_prob', 'Branch_prob', 'float', 0.4),
            ('angle_var', 'Angle_var', 'float', 45.0),
            ('max_depth', 'Max_depth', 'int', 15),
            ('num_seeds', 'Num_seeds', 'int', 3),
            ('step_size', 'Step_size', 'float', 2.5),
            ('intensity', 'Intensity', 'float', 5.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        grid = np.zeros((height, width), dtype=np.float32)
        
        # 生成随机晶核（均匀分布）
        seeds = [
            (np.random.randint(0, height), np.random.randint(0, width))
            for _ in range(kwargs['num_seeds'])
        ]

        def grow(x, y, depth, angle):
            # 坐标转换与边界检查
            x_int = int(np.round(x))
            y_int = int(np.round(y))
            if not (0 <= x_int < width and 0 <= y_int < height):
                return
            
            # 动态强度计算（避免过早衰减）
            strength = 1.0 / (1.0 + depth**0.5)
            grid[y_int, x_int] += strength * kwargs['intensity']
            
            # 终止条件优化
            if depth >= kwargs['max_depth']:
                return
            
            # 计算生长方向
            rad = np.deg2rad(angle)
            dx = kwargs['step_size'] * np.cos(rad)
            dy = kwargs['step_size'] * np.sin(rad)
            
            # 主生长方向
            new_angle = angle + np.random.normal(0, kwargs['angle_var'])
            grow(x + dx, y + dy, depth + 1, new_angle)
            
            # 分叉生长（概率性）
            if np.random.uniform() < kwargs['branch_prob']:
                branch_angle = angle + np.random.uniform(-120, 120)
                grow(x, y, depth + 1, branch_angle)

        # 并行生长多个晶核
        for y_start, x_start in seeds:
            init_angle = np.random.uniform(0, 360)
            grow(x_start, y_start, 0, init_angle)

        # 后处理增强对比度
        grid = np.exp(grid) - 1
        return self.normalize(grid)