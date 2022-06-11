#!/usr/bin/bash
python3 -m venv magoosh &&
source magoosh/bin/activate &&
pip install --no-cache-dir wheel &&
pip install --no-cache-dir -r requirements.txt &&
path="$(pwd)" &&
path="${path}/magoosh_videos" &&
python3 get_magoosh.py  ${1:-${path}} &&
deactivate &&
rm -rf magoosh
