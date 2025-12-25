#!/usr/bin/env bash

set -euo pipefail

SOURCES=(
    "/usr/share/backgrounds/gnome/pixel-pusher-d.jxl"
    "/usr/share/backgrounds/gnome/pixel-pusher-l.jxl"
)

apply_mask() {
    folder=$(dirname $1)
    source=$(basename $1)
    raw_source="original-${source/.jxl/.ppm}"
    raw_masked="masked-${source/.jxl/.ppm}"
    masked="masked-${source}"

    echo ">>> ${folder} <<<"
    echo "> Decoding ${source}..."
    djxl "${folder}/${source}" "${raw_source}"
    echo "> Created ${raw_source}."

    echo "> Masking ${raw_source} ..."
    ./solar_mask.py < ${raw_source} > ${raw_masked}
    echo "> Created ${raw_masked}."

    cjxl "${raw_masked}" "${masked}"
    echo "> Created ${masked}."
}

for item in "${SOURCES[@]}"
do
    apply_mask $item
done

