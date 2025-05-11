#!/usr/bin/env bash

repo="$(dirname "$(dirname "$0")")"
device=

# My current laptop's parameters.
resolution=960x540
dpi=160
density=1
scale=1

usage() {
    echo "$0 [-d DPI] [-r RESOLUTION] [-s SCALE]"
    echo
    echo -e "\tDPI\t\tdots/pixels per inch [$dpi]"
    echo -e "\tRESOLUTION\tWWWWxHHHH in pixels [$resolution]"
    echo -e "\tSCALE\t\tScale factor (DPI/160) [$scale]"
}
while getopts "d:hp:r:s:" o; do
    case "$o" in
        d)
            dpi="$OPTARG"
            ;;
        h)
            usage
            exit
            ;;
        p)
            density="$OPTARG"
            if [[ $density -gt 10 ]]; then
                echo "Invalid 'p'; 0 < p < 10"
                exit 1
            fi
            ;;
        r)
            resolution="$OPTARG"
            ;;
        s)
            scale="$OPTARG"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [[ -n $1 ]]; then
    device="$1"
fi

if [[ $device == a13 ]]; then
    resolution=2408x1080
    dpi=377
    density=2.35
    # scale=1
elif [[ $device == a10 ]]; then
    resolution=1920x1200
    dpi=241
    density=1.5
    # scale=1
elif [[ $devcie == a7lite ]]; then
    resolution=1340x800
    dpi=178
    density=1
    # scale=1
fi

export KIVY_DPI=$((dpi * scale))
export KIVY_METRICS_DENSITY=$((density * scale))
cd "$repo" && python -m src.life_pod --size="$resolution"