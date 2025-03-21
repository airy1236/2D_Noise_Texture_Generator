from .noise_type.noise_base import BaseNoise

class NoiseGenerator:
    """noise generator factory class"""
    _noise_types = {}

    @classmethod
    def register_noise(cls, name, noise_class):
        """register new noise type class"""
        if not issubclass(noise_class, BaseNoise):
            raise ValueError("must subclass BaseNoise")
        cls._noise_types[name] = noise_class

    @classmethod
    def get_available_types(cls):
        """get registered noise types"""
        return list(cls._noise_types.keys())

    @classmethod
    def create(cls, noise_type):
        """create specified noise generator"""
        if noise_type not in cls._noise_types:
            raise ValueError(f"unknown noise type: {noise_type}")
        return cls._noise_types[noise_type]()

    @classmethod
    def get_sorted_noise_types(cls):
        """get registered noise types sorted alphabetically"""
        return sorted(cls._noise_types.keys())