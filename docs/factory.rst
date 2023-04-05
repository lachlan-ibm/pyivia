pyISVA API Version Factory
==========================

Supported Versions
__________________

pyISVA supports management API from several versions of IBM Security Verify Access:

- IBM Security Verify Access 10.0.5.0
- IBM Security Verify Access 10.0.4.0
- IBM Security Verify Access 10.0.3.1
- IBM Security Verify Access 10.0.3.0
- IBM Security Verify Access 10.0.2.0
- IBM Security Verify Access 10.0.1.0
- IBM Security Verify Access 10.0.0.0
- IBM Security Access Manager 9.0.7.0
- IBM Security Access Manager 9.0.6.0
- IBM Security Access Manager 9.0.5.0
- IBM Security Access Manager 9.0.4.0
- IBM Security Access Manager 9.0.3.0
- IBM Security Access Manager 9.0.2.1
- IBM Security Access Manager 9.0.2.0


Usage
_____

This module uses the firmware management API to return the version string from Verify Access and return the
appropriate version implementation of the management API.

A user should not attempt to instantiate the versioned classes, instead the ``pyisva.factory`` module should be
used to create a ``pyisava.factory.Factory`` object which is capable of returning version specific implementation of
the five modules used.

.. code-block:: python

   import pyisva
   f = pyisva.factory.Factory("https://verify.access.appliance", "user", "secret")


.. automodule:: pyisva.factory
   :members:
