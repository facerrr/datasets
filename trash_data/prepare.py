import json
import os
from shutil import copyfile
def convert_coordinates(image_width, image_height, bbox):
    x, y, width, height = bbox
    x_center = (x + width / 2) / image_width
    y_center = (y + height / 2) / image_height
    new_width = width / image_width
    new_height = height / image_height
    return x_center, y_center, new_width, new_height

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def prepare(json_file, image_dir, label_dir):
    with open(json_file, 'r') as file:
        data = json.load(file)
    images = data['images']
    annotations = data['annotations']

    for image in images:
        image_id = image['id']
        image_width = image['width']
        image_height = image['height']
        image_file_name = image['file_name']
        image_file = os.path.join("images_ori/",image_file_name)
        

        if not os.path.exists(image_file):
            continue
        else:
            new_image_file = image_dir+str(image_id)+'.jpg'
            open(new_image_file, 'w') 
            copyfile(image_file, new_image_file)
            
        image_annotations = [annotation for annotation in annotations if annotation['image_id'] == image_id]
        yolo_file_name = str(image_id)
        yolo_file_name = os.path.join(label_dir,yolo_file_name)+'.txt'
        with open(yolo_file_name, 'w') as f:
            for annotation in image_annotations:
                category_id = annotation['category_id']-1
                bbox = annotation['bbox']
                x_center, y_center, width, height = convert_coordinates(image_width, image_height, bbox)
                yolo_line = f"{category_id} {x_center} {y_center} {width} {height}\n"
                f.write(yolo_line)

labels_dir = os.path.join("labels/")
if not os.path.isdir(labels_dir):
        os.mkdir(labels_dir)
train_label_dir = os.path.join(labels_dir,"train/")
if not os.path.isdir(train_label_dir):
        os.mkdir(train_label_dir)
clear_folder(train_label_dir)

val_label_dir = os.path.join(labels_dir,"val/")
if not os.path.isdir(val_label_dir):
        os.mkdir(val_label_dir)
clear_folder(val_label_dir)

image_dir = os.path.join("images/")
train_images_dir = os.path.join(image_dir,"train/")
if not os.path.isdir(train_images_dir):
        os.mkdir(train_images_dir)
clear_folder(train_images_dir)

val_images_dir = os.path.join(image_dir,"val/")
if not os.path.isdir(val_images_dir):
        os.mkdir(val_images_dir)
clear_folder(val_images_dir)

prepare('annotations/train.json',train_images_dir, train_label_dir)

prepare('annotations/val.json',val_images_dir, val_label_dir)
