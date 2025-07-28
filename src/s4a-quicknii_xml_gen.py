"""Generate quick nii input xml file from post histology alignmed pngs

Usage:

python script.py
    ip: path to input images

Example:

python src/s4a-quicknii_xml_gen.py \
    ~/Desktop/work/data/stress-atlas/v1/s3-mspace-pngs/

Env:
rpymain_lin

Created by Mukund on 2025-07-28
"""


import os
import re
import glob
import argparse
from xml.etree.ElementTree import Element, SubElement, ElementTree
from PIL import Image

class QuickNIIXMLGenerator:
    def __init__(self):
        self.supported_extensions = ['.jpg', '.jpeg', '.png']

    def extract_section_number(self, filename):
        # Extract numeric part from filename using regex
        match = re.search(r'(\d+)', filename)
        if match:
            return int(match.group(1))
        else:
            return None

    def get_image_files(self, directory):
        image_files = []
        for ext in self.supported_extensions:
            image_files.extend(glob.glob(os.path.join(directory, f'*{ext}')))
        return image_files

    def get_image_size(self, filepath):
        try:
            with Image.open(filepath) as img:
                return img.size  # returns (width, height)
        except Exception as e:
            print(f"Error reading image size of {filepath}: {e}")
            return (0, 0)

    def create_xml_descriptor(self, image_directory, output_path=None, series_name="Brain Image Series"):
        image_directory = os.path.abspath(image_directory)
        image_files = self.get_image_files(image_directory)

        if not image_files:
            raise ValueError("No supported image files found in the directory.")

        # Extract section numbers and sort
        image_info = []
        for file_path in image_files:
            filename = os.path.basename(file_path)
            sec_num = self.extract_section_number(filename)
            if sec_num is None:
                print(f"Skipping file without section number: {filename}")
                continue
            width, height = self.get_image_size(file_path)
            image_info.append((sec_num, filename, width, height))

        if not image_info:
            raise ValueError("No valid section images with numeric identifiers found.")

        # Sort image list by section number
        image_info.sort(key=lambda x: x[0])

        # Build XML structure
        root = Element('series')
        root.set('name', series_name)

        for sec_num, filename, width, height in image_info:
            slice_elem = SubElement(root, 'slice')
            slice_elem.set('filename', filename)
            slice_elem.set('nr', str(sec_num))
            slice_elem.set('width', str(width))
            slice_elem.set('height', str(height))

        # Create output file
        if output_path is None:
            output_path = os.path.join(image_directory, 'series.xml')

        tree = ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"✅ XML descriptor created: {output_path}")
        return output_path

def main():
    parser = argparse.ArgumentParser(description="Generate QuickNII XML descriptor from image folder.")
    parser.add_argument("image_directory", help="Path to folder containing section images (JPG/PNG).")
    parser.add_argument("--output", "-o", help="Optional path to output XML file.")
    parser.add_argument("--name", "-n", help="Optional name of the image series.", default="Brain Image Series")
    args = parser.parse_args()

    generator = QuickNIIXMLGenerator()
    try:
        generator.create_xml_descriptor(args.image_directory, args.output, args.name)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

