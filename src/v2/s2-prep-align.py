"""Prepare images for alignment pipeline

Usage:

python script.py
    io: data root
    ip: histolozee export folder
    ip: atlas images folder
    op: output folder for transformed atlas images
    op: output folder for transformed histolozee export images

Example:

python src/v2/s2-prep-align.py \
    ~/Desktop/work/data/stress-atlas \
    /v2/s1b-histolozee/exports \
    /v2/s0-atlas-nissls/nissls \
    /v2/s2-slicer/atlas \
    /v2/s2-slicer/histolozee

Supplementary:

mm activate allen

Created by Mukund on 2025-08-26
"""

import os
import sys
import glob

# Parse command line arguments
data_root = sys.argv[1]
histolozee_input_folder = f'{data_root}{sys.argv[2]}'
atlas_input_folder = f'{data_root}{sys.argv[3]}'
atlas_output_folder = f'{data_root}{sys.argv[4]}'
histolozee_output_folder = f'{data_root}{sys.argv[5]}'

print(f"Data root: {data_root}")
print(f"Histolozee input folder: {histolozee_input_folder}")
print(f"Atlas input folder: {atlas_input_folder}")
print(f"Atlas output folder: {atlas_output_folder}")
print(f"Histolozee output folder: {histolozee_output_folder}")

# Create output folders if they don't exist
os.makedirs(atlas_output_folder, exist_ok=True)
os.makedirs(histolozee_output_folder, exist_ok=True)

def process_images(input_folder, output_folder, folder_type):
    """Process images from input folder and save to output folder"""
    print(f"\n=== Processing {folder_type} images ===")
    
    # Find all image files in input folder (common formats)
    image_extensions = ['*.tif', '*.tiff', '*.png', '*.jpg', '*.jpeg']
    image_files = []

    for ext in image_extensions:
        pattern = os.path.join(input_folder, '**', ext)
        image_files.extend(glob.glob(pattern, recursive=True))

    print(f"Found {len(image_files)} {folder_type} image files")

    # Process each image file
    for img_path in image_files:
        filename = os.path.basename(img_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{name_without_ext}.png")
        
        print(f"Processing: {filename}")
        
        # Check if image has alpha channel using vipsheader
        cmd = f'vipsheader -f bands {img_path}'
        bands_result = os.popen(cmd).read().strip()
        
        try:
            num_bands = int(bands_result)
            has_alpha = num_bands == 4  # RGBA
            print(f"  Bands: {num_bands}, Has alpha: {has_alpha}")
        except ValueError:
            print(f"  Warning: Could not determine number of bands for {filename}")
            has_alpha = False
        
        # Build vips command to convert image
        # Remove alpha channel if present and convert to PNG format
        if has_alpha:
            # Extract RGB channels (remove alpha) - extract first 3 bands
            cmd = f'vips extract_band {img_path} {output_path} 0 --n 3'
        else:
            # Convert to PNG format
            cmd = f'vips pngsave {img_path} {output_path}'
        
        print(f"  Command: {cmd}")
        result = os.system(cmd)
        
        if result == 0:
            print(f"  ✓ Successfully processed: {filename}")
        else:
            print(f"  ✗ Failed to process: {filename}")

# Process both sets of images
process_images(histolozee_input_folder, histolozee_output_folder, "histolozee")
process_images(atlas_input_folder, atlas_output_folder, "atlas")

print("\nProcessing complete!")
