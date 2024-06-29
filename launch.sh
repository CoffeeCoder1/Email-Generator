#!/bin/sh
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
source "$parent_path/.venv/bin/activate"
email-list-parser "$parent_path/data/email-list.txt" | email-generator-gui