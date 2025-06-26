import os
from target import Target
from point import Point

class LabelInfo:
    def __init__(self):
        self.class_id_list = []
        self.targets = []
        
    def read_from_txt(self, label_path):
        """
        从文本文件中读取标签信息
        :param label_path: 标签文件路径
        """
        with open(label_path, 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            self._parse_line(line.strip())
            
    def write_to_txt(self, label_path):
        """
        将标签信息写入文本文件
        :param label_path: 标签文件路径
        """
        if label_path is None:
            raise ValueError("label_path cannot be None")
        if os.path.exists(label_path):
            os.remove(label_path)
        if os.path.dirname(label_path) != '':
            os.makedirs(os.path.dirname(label_path), exist_ok=True)
        with open(label_path, 'w') as file:
            for target in self.targets:
                file.write(f"{target.class_id} {target.x_center} {target.y_center} "
                           f"{target.box_w} {target.box_h} ")
                for keypoint in target.keypoints:
                    file.write(f"{keypoint.x} {keypoint.y} ")
                # 去除最后的空格
                file.seek(file.tell() - 1, os.SEEK_SET)
                file.write("\n")

    def _parse_line(self, line):
        """
        解析单行标签信息
        :param line: 单行标签字符串
        """
        try:
            parts = line.split()
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            # 循环读取两个小数构造关键点
            keypoints = []
            for i in range(5, len(parts), 2):
                x = float(parts[i])
                y = float(parts[i+1])
                keypoints.append(Point(x, y))
            
            
            new_target = Target(class_id, x_center, y_center, width, height, len(keypoints), keypoints)
            if class_id not in self.class_id_list:
                self.class_id_list.append(class_id)
            self.targets.append(new_target)
        except Exception as e:
            print(f"Error parsing line: {line}. Error: {e}")
            
    def __str__(self):
        targets_str = '\n\t'.join(str(target) for target in self.targets)
        return f"LabelInfo(\ntargets=[\n\t{targets_str}])"
    
    def __repr__(self):
        return self.__str__()
    
if __name__ == '__main__':
    label_info = LabelInfo()
    label_info.read_from_txt('D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/labels/1.txt')
    print(label_info)
    
        