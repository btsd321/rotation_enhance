针对YOLO-POSE数据集(无遮挡)的旋转增强库

输入：原始图片文件夹路径，原始标签文件路径，预训练模型路径（用于标记新的box），输出文件夹路径，增强参数
要求：标签必须符合YOLO-POSE(无遮挡)的标签格式即： class_id x_center y_center width height x1 y1 x2 y2 x3 y3 ... xn yn

输出：输出文件夹中将会生成旋转增强后的图片文件夹和标签文件夹