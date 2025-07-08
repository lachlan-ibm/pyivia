# PyIVIA

PyIVIA is a Python library that wraps the IBM Verify Identity Access RESTful Web services to provide a

quick and easy way to construct configuration scripts for appliances.

**Supported Versions**
- IBM Verify Identity Access 11.0.1.0
- IBM Verify Identity Access 11.0.0.0
- IBM Security Verify Access 10.0.9.0
- IBM Security Verify Access 10.0.8.0
- IBM Security Verify Access 10.0.7.0
- IBM Security Verify Access 10.0.6.0
- IBM Security Verify Access 10.0.5.0
- IBM Security Verify Access 10.0.4.0
- IBM Security Verify Access 10.0.3.1
- IBM Security Verify Access 10.0.3.0
- IBM Security Verify Access 10.0.2.0
- IBM Security Verify Access 10.0.1.0
- IBM Security Verify Access 10.0.0.0
- IBM Security Access Manager 9.0.7.3
- IBM Security Access Manager 9.0.7.2
- IBM Security Access Manager 9.0.7.1
- IBM Security Access Manager 9.0.7.0
- IBM Security Access Manager 9.0.6.0
- IBM Security Access Manager 9.0.5.0
- IBM Security Access Manager 9.0.4.0
- IBM Security Access Manager 9.0.3.0
- IBM Security Access Manager 9.0.2.1
- IBM Security Access Manager 9.0.2.0

## Installation

For Linux/macOS: if you clone the library to `~/repos/pyivia`, add this to `~/.profile`:
```sh
# add pyivia library to Python's search path
export PYTHONPATH="${PYTHONPATH}:${HOME}/repos/pyivia"
```

## From IBM Security Verify Access 10.0.0.0 onwards:
Module has been build into a package Currently hosted on PyPi that can be installed using pip:

```sh
pip install pyivia
```

## Usage

```python
>>> import pyivia
>>> factory = pyivia.Factory("https://isam.mmfa.ibm.com", "admin", "Passw0rd")
>>> web = factory.get_web_settings()
>>> resp = web.reverse_proxy.restart_instance("default")
>>> if resp.success:
...     print("Successfully restarted the default instance.")
... else:
...     print("Failed to restart the default instance. status_code: %s, data: %s" % (resp.status_code, resp.data))
...
Successfully restarted the default instance.
```

## Documentation
Documentation for using this library can be found on [pyivia GitHub pages](https://lachlan-ibm.github.io/pyivia/index.html).
