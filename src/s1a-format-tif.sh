#!/bin/bash
# formats original tif to pyramidal tif for histolozee
#
# ./src/s1a-format-tif.sh

ipdir=~/Desktop/work/data/stress-atlas/v1/s0-raw
opdir=~/Desktop/work/data/stress-atlas/v1/s1-tifs

# vips tiffsave 3a.tif 3a-p2.tif --tile --pyramid --compression deflate --tile-width 256 --tile-height 256

# list files in ipdir
for file in "$ipdir"/*.tif; do
    # get the filename without the path
    filename=$(basename "$file")
    echo $filename

    # use vips to convert file to pyramidal tif and place in opdir
    vips tiffsave "$file" "$opdir/$filename" --tile --pyramid --compression deflate --tile-width 256 --tile-height 256

done

