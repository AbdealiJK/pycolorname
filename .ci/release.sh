#!/bin/bash

set -x
set -e

# Abort if uncommitted things lie around
git diff HEAD --exit-code

# Release!
python3 .ci/adjust_version_number.py pycolorname/VERSION --release
bash .ci/deploy.pypi.sh

# Adjust version number to next release, script will check validity
python3 .ci/adjust_version_number.py pycolorname/VERSION --new-version ${tag} -b 0

# Commit it
git add pycolorname/VERSION
git commit -m "[GENERATED] Increment version to ${tag}"
