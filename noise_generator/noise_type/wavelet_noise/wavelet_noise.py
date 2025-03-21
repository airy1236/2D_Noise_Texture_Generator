import numpy as np
from scipy.signal import fftconvolve
from noise import pnoise2, snoise2
from ..noise_base import BaseNoise

class WaveletNoise(BaseNoise):
    # �Ľ���С������������
    
    @classmethod
    def get_parameters(cls):
        return [
            ('octaves', 'Octaves', 'int', 5),
            ('base_scale', 'Base Scale', 'float', 5.0),
            ('persistence', 'Persistence', 'float', 0.6),
            ('wavelet_type', 'Wavelet Type', 'choice', ['mexican_hat', 'gabor'])
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        noise = np.zeros((height, width))
        total_amplitude = 0.0
        
        for octave in range(kwargs['octaves']):
            # ��̬���㵱ǰ��Ƶ�̲���
            current_scale = kwargs['base_scale'] * (2 ** octave)
            amplitude = kwargs['persistence'] ** octave
            total_amplitude += amplitude
            
            # ����С����
            kernel = self._create_wavelet_kernel(
                size=int(current_scale)*2+1,
                wavelet_type=kwargs['wavelet_type']
            )
            
            # ����������������
            octave_noise = np.random.randn(height, width)
            octave_noise = fftconvolve(octave_noise, kernel, mode='same')
            
            # �������������
            noise += amplitude * octave_noise / kernel.sum()
        
        return self.normalize(noise / total_amplitude)

    def _create_wavelet_kernel(self, size, wavelet_type):
        # ������׼С����
        x = np.linspace(-3, 3, size)
        y = np.linspace(-3, 3, size)
        xx, yy = np.meshgrid(x, y)
        r = np.sqrt(xx**2 + yy**2)
        
        if wavelet_type == 'mexican_hat':
            # ī����ñС��
            kernel = (2 - r**2) * np.exp(-r**2 / 2)
        elif wavelet_type == 'gabor':
            # GaborС��
            k = 3.0  # ����
            kernel = np.exp(-r**2 / 2) * np.cos(k * r)
        else:
            raise ValueError("unkown wavelet type")
        
        return kernel - kernel.mean()  # ȷ�����ֵ