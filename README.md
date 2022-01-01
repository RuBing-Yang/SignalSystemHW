# SignalSystemHW
信号与系统大作业

图像频域变换+压缩+解压

[toc]

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



### 运行方式

直接运行`main.py`
