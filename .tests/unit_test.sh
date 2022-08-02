#!/bin/bash
python setup.py sdist bdist_wheel
export PYTHONPATH="$PYTHONPATH:$(pwd)/build/lib"
$( cd .tests && python <<EOF
from http import server
import socketserver, json
PORT = 8000
VERSION_JSON = {
    "firmware_label":"isva_10.0.0.0_20200601-2346",
    "firmware_build":"20200601-2346",
    "firmware_version":"10.0.0.0",
    "product_description":"IBM Security Verify Access",
    "deployment_model":"Appliance",
    "product_name":"isva"
}
def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json; charset=utf-8')
    self.end_headers()
    self.wfile.write(json.dumps(VERSION_JSON).encode())

Handler = server.SimpleHTTPRequestHandler
Handler.do_GET = do_GET
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()
EOF
) &
SERVER_PID="$!"
python <<EOF
import pyisva
f = pyisva.Factory("http://localhost:8000", "user", "password")
EOF
kill $SERVER_PID
exit 0
