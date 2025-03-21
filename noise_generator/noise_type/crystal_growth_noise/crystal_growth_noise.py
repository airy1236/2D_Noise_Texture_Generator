import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class CrystalNoise(BaseNoise):
    # �ᾧ��������     ģ����ﾧ�塢�����γ�
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
        
        # ����������ˣ����ȷֲ���
        seeds = [
            (np.random.randint(0, height), np.random.randint(0, width))
            for _ in range(kwargs['num_seeds'])
        ]

        def grow(x, y, depth, angle):
            # ����ת����߽���
            x_int = int(np.round(x))
            y_int = int(np.round(y))
            if not (0 <= x_int < width and 0 <= y_int < height):
                return
            
            # ��̬ǿ�ȼ��㣨�������˥����
            strength = 1.0 / (1.0 + depth**0.5)
            grid[y_int, x_int] += strength * kwargs['intensity']
            
            # ��ֹ�����Ż�
            if depth >= kwargs['max_depth']:
                return
            
            # ������������
            rad = np.deg2rad(angle)
            dx = kwargs['step_size'] * np.cos(rad)
            dy = kwargs['step_size'] * np.sin(rad)
            
            # ����������
            new_angle = angle + np.random.normal(0, kwargs['angle_var'])
            grow(x + dx, y + dy, depth + 1, new_angle)
            
            # �ֲ������������ԣ�
            if np.random.uniform() < kwargs['branch_prob']:
                branch_angle = angle + np.random.uniform(-120, 120)
                grow(x, y, depth + 1, branch_angle)

        # ���������������
        for y_start, x_start in seeds:
            init_angle = np.random.uniform(0, 360)
            grow(x_start, y_start, 0, init_angle)

        # ������ǿ�Աȶ�
        grid = np.exp(grid) - 1
        return self.normalize(grid)