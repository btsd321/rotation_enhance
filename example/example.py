from rotation_enhance import rotation_enhance

# 原始图片集路径
test_imgs_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/images"
# 原始标签集路径
test_labels_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/labels"
# 输出路径
test_output_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/output"
# 旋转角度列表，可正可负，角度制
test_angles_list = [10, 20, 30]
# 预训练模型路径，暂时只支持pt格式
test_model_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/model/best.pt"

# 创建并运行 RotationEnhance 实例
woker = rotation_enhance.RotationEnhance(imgs_folder = test_imgs_folder, 
                        labels_folder = test_labels_folder, 
                        output_folder = test_output_folder, 
                        angles_list = test_angles_list,
                        model_path = test_model_path)
woker.run()