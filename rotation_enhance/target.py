from point import Point

class Target:
    def __init__(self, class_id=0, x_center=0, y_center=0, box_w=0, box_h=0, keypoints_num=0, keypoints=[]):
        self.class_id = class_id
        self.x_center = x_center
        self.y_center = y_center
        self.box_w = box_w
        self.box_h = box_h
        self.keypoints_num = keypoints_num
        self.keypoints = keypoints
        
    def __str__(self):
        return (f"Target(class_id={self.class_id}, x_center={self.x_center}, y_center={self.y_center}, "
                f"box_w={self.box_w}, box_h={self.box_h}, keypoints_num={self.keypoints_num}, "
                f"keypoints={self.keypoints})")