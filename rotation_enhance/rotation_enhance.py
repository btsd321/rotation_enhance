import os
import cv2


class RotationEnhance:
    """
    RotationEnhance class 构造函数
    输入：
        imgs_folder: 原始图像文件夹路径
        labels_folder: 原始标签文件夹路径
        output_folder: 输出文件夹路径
        angles_list: 旋转角度列表, 需要旋转的角度值列表，顺时针为正，逆时针为负
        model_path: 模型路径，暂时只支持.pt文件类型
    """
    def __init__(self, imgs_folder=None, labels_folder=None, output_folder=None, angles_list=None,model_path=None):
        self.imgs_folder = imgs_folder
        self.labels_folder = labels_folder
        self.output_folder = output_folder
        self.angles_list = angles_list
        self.model_path = model_path
        if self.imgs_folder is None:
            raise ValueError("imgs_folder cannot be None")
        else:
            if not os.path.exists(self.imgs_folder):
                raise ValueError(f"imgs_folder does not exist: {self.imgs_folder}")

        if self.labels_folder is None:
            raise ValueError("labels_folder cannot be None")
        else:
            if not os.path.exists(self.labels_folder):
                raise ValueError(f"labels_folder does not exist: {self.labels_folder}")
            else:
                # 尝试解析标签文件，获取关键点个数
                
        if self.output_folder is None:
            raise ValueError("output_folder cannot be None")
        else:
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
        if self.angles_list is None:
            raise ValueError("angles_list cannot be None")
        else:
            # 删除0度旋转
            for angle in self.angles_list:
                if angle == 0:
                    self.angles_list.remove(angle)
        if self.model_path is None:
            raise ValueError("model_path cannot be None")
        else:
            if not os.path.exists(self.model_path):
                raise ValueError(f"model does not exist: {self.model_path}")
        
    def run(self):
        # 遍历原始图像文件夹
        for img in os.listdir(self.imgs_folder):
            img_path = os.path.join(self.imgs_folder, img)
            try:
                read_img = cv2.imread(img_path)
                cv2.imshow("read_img", read_img)
                cv2.waitKey(0)
            except Exception as e:
                print(f"read image error: {img_path}, {e}")
                continue
            
            
    
    
if __name__ == '__main__':
    test_imgs_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/images"
    test_labels_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/labels"
    test_output_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/output"
    test_angles_list = [10, 20, 30]
    test_model_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/model/best.pt"
    rotation_enhance = RotationEnhance(imgs_folder = test_imgs_folder, 
                                        labels_folder = test_labels_folder, 
                                        output_folder = test_output_folder, 
                                        angles_list = test_angles_list,
                                        model_path = test_model_path)
    rotation_enhance.run()