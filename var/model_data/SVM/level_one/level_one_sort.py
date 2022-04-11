import os
import shutil
import sys

classifications = ['empty', 'puck']
base_dir = os.getcwd()

# Moving the images into the training and testing directories
for image_class in classifications:
    class_path = os.path.join(base_dir, image_class)
    my_files = [f for f in os.listdir(class_path)]
    
    sort_limit_train = (len(my_files) // 3) * 2
    sort_limit_test = len(my_files)

    train_dir = os.path.join(base_dir, 'train')
    target_train_dir = os.path.join(train_dir, image_class)

    test_dir = os.path.join(base_dir, 'test')
    target_test_dir = os.path.join(test_dir, image_class)

    for i in range(sort_limit_train):
        current_image = os.path.join(class_path, my_files[i])
        shutil.move(current_image, target_train_dir)

    for i in range(sort_limit_train, sort_limit_test):
        current_image = os.path.join(class_path, my_files[i])
        shutil.move(current_image, target_test_dir)