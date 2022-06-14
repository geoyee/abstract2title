# 后端

本项目后端采用FastAPI，标题生成能力由PaddleNLP提供。启动方法如下：

1. 首先需要在本环境中安装最新版的PaddlePaddle-GPU：
   
   ```shell
   python -m pip install paddlepaddle-gpu==2.3.0 -i https://mirror.baidu.com/pypi/simple
   ```

2. 安装所需要的其他库：
   
   ```shell
   pip install -r requirements.txt
   ```

3. 下载预训练的模型参数。该模型由10k+来自知网空间的“测绘、遥感、GIS”论文训练，下载地址为[百度网盘]()。下载后将该压缩包解压至`backend/weight`中即可。

4. 启动后端：
   
   ```shell
   python app\main.py
   ```
