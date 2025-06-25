import os
import cv2
import numpy as np
from point import Point
from target import Target
from label_info import LabelInfo


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
        self.class_id_list = []
        self.keypoints_num = 0
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
                # 尝试解析标签文件，获取关键点个数，类别个数
                try:
                    for label in os.listdir(self.labels_folder):
                        label_path = os.path.join(self.labels_folder, label)
                        cur_label_info = LabelInfo()
                        cur_label_info.read_from_txt(label_path)
                        if len(cur_label_info.targets) > 0:
                            if self.keypoints_num == 0:
                                self.keypoints_num = cur_label_info.targets[0].keypoints_num
                            for target in cur_label_info.targets:
                                if target.class_id not in self.class_id_list:
                                    self.class_id_list.append(target.class_id)
                except Exception as e:
                    raise ValueError(f"Error reading labels: {e}")
                
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
        if self.keypoints_num == 0:
            raise ValueError("keypoints_num cannot be 0, please check your labels")
        if len(self.class_id_list) == 0:
            raise ValueError("class_id_list cannot be empty, please check your labels")
        
    def run(self):
        # 遍历原始图像文件夹
        origin_imgs = []
        rotated_imgs = []
        for img_file_name in os.listdir(self.imgs_folder):
            img_path = os.path.join(self.imgs_folder, img_file_name)
            try:
                img = cv2.imread(img_path)
                # cv2.imshow("read_img", img)
                # cv2.waitKey(0)
                origin_imgs.append(img)
                
                # 获取label文件夹中同名的标签文件
                label_file_name = img_file_name.split('.')[0] + '.txt'
                origin_label_path = os.path.join(self.labels_folder, label_file_name)
                if not os.path.exists(origin_label_path):
                    print(f"label file does not exist: {origin_label_path}")
                    raise ValueError(f"label file does not exist: {origin_label_path}")
                
                # 读取标签文件
                cur_label_info = LabelInfo()
                cur_label_info.read_from_txt(origin_label_path)
                # 可视化原始标签信息，调试用
                # self.visualize_label_info(img, cur_label_info)
                
                if not os.path.exists(os.path.join(self.output_folder, 'image')):
                        os.makedirs(os.path.join(self.output_folder, 'image'))
                if not os.path.exists(os.path.join(self.output_folder, 'label')):
                        os.makedirs(os.path.join(self.output_folder, 'label'))
                
                for angle in self.angles_list:
                    (rotated_img, M) = self.__rotate_image(img, angle)
                    rotated_img_file_name = self.__get_rotated_img_file_name(img_file_name, angle)
                    rotated_img_path = os.path.join(self.output_folder, 'image', rotated_img_file_name)
                    cv2.imwrite(rotated_img_path, rotated_img)
                    rotated_imgs.append(rotated_img)
                    
                    rotated_targets = self.__get_rotated_targets(cur_label_info.targets, M, angle, rotated_img.shape[1], rotated_img.shape[0], rotated_img.shape[1], rotated_img.shape[0])
                    rotated_label_info = LabelInfo()
                    rotated_label_info.targets = rotated_targets
                    rotated_label_info.class_id_list = cur_label_info.class_id_list
                    # 可视化旋转后的标签信息，调试用
                    #self.visualize_label_info(rotated_img, rotated_label_info)
                    rotated_label_file_name = self.__get_rotated_label_file_name(label_file_name, angle)
                    rotated_label_path = os.path.join(self.output_folder, 'label', rotated_label_file_name)
                    rotated_label_info.write_to_txt(rotated_label_path)
                

            except Exception as e:
                print(f"read image error: {img_path}, {e}")
                continue
            
    def __get_rotated_img_file_name(self, img_file_name, angle):
        rotated_img_file_name = ''
        if angle > 0:
            rotated_img_file_name = img_file_name.split('.')[0] + 's' + f'_{angle}.png'
        else:
            rotated_img_file_name = img_file_name.split('.')[0] + 'u' + f'_{abs(angle)}.png'
        return rotated_img_file_name
    
    def __get_rotated_label_file_name(self, label_file_name, angle):
        rotated_label_file_name = ''
        if angle > 0:
            rotated_label_file_name = label_file_name.split('.')[0] + 's' + f'_{angle}.txt'
        else:
            rotated_label_file_name = label_file_name.split('.')[0] + 'u' + f'_{abs(angle)}.txt'
        return rotated_label_file_name
    
    def __rotate_image(self, img, angle):
        # 获取图像的中心
        (h, w) = img.shape[:2]
        center = (w / 2, h / 2)

        # 计算旋转矩阵
        M = cv2.getRotationMatrix2D(center, angle, 1.0)  # 最后一个参数是缩放因子
        
        # 从旋转矩阵中提取旋转角度和缩放因子
        angle_rad = np.deg2rad(angle)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # 计算新图像的边界
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        # 调整旋转矩阵以适应新的边界
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        
        # 应用旋转矩阵到图像上
        rotated_image = cv2.warpAffine(img, M, (new_w, new_h))
        cv2.imshow("Rotated Image", rotated_image)
        cv2.waitKey(0)
        return (rotated_image, M)
    
    def __get_rotated_point(self, M, x, y):
        # 将点转换为齐次坐标形式
        point = np.array([x, y, 1])
        
        # 使用旋转矩阵对点进行变换
        rotated_point = M @ point
        
        # 将变换后的齐次坐标转换回普通坐标形式
        rotated_x = rotated_point[0]
        rotated_y = rotated_point[1]
        
        return (rotated_x, rotated_y)
    
    def __get_rotated_targets(self, targets, M, angle, img_w, img_h, rotated_img_w, rotated_img_h):
        rotated_targets = []
        if len(targets) == 0:
            return rotated_targets
        for target in targets:
            rotated_target_class_id = target.class_id
            rotated_keypoints = []
            (rotated_target_x_center, rotated_target_y_center) = self.__get_rotated_point(M, target.x_center * img_w, target.y_center * img_h)
            rotated_target_x_center /= rotated_img_w
            rotated_target_y_center /= rotated_img_h
            for keypoint in target.keypoints:
                (rotated_keypoint_x, rotated_keypoint_y) = self.__get_rotated_point(M, keypoint.x * img_w, keypoint.y * img_h)
                rotated_keypoint_x /= rotated_img_w
                rotated_keypoint_y /= rotated_img_h
                rotated_keypoint = Point(rotated_keypoint_x, rotated_keypoint_y)
                rotated_keypoints.append(rotated_keypoint)
                
            target_box_point1_x = target.x_center - target.box_w / 2
            target_box_point1_y = target.y_center - target.box_h / 2
            target_box_point2_x = target.x_center + target.box_w / 2
            target_box_point2_y = target.y_center - target.box_h / 2
            target_box_point3_x = target.x_center + target.box_w / 2
            target_box_point3_y = target.y_center + target.box_h / 2
            target_box_point4_x = target.x_center - target.box_w / 2
            target_box_point4_y = target.y_center + target.box_h / 2
            
            rotated_target_box_point1_x, rotated_target_box_point1_y = self.__get_rotated_point(M, target_box_point1_x * img_w, target_box_point1_y * img_h)
            rotated_target_box_point2_x, rotated_target_box_point2_y = self.__get_rotated_point(M, target_box_point2_x * img_w, target_box_point2_y * img_h)
            rotated_target_box_point3_x, rotated_target_box_point3_y = self.__get_rotated_point(M, target_box_point3_x * img_w, target_box_point3_y * img_h)
            rotated_target_box_point4_x, rotated_target_box_point4_y = self.__get_rotated_point(M, target_box_point4_x * img_w, target_box_point4_y * img_h)

            min_x = min(rotated_target_box_point1_x, rotated_target_box_point2_x, rotated_target_box_point3_x, rotated_target_box_point4_x)
            min_y = min(rotated_target_box_point1_y, rotated_target_box_point2_y, rotated_target_box_point3_y, rotated_target_box_point4_y)
            max_x = max(rotated_target_box_point1_x, rotated_target_box_point2_x, rotated_target_box_point3_x, rotated_target_box_point4_x)
            max_y = max(rotated_target_box_point1_y, rotated_target_box_point2_y, rotated_target_box_point3_y, rotated_target_box_point4_y)
            rotated_target_box_w = (max_x - min_x) / rotated_img_w
            rotated_target_box_h = (max_y - min_y) / rotated_img_h
            rotated_target = Target(rotated_target_class_id, rotated_target_x_center, rotated_target_y_center, rotated_target_box_w, rotated_target_box_h, rotated_keypoints)
            rotated_targets.append(rotated_target)
        return rotated_targets
    
    def visualize_label_info(self, img, label_info):
        # 在img上可视化标签信息
        if label_info is None:
            raise ValueError("label_info cannot be None")
        if len(label_info.targets) == 0:
            print("No targets to visualize.")
            # 显示图像（可选）
            cv2.imshow("Visualized Image", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return
        for target in label_info.targets:
            # 1. 可视化box
            (h, w) = img.shape[:2]
            x_center = target.x_center * w
            y_center = target.y_center * h
            box_w = target.box_w * w
            box_h = target.box_h * h

            # 计算边界框的左上角和右下角坐标
            x_min = int(x_center - box_w / 2)
            y_min = int(y_center - box_h / 2)
            x_max = int(x_center + box_w / 2)
            y_max = int(y_center + box_h / 2)

            # 绘制边界框
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # 2. 可视化关键点（可选）
            for keypoint in target.keypoints:
                kx = int(keypoint.x * w)
                ky = int(keypoint.y * h)
                cv2.circle(img, (kx, ky), 3, (255, 0, 0), -1)

        # 显示图像（可选）
        cv2.imshow("Visualized Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
            
            
            
            
    
    
if __name__ == '__main__':
    test_imgs_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/images"
    test_labels_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/labels"
    test_output_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/output"
    test_angles_list = [10, 20, 30]
    test_model_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/model/best.pt"
    woker = RotationEnhance(imgs_folder = test_imgs_folder, 
                            labels_folder = test_labels_folder, 
                            output_folder = test_output_folder, 
                            angles_list = test_angles_list,
                            model_path = test_model_path)
    woker.run()