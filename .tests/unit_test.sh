#!/bin/bash
python setyp.py sdist bdist_wheel
export PYTHONPATH="$PYTHONPATH:$(pwd)/build/lib"
python <<EOF
import pyisva
f = pyisva.factory("https://ibm.security.verify.access", "user", "password")
EOF

exit 0
