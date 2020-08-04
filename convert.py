# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015

This script is to convert the txt annotation files to appropriate format needed by YOLO 

@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import os
from os import walk, getcwd
from PIL import Image
import distutils.file_util


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    

def main(global_path, dataset_name):
    classes = []
    wd = getcwd()
    list_file = open('%s/data/all_list.txt'%global_path, 'w')
    if not os.path.exists(global_path + '/data/obj'):
       os.makedirs(global_path + '/data/obj')
    for root, dirs, files in os.walk(global_path + '/../../../dataset/' + dataset_name + '_label/' ):
        if(len(files) == 0):
            for className in dirs:
                classes.insert(len(classes), className)
        else:
            #print classes
            cls = os.path.basename(root)
            cls_id = classes.index(cls)
            """ Configure Paths"""   
            mypath = global_path + '/../../../dataset/' + dataset_name + '_label/'+ cls + "/"
            outpath = global_path + "/data/obj/"
            """ Get input text file list """
            txt_name_list = []
            txt_name_list.extend(files)
            print(txt_name_list)
    
            """ Process """
            for txt_name in txt_name_list:
                # txt_file =  open("Labels/stop_sign/001.txt", "r")
                
                """ Open input text files """
                txt_path = mypath + txt_name
                print("Input:" + txt_path)
                txt_file = open(txt_path, "r")
                lines = txt_file.readlines()   #for ubuntu, use "\r\n" instead of "\n"
                lines = [x.strip() for x in lines]
                
                """ Open output text files """
                txt_outpath = outpath + txt_name
                print("Output:" + txt_outpath)
                txt_outfile = open(txt_outpath, "w")
                #for line in lines:
                #    print(line)
                
                
                """ Convert the data to YOLO format """
                ct = 0
                for line in lines:
                    #print('lenth of line is: ')
                    print(line)
                    #print('\n')
                    if(len(line) >= 2):
                        ct = ct + 1
                        #print(line + "\n")
                        elems = line.split(' ')
                        print(elems)
                        if len(elems) < 2:
                            continue
                        xmin = elems[0]
                        xmax = elems[2]
                        ymin = elems[1]
                        ymax = elems[3]
                        #
                        img_path = str('%s%s.JPG'%(global_path + '/../../../dataset/' + dataset_name + '/'+ cls + '/', os.path.splitext(txt_name)[0]))
                        #t = magic.from_file(img_path)
                        #wh= re.search('(\d+) x (\d+)', t).groups()
                        im=Image.open(img_path)
                        w= int(im.size[0])
                        h= int(im.size[1])
                        #w = int(xmax) - int(xmin)
                        #h = int(ymax) - int(ymin)
                        # print(xmin)
                        print(w, h)
                        print(str(xmin))
                        print(float(xmax))
                        print(float(ymin))
                        print(float(ymax))
            		
                        b = (float(xmin), float(xmax), float(ymin), float(ymax))
                        bb = convert((w,h), b)
                        #print(bb)
                        txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                image_file = os.path.split(txt_name)[-1].split('.')[0]
                image_file = image_file + '.jpg'
                distutils.file_util.copy_file(global_path + '/../../../dataset/' + dataset_name + '/'+ cls + '/' + image_file, outpath)
                        
                """ Save those images with bb into list"""
                if(ct != 0):
                    list_file.write('%s/%s.JPEG\n'%(global_path + '/../../../dataset/' + dataset_name + '/'+ cls + '/', os.path.splitext(txt_name)[0]))
                    
    list_file.close()
    