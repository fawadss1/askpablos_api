Quick Start
===========

This guide will help you get started with the AskPablos API client in just a few minutes.

Basic Setup
-----------

First, import the client and create an instance:

.. code-block:: python

   from askpablos_api import AskPablos

   # Initialize the client with your credentials
   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

Authentication
--------------

The AskPablos API uses HMAC-SHA256 signature-based authentication. You need:

1. **API Key**: Your unique identifier
2. **Secret Key**: Your private signing key

.. code-block:: python

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

Making Your First Request
-------------------------

.. code-block:: python

   # Simple GET request
   response = client.get("https://httpbin.org/ip")
   print(response)

   # Expected output:
   # {
   #     "status_code": 200,
   #     "headers": {"content-type": "application/json", ...},
   #     "content": '{"origin": "123.456.789.0"}',
   #     "url": "https://httpbin.org/ip",
   #     "proxy_used": "proxy.example.com:8080",
   #     "time_taken": 1.23
   # }

Common Usage Patterns
---------------------

GET with Query Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   response = client.get(
       "https://api.example.com/users",
       params={"page": 1, "limit": 10}
   )

GET with Custom Headers
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   response = client.get(
       "https://api.example.com/protected",
       headers={"Authorization": "Bearer your_token"}
   )

JavaScript-Heavy Sites
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use browser automation for SPAs
   response = client.get(
       "https://spa-website.com",
       browser=True
   )

Response Format
---------------

All successful requests return a dictionary with:

.. code-block:: python

   {
       "status_code": 200,                    # HTTP status code
       "headers": {...},                      # Response headers
       "content": "Response body content",    # Response content
       "url": "Final URL after redirects",   # Final URL
       "proxy_used": "proxy.example.com",    # Proxy information
       "time_taken": 1.23                    # Request duration
   }

Error Handling
--------------

.. code-block:: python

   from askpablos_api import AskPablos, AuthenticationError, ResponseError

   try:
       client = AskPablos(api_key="", secret_key="")
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")

   try:
       response = client.get("https://example.com")
   except ResponseError as e:
       print(f"API error {e.status_code}: {e.message}")

Next Steps
----------

* Read the :doc:`api_reference` for detailed method documentation
* Check out :doc:`examples` for more usage patterns
* Learn about :doc:`error_handling` for robust applications
