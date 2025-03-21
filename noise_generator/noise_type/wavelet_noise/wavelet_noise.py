import numpy as np
from scipy.signal import fftconvolve
from noise import pnoise2, snoise2
from ..noise_base import BaseNoise

class WaveletNoise(BaseNoise):
    # 改进的小波噪声生成器
    
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
            # 动态计算当前倍频程参数
            current_scale = kwargs['base_scale'] * (2 ** octave)
            amplitude = kwargs['persistence'] ** octave
            total_amplitude += amplitude
            
            # 生成小波核
            kernel = self._create_wavelet_kernel(
                size=int(current_scale)*2+1,
                wavelet_type=kwargs['wavelet_type']
            )
            
            # 生成随机噪声并卷积
            octave_noise = np.random.randn(height, width)
            octave_noise = fftconvolve(octave_noise, kernel, mode='same')
            
            # 振幅补偿并叠加
            noise += amplitude * octave_noise / kernel.sum()
        
        return self.normalize(noise / total_amplitude)

    def _create_wavelet_kernel(self, size, wavelet_type):
        # 创建标准小波核
        x = np.linspace(-3, 3, size)
        y = np.linspace(-3, 3, size)
        xx, yy = np.meshgrid(x, y)
        r = np.sqrt(xx**2 + yy**2)
        
        if wavelet_type == 'mexican_hat':
            # 墨西哥帽小波
            kernel = (2 - r**2) * np.exp(-r**2 / 2)
        elif wavelet_type == 'gabor':
            # Gabor小波
            k = 3.0  # 波数
            kernel = np.exp(-r**2 / 2) * np.cos(k * r)
        else:
            raise ValueError("unkown wavelet type")
        
        return kernel - kernel.mean()  # 确保零均值