import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class NeuralNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('model_depth', 'Model_depth', 'int', 5),
            ('layer_size', 'Layer_size', 'int', 8),
            ('activation', 'Activation', 'choice', ['relu', 'sigmoid', 'tanh'])
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        x = np.linspace(-5, 5, width)
        y = np.linspace(-5, 5, height)
        xx, yy = np.meshgrid(x, y)
        
        def neural_field(x, y):
            input_val = np.stack([x, y], axis=-1).astype(np.float32)
            
            for _ in range(kwargs['model_depth']):
                # He初始化权重
                weights = np.random.randn(input_val.shape[-1], kwargs['layer_size']) * np.sqrt(2/input_val.shape[-1])
                input_val = input_val @ weights
                
                # 增强非线性
                if kwargs['activation'] == 'relu':
                    input_val = np.maximum(0, input_val)
                elif kwargs['activation'] == 'sigmoid':
                    input_val = 1/(1+np.exp(-input_val))
                else:
                    input_val = np.tanh(input_val)
            
            return input_val.mean(axis=-1)
        
        # 多尺度融合
        noise1 = neural_field(xx, yy)
        noise2 = neural_field(xx*0.5, yy*0.5)
        return self.normalize(noise1 + 0.5*noise2)