API Reference
=============

This section provides detailed documentation for all classes and methods in the AskPablos API client.

Core Classes
------------

AskPablos
~~~~~~~~~

.. autoclass:: askpablos_api.AskPablos
   :members:
   :undoc-members:
   :show-inheritance:

The main client class for making requests through the AskPablos proxy service. This is the primary interface that most users will interact with.

ProxyClient
~~~~~~~~~~~

.. autoclass:: askpablos_api.ProxyClient
   :members:
   :undoc-members:
   :show-inheritance:

A lower-level client for direct proxy interactions and advanced use cases.

HTTPClient
~~~~~~~~~~

.. autoclass:: askpablos_api.HTTPClient
   :members:
   :undoc-members:
   :show-inheritance:

Handles HTTP communication and request execution.

AuthManager
~~~~~~~~~~~

.. autoclass:: askpablos_api.AuthManager
   :members:
   :undoc-members:
   :show-inheritance:

Manages authentication and HMAC signature generation.

ParameterValidator
~~~~~~~~~~~~~~~~~~

.. autoclass:: askpablos_api.ParameterValidator
   :members:
   :undoc-members:
   :show-inheritance:

Validates request parameters and enforces API requirements.

Data Models
-----------

ResponseData
~~~~~~~~~~~~

.. autoclass:: askpablos_api.ResponseData
   :members:
   :undoc-members:
   :show-inheritance:

RequestOptions
~~~~~~~~~~~~~~

.. autoclass:: askpablos_api.RequestOptions
   :members:
   :undoc-members:
   :show-inheritance:

Exception Classes
-----------------

AskPablosError
~~~~~~~~~~~~~~

.. autoclass:: askpablos_api.AskPablosError
   :members:
   :undoc-members:
   :show-inheritance:

AuthenticationError
~~~~~~~~~~~~~~~~~~~

.. autoclass:: askpablos_api.AuthenticationError
   :members:
   :undoc-members:
   :show-inheritance:

APIConnectionError
~~~~~~~~~~~~~~~~~~

.. autoclass:: askpablos_api.APIConnectionError
   :members:
   :undoc-members:
   :show-inheritance:

ResponseError
~~~~~~~~~~~~~

.. autoclass:: askpablos_api.ResponseError
   :members:
   :undoc-members:
   :show-inheritance:
