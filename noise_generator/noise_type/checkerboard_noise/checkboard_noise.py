import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class CheckerboardNoise(BaseNoise):
    # ∆Â≈Ã∏Ò‘Î…˘
    @classmethod
    def get_parameters(cls):
        return [('tile_size', 'Tile Size', 'int', 32)]

    def generate(self, width, height, seed, **kwargs):
        ts = kwargs['tile_size']
        return ((np.indices((height, width)) // ts).sum(axis=0) % 2 * 255)