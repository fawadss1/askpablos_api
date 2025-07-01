AskPablos API Documentation
==========================

Welcome to the AskPablos API client documentation. This library provides a professional, simple and secure way to make GET requests through the AskPablos proxy service with rotating IP addresses and browser support.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api_reference
   examples
   error_handling

Overview
--------

The AskPablos API client is a Python library designed for making GET requests through a proxy service. It features:

* 🔐 **Secure Authentication**: HMAC-SHA256 signature-based authentication
* 🌐 **Proxy Support**: Route requests through rotating proxies
* 🤖 **Browser Integration**: Support for JavaScript-heavy websites
* 🛡️ **Error Handling**: Comprehensive exception handling with specific error types
* 📊 **Logging**: Built-in logging support for debugging and monitoring
* 🎯 **Simple Interface**: GET-only requests for clean and focused API
* 🚀 **High Performance**: Optimized for speed and reliability
* 📦 **Zero Dependencies**: Only requires the standard requests library

Key Components
--------------

The library consists of several key components:

**AskPablos Class**
   The main high-level interface for making proxy requests. This is what most users will interact with.

**ProxyClient Class**
   Lower-level client that handles the direct communication with the AskPablos API service, including authentication and request signing.

**ResponseData Class**
   Response object that provides structured access to response data with dot notation.

**Exception Classes**
   Comprehensive exception hierarchy for proper error handling and debugging.

Quick Example
-------------

.. code-block:: python

   from askpablos_api import AskPablos

   # Initialize the client
   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Make a GET request
   response = client.get("https://httpbin.org/ip")
   print(f"Status: {response.status_code}")
   print(f"Content: {response.content}")

   # With custom options
   response = client.get(
       url="https://example.com",
       headers={"User-Agent": "Custom Agent"},
       use_browser=True,
       timeout=30
   )

Installation
------------

Install the library using pip:

.. code-block:: bash

   pip install askpablos-api

Requirements
------------

- Python 3.9 or higher
- requests >= 2.25.0

Getting Help
------------

* Read the :doc:`quickstart` guide for a quick introduction
* Check the :doc:`api_reference` for detailed API documentation
* Review :doc:`examples` for practical usage scenarios
* Learn about :doc:`error_handling` for robust error management

Links
-----

* **PyPI**: https://pypi.org/project/askpablos-api/
* **Documentation**: https://askpablos-api.readthedocs.io/en/latest/
* **Source Code**: https://github.com/fawadss1/askpablos_api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
