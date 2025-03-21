import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class BlueNoise(BaseNoise):
    @classmethod
    def get_parameters(cls):
        return [
            ('radius', 'Min Distance', 'float', 0.05),  # 相对尺寸的比例
            ('max_samples', 'Max Samples', 'int', 100)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        radius = kwargs['radius'] * min(width, height)
        points = []
        
        # 泊松圆盘采样
        grid_size = int(radius / np.sqrt(2))
        grid = np.full((height//grid_size+2, width//grid_size+2), -1, dtype=int)
        
        active = []
        first_point = (np.random.uniform(0, width), np.random.uniform(0, height))
        active.append(first_point)
        points.append(first_point)
        
        while active:
            idx = np.random.randint(len(active))
            parent = active[idx]
            
            found = False
            for _ in range(30):
                angle = np.random.uniform(0, 2*np.pi)
                dist = np.random.uniform(radius, 2*radius)
                x = parent[0] + dist * np.cos(angle)
                y = parent[1] + dist * np.sin(angle)
                
                if 0 <= x < width and 0 <= y < height:
                    grid_x, grid_y = int(x//grid_size), int(y//grid_size)
                    valid = True
                    
                    for i in range(max(0, grid_y-1), min(grid.shape[0], grid_y+2)):
                        for j in range(max(0, grid_x-1), min(grid.shape[1], grid_x+2)):
                            if grid[i,j] != -1:
                                dx = x - points[grid[i,j]][0]
                                dy = y - points[grid[i,j]][1]
                                if dx*dx + dy*dy < radius*radius:
                                    valid = False
                                    break
                        if not valid:
                            break
                    
                    if valid:
                        points.append((x,y))
                        active.append((x,y))
                        grid[grid_y, grid_x] = len(points)-1
                        found = True
                        break
            
            if not found:
                active.pop(idx)
        
        # 生成距离场
        x = np.linspace(0, width, width)
        y = np.linspace(0, height, height)
        xx, yy = np.meshgrid(x, y)
        noise = np.zeros((height, width))
        
        for p in points:
            dist = (xx - p[0])**2 + (yy - p[1])**2
            noise = np.maximum(noise, np.sqrt(dist))
        
        return self.normalize(noise)
