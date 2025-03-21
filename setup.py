from setuptools import setup, find_packages

setup (
	name = "2D _Noise_Texture_Generator",	
	version = "0.0.1",
	packages = find_packages(),
	install_requires = [
		"noise==1.2.2",
		"numpy==2.2.4",
		"Pillow==11.1.0"
        "scipy==1.15.2",
		"setuptools==70.2.0",
    ],
	
	python_requires = '>=3.8',

)