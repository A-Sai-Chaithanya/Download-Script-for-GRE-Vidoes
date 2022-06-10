#!/usr/bin/bash
python3 -m venv magoosh &&
source magoosh/bin/activate &&
pip install wheel &&
pip install --no-cache-dir -r requirements.txt &&
path="$(pwd)" &&
path="${path}/magoosh_videos" &&
python3 get_magoosh.py  ${path} &&
deactivate &&
rm -rf magoosh
