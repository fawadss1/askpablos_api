AskPablos API Documentation
==========================

Welcome to the AskPablos API client documentation. This library provides a simple and secure way to make GET requests through the AskPablos proxy service.

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
* 🛡️ **Error Handling**: Comprehensive exception handling
* 📊 **Logging**: Built-in logging support for debugging
* 🎯 **Simple Interface**: GET-only requests for clean API

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
   print(response)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
