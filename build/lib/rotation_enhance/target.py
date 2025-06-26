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
        return (f"Target(\n\tclass_id={self.class_id}, \n\tx_center={self.x_center}, \n\ty_center={self.y_center}, "
                f"\n\tbox_w={self.box_w}, \n\tbox_h={self.box_h}, \n\tkeypoints_num={self.keypoints_num}, "
                f"\n\tkeypoints={self.keypoints})\n")
        
    def __repr__(self):
        return self.__str__()
    
    def is_matched(self, other, distance_threshold=0.03):
        if not isinstance(other, Target):
            return False
        else:
            if self.class_id != other.class_id:
                return False
            distance = ((self.x_center - other.x_center) ** 2 + (self.y_center - other.y_center) ** 2) ** 0.5
            if distance > distance_threshold:
                return False
            return True