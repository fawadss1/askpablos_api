API Reference
=============

This section provides detailed documentation for all classes and methods in the AskPablos API client.

AskPablos Class
---------------

.. autoclass:: askpablos_api.AskPablos
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__
   .. automethod:: get

ProxyClient Class
-----------------

.. autoclass:: askpablos_api.ProxyClient
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__
   .. automethod:: request

Exceptions
----------

.. automodule:: askpablos_api.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

AskPablosError
~~~~~~~~~~~~~~

.. autoexception:: askpablos_api.AskPablosError
   :members:
   :show-inheritance:

AuthenticationError
~~~~~~~~~~~~~~~~~~~

.. autoexception:: askpablos_api.AuthenticationError
   :members:
   :show-inheritance:

APIConnectionError
~~~~~~~~~~~~~~~~~~

.. autoexception:: askpablos_api.APIConnectionError
   :members:
   :show-inheritance:

ResponseError
~~~~~~~~~~~~~

.. autoexception:: askpablos_api.ResponseError
   :members:
   :show-inheritance:

Utility Functions
-----------------

.. automodule:: askpablos_api.utils
   :members:
   :undoc-members:

configure_logging
~~~~~~~~~~~~~~~~~

.. autofunction:: askpablos_api.configure_logging

build_proxy_options
~~~~~~~~~~~~~~~~~~~

.. autofunction:: askpablos_api.build_proxy_options

Method Details
--------------

get() Method
~~~~~~~~~~~~

The primary method for making GET requests through the proxy.

**Signature:**

.. code-block:: python

   get(url, params=None, headers=None, browser=False, rotate_proxy=True, timeout=30, **options)

**Parameters:**

* **url** (*str*) - The target URL to fetch. Must be a valid HTTP/HTTPS URL.
* **params** (*dict, optional*) - URL query parameters to append.
* **headers** (*dict, optional*) - Custom headers for the request.
* **browser** (*bool, optional*) - Whether to use browser automation. Defaults to False.
* **rotate_proxy** (*bool, optional*) - Whether to use proxy rotation. Defaults to True.
* **timeout** (*int, optional*) - Request timeout in seconds. Defaults to 30.
* **options** - Additional proxy options like user_agent, cookies, etc.

**Returns:**

* **dict** - JSON response from the API

**Raises:**

* **AuthenticationError** - If credentials are invalid
* **APIConnectionError** - If connection fails
* **ResponseError** - If API returns an error

**Example:**

.. code-block:: python

   response = client.get(
       "https://api.example.com/data",
       params={"page": 1},
       headers={"Authorization": "Bearer token"},
       browser=True,
       timeout=60
   )
