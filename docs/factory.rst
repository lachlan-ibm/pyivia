pyIVIA API Version Factory
==========================

Supported Versions
__________________

pyIVIA supports management API from several versions of IBM Verify Identity Access:

- IBM Verify Identity Access 11.0.3.0
- IBM Verify Identity Access 11.0.2.0
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
- IBM Security Access Manager 9.0.7.0
- IBM Security Access Manager 9.0.6.0
- IBM Security Access Manager 9.0.5.0
- IBM Security Access Manager 9.0.4.0
- IBM Security Access Manager 9.0.3.0
- IBM Security Access Manager 9.0.2.1
- IBM Security Access Manager 9.0.2.0


Usage
_____

This module uses the firmware management API to return the version string from Verify Identity Access and return the
appropriate version implementation of the management API.

A user should not attempt to instantiate the versioned classes, instead the ``pyivia.factory`` module should be
used to create a ``pyisava.factory.Factory`` object which is capable of returning version specific implementation of
the five modules used.

.. code-block:: python

   import pyivia
   f = pyivia.factory.Factory("https://verify.identity.access.appliance", "user", "secret")

Verifying TLS to Verify Identity Access Management Interface
____________________________________________________________

By default, connections to verify access local management interface do not verify the x509 certificate with 
python's CA truststore. to verify connections, the ``PYIVIA_VERIFY_TLS_LMI`` environment variable can be used. 
If ``PYIVIA_VERIFY_TLS_LMI=true`` then the default CA certificate store is used to verify TLS connections 
to a Verify Identity Access management interface.

Consult python or operating system documentation for steps to add certificates to this store.

.. autoclass:: pyivia.factory.Factory
   :members:
