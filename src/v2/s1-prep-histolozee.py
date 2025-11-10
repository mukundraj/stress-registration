"""Prepare images for loading into histolozee

Usage:

python script.py
    io: data root
    ip: file names list
    ip: gcp bucket folder with images
    op: output folder for processed images

Example:

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-3.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-3 \

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-9.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-9 \

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-13.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-13 \

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-14.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-14 \

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-16.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-16 \

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-22.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-22 \

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-23.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-23 \

python src/v2/s1-prep-histolozee.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s0-ippaths/ippaths-SA-24.txt \
    /v2/s1a-tmp \
    /v2/s1b/s1b-histolozee-SA-24 \

Supplementary:

mm activate allen

Created by Mukund on 2025-08-25
"""


# iterate over imgs; copy from bucket; convert; save to output folder
# downscale; make pyramidal tif; no alpha channel

# iterate over files in  ippaths.txt and print the lines
import os
import sys


data_root = sys.argv[1]
ippaths_file = f'{data_root}{sys.argv[2]}'
output_folder_tmp = f'{data_root}{sys.argv[3]}'
output_folder = f'{data_root}{sys.argv[4]}'

print(ippaths_file)

with open(ippaths_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            print(line)

            # get filename from line
            filename = os.path.basename(line)
            # get op file name
            op_path_name_tmp = f'{output_folder_tmp}/{filename}'
            print(op_path_name_tmp)

            # print resolution of image in line using vips
            cmd = f'vipsheader {line}'
            os.system(cmd)

            # print command to downsample by a factor of 4 using vips
            cmd = f'vips resize {line} {op_path_name_tmp} 0.0625'
            # cmd = f'vips resize {line} {op_path_name_tmp} 0.125'
            os.system(cmd)
            
            op_path_name = f'{output_folder}/{filename}'

            # convert op_path_name_tmp to pyramidal tif via vips
            cmd = f'vips tiffsave {op_path_name_tmp} {op_path_name} --tile --pyramid --compression=jpeg --Q=90 --tile-width=256 --tile-height=256 --bigtiff'
            os.system(cmd)

            cmd = f'vips tiffsave {op_path_name_tmp} {op_path_name} --tile --pyramid --compression deflate --tile-width 256 --tile-height 256'
            os.system(cmd)

