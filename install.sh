#!/bin/sh
parent_path="$HOME/.local/share/email-generator"
cd "$parent_path"
python3 -m venv --system-site-packages "$parent_path/.venv"
source "$parent_path/.venv/bin/activate"
pip3 install email-draft-generator