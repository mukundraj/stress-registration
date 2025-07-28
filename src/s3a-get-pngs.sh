#!/bin/sh
# convert tifs exported by histolozee to png format for quicknii
#
# ./src/s3-get-pngs.sh

ipdir=~/Desktop/work/data/stress-atlas/v1/s2-mspace/
opdir=~/Desktop/work/data/stress-atlas/v1/s3-mspace-pngs/

# convert all tifs in ipdir to pngs in opdir

mkdir -p "$opdir"

for tif_file in "$ipdir"*.tif; do
    if [ -f "$tif_file" ]; then
        filename=$(basename "$tif_file" .tif)
        vips copy "$tif_file" "$opdir$filename.png"
        echo "Converted: $filename.tif -> $filename.png"
    fi
done

echo "Conversion complete!"
