# 2D Noise Texture Generator

## 目录

- [概述]
- [构建]
- [结构]
- [使用]

### 概述
- 本项目的意图在于研究一些常见或不常见的噪声生成算法，并将它们集成在一个工具中以后使用。
- 这个项目是一个小工具，它目前支持41中噪声生成方式，其中的一些效果可能不是很理想。
- 你可以使用它生成许多种类和样式的噪声纹理，它们全部由CPU生成，关于GPU的生成的噪声效率肯定会更高，但是本人对于python在GPU上的变成不是很了解，不过目前的状态应付一些简单的噪声纹理生成已经足够了。


### 构建

- 本项目使用vscode编写，你也可以使用其他的构建方式，但是尽量不要改变项目中文件的结构。
- python>=3.8

### 结构
```bash
2D_Noise_Texture_Generator/
│
├── editor/                       # 编辑器UI模块
│   └── editor.py                 # 编辑器UI的管理类
│
├── noise_generator/              # 核心的噪声管理与生成模块
│   ├── noise_type/               # 各种类型的噪声实现类
│   │   ├── anistropic_noise/     
│   │   │   └── anistropic_noise  # 具体的噪声实现类
│   │   ├── .../                  # 其他噪声实现类
│   │   │
│   │   └── noise_base.py         # 噪声的抽象类
│   │
│   ├── generator.py              # 噪声生成类
│   │
│   └── register.py               # 噪声种类的注册
│
├── 2D_Noise_Texture_Generator.py # 主函数
│
├── setup.py                      # setup.py
│
└── README.md                     # README.md
```

- noise_type中的noise_base.py写有噪声基类里面，所有噪声都继承了这个抽象类，其中有一些所有噪声共同使用的方法。
- register.py用于注册噪声，让系统知道有这个噪声的存在。

### 使用

- 此项目写得非常直觉，调整参数，点击generator按钮就可以在右侧生成一个预览框中的图片，点击save就可以保存这种图片。
- 本项目中支持多种噪声生成方式，当然你也可以增加自己的噪声生成方式
```
噪声基类
import numpy as np
from abc import ABC, abstractmethod

class BaseNoise(ABC):
    """abstract base class for noise generators"""
    @classmethod
    @abstractmethod
    def get_parameters(cls):
        """return parameter configuration for this noise type"""
        return []

    @abstractmethod
    def generate(self, width, height, seed, **kwargs):
        """generate noise array"""
        pass

    def normalize(self, data):
        """Normalize data to 0-255 range"""
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max - data_min == 0:
            return np.zeros_like(data, dtype=np.uint8)
        return ((data - data_min) / (data_max - data_min) * 255).astype(np.uint8)
```
你需要在你的噪声生成方式中实现get_parameters和generate函数/
```
像这样
import numpy as np
from noise import snoise2

from ..noise_base import BaseNoise

class AnisotropicNoise(BaseNoise):
    # 模拟木材纹理、织物等方向性材质
    @classmethod
    def get_parameters(cls):
        return [
            ('direction', 'Direction', 'float', 45.0),
            ('stretch', 'Stretch', 'float', 5.0),
            ('frequency', 'Freuency', 'float', 0.02),
            ('octaves', 'Octaves', 'int', 3)
        ]

    def generate(self, width, height, seed, **kwargs):
        np.random.seed(seed)
        theta = np.deg2rad(kwargs['direction'])
        rot_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        
        # 生成网格坐标系统（优化实现）
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 10, height)
        xx, yy = np.meshgrid(x, y)
        coords = np.stack([xx, yy], axis=-1)
        
        # 应用坐标变换
        stretched_coords = (coords @ rot_matrix) * [1, kwargs['stretch']]
        
        # 向量化噪声计算
        @np.vectorize
        def calc_noise(x, y):
            return snoise2(x * kwargs['frequency'],
                          y * kwargs['frequency'],
                          octaves=kwargs['octaves'])
        
        noise = calc_noise(stretched_coords[...,0], stretched_coords[...,1])
        return self.normalize(noise)
```
get_parameters中的返回值是一种固定的格式: (变量名称，变量在UI上显示的名称，变量类型，变量默认值)/
在generate中使用get_parameters中定义的变量采用: kwargs[变量名称] /
/
接下来你需要在register中注册这个噪声类型
```
引用这个类的地址
from .noise_type.anisotropic_noise import anisotropic_noise

加入noise_types数组中
noise_types = [
	...
	anisotropic_noise.AnisotropicNoise, 
	... 
	]
```
你不需要担心名称顺序混乱的问题，在generat中会有一个按名称字母排序的函数/
```
注册之后会有一个循环来自动注册所以噪声类
for noise_cls in noise_types:
    NoiseGenerator.register_noise(noise_cls.__name__.rsplit('Noise',1)[0], noise_cls)
```
- 增加一个新的保存格式
```
在这里按照格式增加即可
filetypes = [
	("PNG file", "*.png"), 
	("JPG file", "*.jpg"), 
	("TGA file", "*.tga"),
	("all files", "*.*")
	]
```
此项目是的图片保存是使用PIL库实现的，可以保存的格式的种类全都取决于PIL库。



### 欢迎纠正错误与贡献

- 因为这些噪声的生成方式都是在网络上找到的，我自己并不知道其中的噪声生成方式是否正确，所以欢迎纠正其中的错误。
- 这个项目还是存在不完善的地方，比如性能方面和DDS格式的保存还没有支持，所以欢迎贡献与修改。