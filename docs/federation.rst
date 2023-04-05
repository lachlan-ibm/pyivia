
.. _federation:

Federations
###########
The Federations module can be used to configure standards based integrations using Federated technologies, such as 
OIDC and SAML. This module is also used to configure how identity attributes are mapped between token types as well
as providing additional sources of information for federated identities.


.. automodule:: pyisva.core.federationsettings
   :members:


Federations configuration
=========================


.. autoclass:: pyisva.core.federation.federations.Federations
   :members:


Access Policies
===============


.. autoclass:: pyisva.core.federation.accesspolicy.AccessPolicy
   :members:


Attribute Sources
=================


.. autoclass:: pyisva.core.federation.attributesources.AttributeSources
   :members:


Point of Contact (POC) Profile
==============================


.. autoclass:: pyisva.core.federation.pointofcontact.PointOfContact
    :members:


Security Token Service (STS)
============================


.. autoclass:: pyisva.core.federation.securitytokenservice.SecurityTokenService
   :members: