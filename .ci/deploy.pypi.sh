#!/bin/bash

# Do not use `set -x` here as then it displays the PYPIPW in logs
set -e

# Get environment variables, readily decrypted by rultor
source ../rultor_secrets.sh

# Ship it!
echo "Uploading pycolorname to pypi"
pip3 install twine wheel
python3 setup.py sdist bdist_wheel
twine upload dist/* -u "$PYPIUSER" -p "$PYPIPW"

echo "Installing pycolorname from pypi"
pip3 install --pre pycolorname==`cat pycolorname/VERSION` --upgrade
pypi_version=`cd .. && python3 -c "import pycolorname; print(pycolorname.__version__)"`
repo_version=`cat pycolorname/VERSION`

echo versions: pip=$pypi_version repo=$repo_version
[ $pypi_version = $repo_version ]
