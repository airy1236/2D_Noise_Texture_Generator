from .generator import NoiseGenerator

from .noise_type.perlin_noise import perlin_noise
from .noise_type.white_noise import white_noise
from .noise_type.simplex_noise import simplex_noise
from .noise_type.fractal_noise import fractal_noise
from .noise_type.gaussian_noise import gaussian_noise
from .noise_type.salt_pepper_noise import salt_pepper_noise
from .noise_type.cellular_noise import cellular_noise
from .noise_type.blue_noise import blue_noise
from .noise_type.voronoi_noise import voronoi_noise
from .noise_type.worley_noise import worley_noise
from .noise_type.marble_noise import marble_noise
from .noise_type.wood_noise import wood_noise
from .noise_type.value_noise import value_noise
from .noise_type.fbm_noise import fbm_noise
from .noise_type.turbulence_noise import turbulence_noise
from .noise_type.checkerboard_noise import checkboard_noise
from .noise_type.gradient_noise import gradient_noise
from .noise_type.hash_noise import hash_noise
from .noise_type.lava_noise import lava_noise
from .noise_type.cloud_noise import cloud_noise
from .noise_type.gabor_noise import gabor_noise
from .noise_type.billow_noise import billow_noise
from .noise_type.ridged_multi_fractal_noise import ridged_multi_fractal_noise
from .noise_type.terrain_noise import terrain_noise
from .noise_type.curl_noise import curl_noise
from .noise_type.lattice_noise import lattice_noise
from .noise_type.erosion_noise import erosion_noise
from .noise_type.anisotropic_noise import anisotropic_noise
from .noise_type.porous_noise import porous_noise
from .noise_type.emi_noise import emi_noise
from .noise_type.crystal_growth_noise import crystal_growth_noise
from .noise_type.quantum_noise import quantum_noise
from .noise_type.neural_noise import neural_noise
from .noise_type.wavelet_noise import wavelet_noise
from .noise_type.pointillism_noise import pointillism_noise
from .noise_type.reaction_diffusion_noise import reaction_diffusion_noise
from .noise_type.fbm_variations_noise import fbm_variantions_noise
from .noise_type.stochastic_rotation_noise import stochastic_rotation_noise
from .noise_type.diamond_square_noise import diamond_square_noise
from .noise_type.flow_noise import flow_noise
from .noise_type.permutation_noise import permutation_noise



# register noise type
noise_types = [
	white_noise.WhiteNoise,
	gaussian_noise.GaussianNoise,
	perlin_noise.PerlinNoise,
	simplex_noise.SimplexNoise,
	fractal_noise.FractalNoise,
	salt_pepper_noise.SaltPepperNoise,
	cellular_noise.CellularNoise,
	blue_noise.BlueNoise,
	voronoi_noise.VoronoiNoise,
	worley_noise.WorleyNoise,
	marble_noise.MarbleNoise,
	wood_noise.WoodNoise,
	value_noise.ValueNoise,
	fbm_noise.FBmNoise,
	turbulence_noise.TurbulenceNoise,
	checkboard_noise.CheckerboardNoise,
	gradient_noise.GradientNoise,
	hash_noise.HashNoise,
	lava_noise.LavaNoise,
	cloud_noise.CloudNoise,
	gabor_noise.GaborNoise,
	billow_noise.BillowNoise,
	ridged_multi_fractal_noise.RidgedMultifractal,
	terrain_noise.TerrainNoise,
	curl_noise.CurlNoise,
	lattice_noise.LatticeNoise,
	erosion_noise.ErosionNoise,
	anisotropic_noise.AnisotropicNoise,
	porous_noise.PorousNoise,
	emi_noise.EMINoise,
	crystal_growth_noise.CrystalNoise,
	quantum_noise.QuantumNoise,
	neural_noise.NeuralNoise,
	wavelet_noise.WaveletNoise,
	pointillism_noise.PointillismNoise,
	reaction_diffusion_noise.ReactionDiffusionNoise,
	fbm_variantions_noise.FBMVariations,
	stochastic_rotation_noise.StochasticRotationNoise,
	diamond_square_noise.DiamondSquareNoise,
	flow_noise.FlowNoise,
	permutation_noise.PermutationNoise,

	]

# register save file type
filetypes = [
	("PNG file", "*.png"), 
	("JPG file", "*.jpg"), 
	("TGA file", "*.tga"),
	("all files", "*.*")
	]






	

for noise_cls in noise_types:
    NoiseGenerator.register_noise(noise_cls.__name__.rsplit('Noise',1)[0], noise_cls)
