WebSEAL Reverse Proxy Settings
##############################
The WebSEAL module contains methods to configure reverse proxy instances and the associated identity configuration.

.. _web_settings:

WebSEAL (Web Reverse Proxy)
***************************

The Web Settings module can be used to configure the Web Reverse Proxy and associated junctions as well as configure
integrations with the Runtime Server's user registry and policy server.

.. automodule:: pyisva.core.websettings
   :members:


API Access Control
==================

The API Access Control module is used to configure WebSEAL instances which can be used as API Gateways

.. automodule:: pyisva.core.web.api_access_control


Authorization Server
--------------------

.. autoclass:: pyisva.core.web.apiac.authorization_server.AuthorizationServer
   :members:

Cross Origin Remote Scripting
-----------------------------

.. autoclass:: pyisva.core.web.apiac.cors.CORS
   :members:

Document Root
-------------

.. autoclass:: pyisva.core.web.apiac.document_root.DocumentRoot
    :members:

Policies
--------

.. autoclass:: pyisva.core.web.apiac.policies.Policies
   :members:

Resources
---------

.. autoclass:: pyisva.core.web.apiac.resources.Resources
   :members:

Utilities
---------

.. autoclass:: pyisva.core.web.apiac.utilities.Utilities
   :members:

Client Certificate Mapping
==========================

.. autoclass:: pyisva.core.web.clientcertmapping.ClientCertMapping
   :members:

Distributed Session Cache
=========================

.. autoclass:: pyisva.core.web.dscadmin.DSCAdmin
   :members:

Form Single Sign-On
===================

.. autoclass:: pyisva.core.web.fsso.FSSO
   :members:

HTTP Transformations
====================

.. autoclass:: pyisva.core.web.httptransform.HTTPTransform
   :members:

Junction Mapping
================

.. autoclass:: pyisva.core.web.junctionmapping.JunctionMapping
   :members:

Kerberos
========

.. autoclass:: pyisva.core.web.kerberos.Kerberos
   :members:

Password Strength Rules
=======================

.. autoclass:: pyisva.core.web.passwordstrength.PasswordStrength
   :members:

Policy Administration
=====================

.. autoclass:: pyisva.core.web.policyadmin.PolicyAdmin
   :members:

Rate Limiting
=============

.. autoclass:: pyisva.core.web.ratelimit.RateLimit
   :members:

Reverse proxy
=============

.. autoclass:: pyisva.core.web.reverseproxy.ReverseProxy
   :members:

RSA Security Token
==================

.. autoclass:: pyisva.core.web.rsa.RSA
   :members:

Runtime Component
=================

.. autoclass:: pyisva.core.web.runtimecomponent.RuntimeComponent
   :members:

URL Mapping
===========

.. autoclass:: pyisva.core.web.urlmapping.URLMapping
   :members:

User Mapping
============

.. autoclass:: pyisva.core.web.usermapping.UserMapping
   :members:
