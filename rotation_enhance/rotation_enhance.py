


class RotationEnhance:
    """
    RotationEnhance class 构造函数
    输入：
        imgs_path: 原始图像文件夹路径
        labels_path: 原始标签文件夹路径
        output_path: 输出文件夹路径
        angles_list: 旋转角度列表, 需要旋转的角度值列表
        model_path: 模型路径，暂时只支持.pt文件类型
    """
    def __init__(self, imgs_path=None, labels_path=None, output_path=None, angles_list=None,model_path=None):
        self.imgs_path = imgs_path
        self.labels_path = labels_path
        self.output_path = output_path
        self.angles_list = angles_list
        self.model_path = model_path
        if self.imgs_path is None:
            raise ValueError("imgs_path cannot be None")
        if self.labels_path is None:
            raise ValueError("labels_path cannot be None")
        if self.output_path is None:
            raise ValueError("output_path cannot be None")
        if self.angles_list is None:
            raise ValueError("angles_list cannot be None")
        if self.model_path is None:
            raise ValueError("model_path cannot be None")
        
    def run(self):
        pass
    
    
if __name__ == '__main__':
    test_imgs_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/images"
    test_labels_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/labels"
    test_output_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/output"
    test_angles_list = [10, 20, 30]
    test_model_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/model/best.pt"
    rotation_enhance = RotationEnhance(imgs_path = test_imgs_path, 
                                        labels_path = test_labels_path, 
                                        output_path = test_output_path, 
                                        angles_list = test_angles_list,
                                        model_path = test_model_path)
    rotation_enhance.run()