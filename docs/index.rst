Welcome to pyISVA!
==================================
pyISVA is an python wrapper to the IBM Security Verify Access configuration API. You can use this library to interact 
with a Verify Access Deployment; applying and deploying configuration.


Installation
------------
You can install ``pyisva`` with ``pip``:

.. code-block:: bash

   $ pip install pyisva


Architecture
------------
pyISVA is broken into five modules which are responsible for configuring specific features of an deployment. These modules
are versioned and should be created using the provided factory methods. The factory does basic discovery on the appliance to 
determine the release version and deployment model being used.

The system settings and analysis/diagnostics features are used to set up system wide features such as SSL databases and 
log forwarding.The WebSEAL, Access Control and Federation modules are responsible for configuring their respective API.

Changes are published using the ``system.restartshutdown`` module, which is capable of publishing changes for both 
Container and Appliance deployment architectures. Note for Container architectures pyISVA is NOT capable of managing the 
runtime containers.


.. toctree::
    :maxdepth: 2
    :caption: pyISVA modules

    factory
    systemsettings
    analysisdiagnostics
    websettings
    accesscontrol
    federation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
