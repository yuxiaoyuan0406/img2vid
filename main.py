from asyncore import write
import numpy as np
import cv2
import os
import sys
import argparse


def main(opt: argparse.Namespace):
    img_dir:str = opt.input
    vid_dir:str = opt.output

    img_list = os.listdir(img_dir)
    assert len(img_list), 'no file in directory: {}'.format(img_dir)
    if(opt.sort_by_name):
        def sort_by_name(name: str):
            return int(name.split('.')[0])
        img_list.sort(key=sort_by_name)
    print('{} image(s) found'.format(len(img_list)))

    # get image shape
    _ = cv2.imread(os.path.join(img_dir, img_list[0]))
    img_shape = _.shape
    print('image shape: {}'.format(img_shape))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # vc2.Mat.shape is a tuple like ( height, width, channel )
    # but a cv2.VideoWriter take a tuple as ( width, height )
    # so reverse a tuple by [::-1] and take the last 2 elements by [-2::]
    writer = cv2.VideoWriter(vid_dir, fourcc, opt.fps, img_shape[::-1][-2::])

    for img in img_list:
        _ = cv2.imread(os.path.join(img_dir, img))
        writer.write(_)
    writer.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='/home/dennis/Program/ROLO/benchmark/DATA/BlurBody/img', help='source images')
    parser.add_argument('--output', type=str, default='./out.mp4', help='output file')
    parser.add_argument('--fps', type=int, default=60, help='video fps')
    parser.add_argument('--sort-by-name', action='store_true', help='sort images by file name')
    opt = parser.parse_args()

    assert os.path.isdir(opt.input), 'require a directory: {}'.format(opt.input)
    assert os.path.exists(opt.input), 'no such directory: {}'.format(opt.input)

    output_path, _ = os.path.split(opt.output)
    assert _ != '', 'need a file name for output'
    if os.path.exists(output_path):
        pass
    else:
        os.makedirs(output_path)
    
    assert opt.fps > 0, 'fps must be larger than 0'

    main(opt)
