from ultralytics import YOLO
from PIL import Image
from .target import Target
from .point import Point


# # 对单张图片进行推理并可视化结果
# model = YOLO("runs/pose/train/weights/best.pt")  # build from YAML and transfer weights
# results = model(["dataset/images/test/20250327_175217_rMC5cmNa.jpg"])  # return a list of Results objects

# # Process results list
# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     # result.show()  # display to screen
#     result.save(filename="result.jpg")  # save to disk
#     # 打印 boxes, masks, keypoints, probs, obb 信息
#     print("boxes: ", boxes)
#     print("masks: ", masks)
#     print("keypoints: ", keypoints)
#     print("probs: ", probs)
#     print("obb: ", obb)

def get_yolo_predicted_targets(img, model, conf=0.6, iou=0.5, agnostic_nms=False):
    results = model.predict(img, conf = conf, iou = iou, agnostic_nms = agnostic_nms)  # return a list of Results objects
    targets = []
    for result in results:
        boxes = result.boxes  # Boxes object
        keypoints = result.keypoints  # Keypoints object
        classes = boxes.cls.cpu().numpy() if boxes is not None else []
        xywhn = boxes.xywhn.cpu().numpy() if boxes is not None else []
        scores = boxes.conf.cpu().numpy() if boxes is not None else []
        kpts = keypoints.xyn.cpu().numpy() if keypoints is not None else []

        for i in range(len(xywhn)):
            x,y, w, h = xywhn[i]
            cur_class_id = int(classes[i])
            cur_box_w = w
            cur_box_h = h
            cur_x_center = x
            cur_y_center = y

            # 关键点
            cur_keypoints_list = []
            if len(kpts) > i:
                for kp in kpts[i]:
                    kp_x, kp_y = kp
                    cur_keypoints_list.append(Point(kp_x, kp_y))

            target = Target(
                class_id=cur_class_id,
                x_center=cur_x_center,
                y_center=cur_y_center,
                box_w=cur_box_w,
                box_h=cur_box_h,
                keypoints_num=len(cur_keypoints_list),
                keypoints=cur_keypoints_list
            )
            targets.append(target)
    return targets, scores

# if __name__ == "__main__":
#     model = YOLO("D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/model/best.pt")  # build from YAML and transfer weights
#     img = Image.open("D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/images/1.png")
#     targets, scores = get_yolo_predicted_targets(img, model)
#     print(targets)
#     print(scores)