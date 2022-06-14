#!/usr/bin/bash
trap cleanup 2

cleanup()
{
    clear
    echo 'SIGINT or SIGQUIT detected'
    echo 'Cleaning Up and Exiting'
    deactivate
    rm -r ${path} "$(pwd)/magoosh" "$(pwd)/download.log"
    exit
}

python3 -m venv magoosh &&
source magoosh/bin/activate &&
pip install --no-cache-dir wheel &&
pip install --no-cache-dir -r requirements.txt && clear &&
path="$(pwd)/magoosh_videos" &&
path=${1:-${path}}
python3 get_magoosh.py  ${path} &&
deactivate &&
rm -rf magoosh
