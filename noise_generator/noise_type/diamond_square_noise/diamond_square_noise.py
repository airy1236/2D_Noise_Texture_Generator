import math
import numpy as np

from ..noise_base import BaseNoise

class DiamondSquareNoise(BaseNoise):
    # 钻石-正方形噪声
    @classmethod
    def get_parameters(cls):
        return [
            ('roughness', 'Roughness', 'float', 0.6),
            ('init_range', 'Init_range', 'float', 1.0)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        size = max(width, height)
        size = 2 ** math.ceil(math.log2(size)) + 1
        grid = np.zeros((size, size))
        
        grid[0, 0] = kwargs['init_range'] * np.random.uniform(-1, 1)
        grid[0, -1] = kwargs['init_range'] * np.random.uniform(-1, 1)
        grid[-1, 0] = kwargs['init_range'] * np.random.uniform(-1, 1)
        grid[-1, -1] = kwargs['init_range'] * np.random.uniform(-1, 1)
        
        step = size - 1
        while step > 1:
            self._diamond_step(grid, step, kwargs['roughness'])
            self._square_step(grid, step, kwargs['roughness'])
            step = step // 2
            kwargs['roughness'] *= 0.5
        
        return self.normalize(grid[:height, :width])

    def _diamond_step(self, grid, step, roughness):
        half = step // 2
        for y in range(0, grid.shape[0]-1, step):
            for x in range(0, grid.shape[1]-1, step):
                avg = (grid[y, x] + 
                       grid[y, x+step] + 
                       grid[y+step, x] + 
                       grid[y+step, x+step]) / 4
                grid[y+half, x+half] = avg + roughness * np.random.uniform(-1, 1)

    def _square_step(self, grid, step, roughness):
        half = step // 2
        for y in range(0, grid.shape[0], half):
            for x in range((y + half) % step, grid.shape[1], step):
                total = 0
                count = 0
                if x >= half:
                    total += grid[y, x - half]
                    count +=1
                if x + half < grid.shape[1]:
                    total += grid[y, x + half]
                    count +=1
                if y >= half:
                    total += grid[y - half, x]
                    count +=1
                if y + half < grid.shape[0]:
                    total += grid[y + half, x]
                    count +=1
                if count > 0:
                    grid[y, x] = total/count + roughness * np.random.uniform(-1, 1)
