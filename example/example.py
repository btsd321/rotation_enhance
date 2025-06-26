from rotation_enhance import rotation_enhance

test_imgs_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/images"
test_labels_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/labels"
test_output_folder = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/output"
test_angles_list = [10, 20, 30]
test_model_path = "D:/Project/all_data_5_r_rune_fitered/rotation_enhance/test/model/best.pt"
woker = rotation_enhance.RotationEnhance(imgs_folder = test_imgs_folder, 
                        labels_folder = test_labels_folder, 
                        output_folder = test_output_folder, 
                        angles_list = test_angles_list,
                        model_path = test_model_path)
woker.run()