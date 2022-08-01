#!/bin/bash
python setup.py sdist bdist_wheel
export PYTHONPATH="$PYTHONPATH:$(pwd)/build/lib"
python <<EOF
from pyisva.factory import Factory
f = Factory("https://ibm.security.verify.access", "user", "password")
EOF

exit 0
