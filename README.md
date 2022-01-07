# SignalSystemHW
信号与系统大作业

图像频域变换+压缩+解压

[toc]

## Cython

[Python调用C++](https://zhuanlan.zhihu.com/p/74219095)



## 更改内容

### 封装Python

将`encode.py`和`decode.py`封装到同一个类`helper`中

调用方法：

```python
from helper import helper
# 创建类实例，初始化输入、输出图片和编码文件名
helper = helper("images/image.bmp", "encode.txt", "images/out.bmp")
# encode
helper.encode_from_img()
# decode
helper.decode_to_img()
```

### 封装C++

在`/SignalSystemHW/cython/Huffman.cpp`文件中是用C++写的哈夫曼编码API

**TODO**：de huffman

利用Cython封装成`rect.PyHuffman`类，在cython文件夹下命令行运行：

```
python setup.py build_ext --inplace
```

生成的动态链接库文件名为`rect.cp39-win_amd64.pyd`，需要与调用方python入口文件放在同一文件夹下



## 运行方式

直接运行`/SignalSystemHW/main.py`

输入文件：`/SignalSystemHW/images/image.bmp`

python的编码文件：`/SignalSystemHW/encode.txt`

c++的哈夫曼编码文件：`/SignalSystemHW/huffman.txt`

ps：建议在visual studio运行（但是vs需要装python拓展，得挂梯子）
