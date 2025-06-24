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
            
            self.targets.append(new_target)
        except Exception as e:
            print(f"Error parsing line: {line}. Error: {e}")
            
    def __str__(self):
        targets_str = ', '.join(str(target) for target in self.targets)
        class_num = self.get_class_num()
        return f"LabelInfo(class_num={class_num}, targets=[{targets_str}])"
        
    def get_class_num(self):
        """
        获取标签中类别的数量
        :return: 类别数量
        """
        return len(self.class_id_list)
    
if __name__ == '__main__':
    label_info = LabelInfo()
    label_info.read_from_txt('D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/labels/1.txt')
    print(label_info)
    
        