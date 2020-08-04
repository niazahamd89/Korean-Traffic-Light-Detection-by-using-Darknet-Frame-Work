import re
import os

num_classes = 0
classes_name = []

def modify_yolo_config(global_path, dataset_name, batch_size, subdivisions):
    go_to_imageDir = os.path.join(global_path + '/../../../dataset', dataset_name)
    for root, dirs, files in os.walk(go_to_imageDir):
        if(len(files) == 0):
            num_classes = len(dirs)
            for dir in dirs:
                classes_name.insert(len(classes_name), dir)

    new_lines = []
    yolo_file = open('%s/my-yolo-voc.2.0.cfg'%global_path, 'r')
    lines = yolo_file.readlines()
    lines = [x.strip() for x in lines]
    for line in lines:
        pattern = 'batch='
        prog = re.compile(pattern)
        if prog.match(line):
            line = 'batch=' + str(batch_size)
            new_lines.insert(len(new_lines), line)
            continue
        pattern = 'subdivisions='
        prog = re.compile(pattern)
        if prog.match(line):
            line = 'subdivisions=' + str(subdivisions)
            new_lines.insert(len(new_lines), line)
            continue
        pattern = 'classes='
        prog = re.compile(pattern)
        if prog.match(line):
            line = 'classes=' + str(num_classes)
            new_lines.insert(len(new_lines), line)
            continue
        new_lines.insert(len(new_lines), line)


    for i in range(0, len(lines)):
        line = lines[len(lines) - i - 1]
        pattern = 'filters='
        prog = re.compile(pattern)
        if prog.match(line):
            line = 'filters=' + str((num_classes+5)*5)
            new_lines[len(lines) - i - 1] = line
            break
        
    yolo_file.close()
    yolo_file = open('%s/my-yolo-voc.2.0.cfg'%global_path, 'w')
        
    for line in new_lines:
        yolo_file.write(line + '\n')

def create_obj_names(global_path):
    obj_name_file = open('%s/data/obj.names'% global_path, 'w')
    for class_name in classes_name:
        obj_name_file.write(class_name + '\n')

def create_obj_data(global_path):
    obj_data_file = open('%s/data/obj.data'% global_path, 'w')
    obj_data_file.write('classes = ' + str(len(classes_name)) + '\n')
    obj_data_file.write('train  = data/train.txt\n')
    obj_data_file.write('valid  = data/test.txt\n')
    obj_data_file.write('names = data/obj.names\n')
    obj_data_file.write('backup = backup/' + '\n')

def main(global_path, dataset_name, batch_size, subdivisions):
    modify_yolo_config(global_path=global_path, dataset_name=dataset_name, batch_size=batch_size, subdivisions=subdivisions)
    create_obj_names(global_path=global_path)
    create_obj_data(global_path=global_path)