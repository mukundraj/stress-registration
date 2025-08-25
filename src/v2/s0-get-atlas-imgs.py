"""Download allen atlas nissl images for saggital sections

Usage:

python script.py \
    io: dataroot
    op: outdir

Example:

python src/v2/s0-get-atlas-imgs.py \
    ~/Desktop/work/data/ \
    stress-atlas/v2/s0-atlas-nissls
    
Notes:

https://mouse.brain-map.org/static/atlas

Supplementary:

mm activate allen

Created by Mukund on 2025-08-20
"""


from allensdk.api.queries.image_download_api import ImageDownloadApi
from allensdk.api.queries.svg_api import SvgApi
from allensdk.config.manifest import Manifest

from allensdk.api.queries.image_download_api import ImageDownloadApi
import pandas as pd
from pathlib import Path
import os

import sys
from pathlib import Path
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

dataroot = sys.argv[1]
datafolder = sys.argv[2]

print(dataroot)
print(datafolder)
output_dir = Path(f'{dataroot}{datafolder}/').expanduser()
print(output_dir)


image_api = ImageDownloadApi()
atlas_id = 2  # P56 Mouse Brain Atlas
atlas_image_records = image_api.atlas_image_query(atlas_id)
atlas_image_dataframe = pd.DataFrame(atlas_image_records)
# Get the image IDs for the sagittal Nissl sections
sagittal_ids = atlas_image_dataframe['id'].tolist()

print(len(sagittal_ids))

os.makedirs(output_dir, exist_ok=True)
downsample = 2  # 0 = full resolution


# download nissl images
for img_id in sagittal_ids:
    file_path = Path(output_dir) / f'{img_id}_nissl.png'
    image_api.download_atlas_image(img_id, file_path, annotation=False, downsample=downsample)


# download annotation and svg images
svg_api = SvgApi()
for img_id in sagittal_ids:
    file_path = Path(output_dir) / f'anno/{img_id}_anno.png'
    image_api.download_atlas_image(img_id, file_path, annotation=True, downsample=downsample)

    file_path = Path(output_dir) / f'svgs/{img_id}_svg.svg'
    svg_api.download_svg(img_id, file_path=f'{file_path}')
    
