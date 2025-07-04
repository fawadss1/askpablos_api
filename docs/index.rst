3. :doc:`api_reference` - Complete API documentation
4. :doc:`examples` - Advanced usage patterns
5. :doc:`error_handling` - Exception handling guide
AskPablos API Documentation
Support
-------
.. toctree::
* **Documentation**: Complete API reference and examples
* **Error Handling**: Comprehensive exception system
* **Validation**: Built-in parameter validation
* **Logging**: Configurable logging for debugging
   examples
   error_handling

Overview
--------

The AskPablos API client is a Python library designed for making web requests through a proxy service. It features:

* 🔐 **Secure Authentication**: HMAC-SHA256 signature-based authentication
* 🌐 **Proxy Rotation**: Automatic IP rotation to avoid rate limiting
* 🤖 **Browser Automation**: Full browser support with JavaScript rendering
* 📸 **Screenshot Capture**: Take high-quality screenshots of web pages
* ⏱️ **Smart Page Loading**: Wait for complete page load with dynamic content
* 🎛️ **JavaScript Strategies**: Fine-tuned JS control (DEFAULT, True, False)
* 🔄 **Multiple HTTP Methods**: Support for GET, POST, PUT, DELETE, and more
* 📊 **Query Parameters**: Easy URL parameter handling
* 🛡️ **Error Handling**: Comprehensive exception handling with specific error types
* 📋 **Custom Headers**: Full control over request headers
* 🚀 **High Performance**: Optimized for speed and reliability
* 📦 **Minimal Dependencies**: Only requires the standard requests library

Key Components
--------------

The library consists of several key components:

**AskPablos Class**
   The main high-level interface for making proxy requests with comprehensive options for browser automation, proxy rotation, and screenshot capture.

**ProxyClient Class**
   Lower-level client that handles direct communication with the AskPablos API service, supporting all HTTP methods and advanced proxy configurations.

**ResponseData Class**
   Enhanced response object that provides structured access to response data, including screenshot data and detailed timing information.

**Exception Classes**
   Comprehensive exception hierarchy for proper error handling and debugging, including parameter validation.

Quick Example
-------------

.. code-block:: python

   from askpablos_api import AskPablos

   # Initialize client
   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Simple request
   response = client.get("https://httpbin.org/ip")
   print(f"Status: {response.status_code}")

   # Advanced request with browser features
   response = client.get(
       url="https://spa-example.com",
       browser=True,
       wait_for_load=True,
       screenshot=True,
       js_strategy="DEFAULT",
       rotate_proxy=True,
       timeout=45
   )

New Features in Latest Version
-----------------------------

**Enhanced Browser Support**
   - Screenshot capture with `screenshot=True`
   - Page load waiting with `wait_for_load=True`
   - JavaScript strategy control with `js_strategy` options

**Proxy Management**
   - Automatic proxy rotation with `rotate_proxy=True`
   - Smart timeout handling for different request types

**Parameter Handling**
   - URL query parameters support with `params` dictionary
   - Custom headers support with `headers` dictionary
   - Additional proxy options via `**options`

**Validation & Error Handling**
   - Parameter validation for browser-specific features
   - Enhanced error messages with specific exception types
   - Improved debugging with detailed response information

Getting Started
---------------

1. :doc:`installation` - Install the library
2. :doc:`quickstart` - Basic usage and examples

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
