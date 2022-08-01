#!/bin/bash
python setup.py sdist bdist_wheel
export PYTHONPATH="$PYTHONPATH:$(pwd)/build/lib"
cd .tests && python -m http.server &
SERVER_PID="$!"
python <<EOF
import pyisva
f = pyisva.Factory("http://localhost:8000", "user", "password")
EOF
kill $SERVER_PID
exit 0
