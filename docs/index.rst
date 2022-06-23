Welcome to pyISVA's documentation!
==================================
pyISVA is an python wrapper to the IBM Security Verify Access configuration API. You can use this library to interact 
with a Verify Access Deployment; applying and deploying configuration.


Installation
------------
You can install ``pyisva`` with ``pip``:

.. code-block:: console
    $ pip install pyisva

.. _pyisva_architecture

Architecture
------------
pyISVA is broken into six modules which are responsible for configuring specific aspects of an appliance. The base,
appliance and docker modules are responsible for system configuration such as SSL databases, date/time settings,
and log collation.

The WebSEAL, AAC and Federation modules are responsible for configuring their respective API.


.. automodule:: pyisva
   :members:


.. toctree::
    :maxdepth: 2
    :caption: pyISVA modules

    base
    appliance
    docker
    webseal
    aac
    federation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
