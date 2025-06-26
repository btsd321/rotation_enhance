针对YOLO-POSE数据集(无遮挡)的旋转增强库

输入：原始图片文件夹路径，原始标签文件路径，预训练模型路径（用于标记新的box），输出文件夹路径，增强参数
要求：
    1. 图片要求为png格式，标签要求为txt格式
    2. 标签必须符合YOLO-POSE(无遮挡)的标签格式即： class_id x_center y_center width height x1 y1 x2 y2 x3 y3 ... xn yn
    3. 输入文件夹中图片文件名必须与标签文件名一一对应

输出：输出文件夹中将会生成旋转增强后的图片文件夹和标签文件夹

使用方法：
    1. 在根目录下clone本库代码到本地，即运行命令：git clone https://github.com/btsd321/rotation_enhance.git
    2. 运行命令：cd rotation_enhance，再运行命令：pip install -e . 进行安装
    3.参考rotation_enhance/example/example.py文件，在根目录下编写自己的代码，调用rotate_enhance函数进行旋转增强
