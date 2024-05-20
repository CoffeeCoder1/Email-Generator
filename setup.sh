#!/bin/sh
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
python3 -m venv --system-site-packages "$parent_path/.venv"
source "$parent_path/.venv/bin/activate"
pip3 install build
python3 -m build
pip3 install --force-reinstall ./dist/*.whl