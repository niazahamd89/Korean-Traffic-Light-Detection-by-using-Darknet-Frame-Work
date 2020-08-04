import os
import sys

sys.path.append(os.path.dirname(sys.argv[0]))
import load_dataset
import convert
import separate
import dataset_postprocessing

#load_dataset.main(global_path=os.path.dirname(sys.argv[0]), dataset_name='obj_detection')
#convert.main(global_path=os.path.dirname(sys.argv[0]), dataset_name='obj_detection')
#separate.main(global_path=os.path.dirname(sys.argv[0]))
#execution_path = os.path.dirname(sys.argv[0])
#print "the end!"
#print sys.argv[0]
#print sys.argv[2]

if sys.argv[2] == 'labeling':
    load_dataset.main(global_path=os.path.dirname(sys.argv[0]), dataset_name=sys.argv[1])
#elif sys.argv[2] == 'convert':
    convert.main(global_path=os.path.dirname(sys.argv[0]), dataset_name=sys.argv[1])
#elif sys.argv[2] == 'separate':
    separate.main(global_path=os.path.dirname(sys.argv[0]))

    dataset_postprocessing.main(global_path=os.path.dirname(sys.argv[0]), dataset_name='obj_detection', batch_size=64, subdivisions=8)