import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class TurbulenceNoise(BaseNoise):
    # ��������
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
        
        # ���ɱ�׼������ϵͳ
        x = np.linspace(0, 1, width)  # ��׼����[0,1]��Χ
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # �������������ɺ���
        @np.vectorize
        def vectorized_snoise(x, y, octaves=1):
            return snoise2(x, y, octaves=octaves)
        
        # �����ٶ��Ƴ�
        @np.vectorize
        def potential(x, y):
            t = kwargs['time_step'] * 0.1
            real_part = vectorized_snoise(x + t, y, octaves=3)
            imag_part = vectorized_snoise(x - t, y + 1.0, octaves=3)
            return real_part + 1j * imag_part
        
        psi = potential(xx * 2*np.pi, yy * 2*np.pi)  # ������[0,2��]
        
        # �����ٶȳ���ʹ�ø����ݶȣ�
        dx, dy = np.gradient(psi)
        vx = dy.real * kwargs['vorticity']
        vy = -dx.imag * kwargs['vorticity']
        
        # ����������
        turbulence = np.zeros_like(xx)
        freq = 1.0
        energy = 1.0
        
        for _ in range(kwargs['octaves']):
            # ���ɵ�ǰ�߶�������
            layer = vectorized_snoise(xx * freq, yy * freq, octaves=1)
            
            # Kolmogorov����˥������
            amp = energy * (freq ** (-5/3))
            layer *= amp
            
            # ���ȳ����ƣ��ӵ����α�Ƶ��ʼ��
            if _ >= 2:
                velocity_mag = np.sqrt(vx**2 + vy**2)
                layer *= velocity_mag
                
            turbulence += layer
            
            # ���²���
            energy *= kwargs['energy_ratio']
            freq *= 2.0
        
        # �����Ա任��ǿϸ��
        turbulence = np.sin(turbulence * np.pi) * np.exp(-0.1 * turbulence**2)
        
        return self.normalize(turbulence)