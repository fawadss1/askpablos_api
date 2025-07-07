AskPablos API Documentation
===========================

Welcome to the AskPablos API client documentation. This Python library provides a simple and powerful interface for making web requests through the AskPablos proxy service.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api_reference
   examples
   error_handling
   configuration
   troubleshooting

Overview
--------

The AskPablos API client is a Python library designed for making web requests through a proxy service. It features:

* 🔐 **Secure Authentication**: HMAC-SHA256 signature-based authentication
* 🌐 **Proxy Rotation**: Automatic IP rotation to avoid rate limiting
* 🤖 **Browser Automation**: Full browser support with JavaScript rendering
* 📸 **Screenshot Capture**: Take high-quality screenshots of web pages
* ⏱️ **Smart Page Loading**: Wait for complete page load with dynamic content
* 🎛️ **JavaScript Strategies**: Fine-tuned JS control (DEFAULT, True, False)
* 🔄 **GET Method Only**: Focused on GET requests for simplicity and reliability
* 📊 **Query Parameters**: Easy URL parameter handling
* 🛡️ **Error Handling**: Comprehensive exception handling with specific error types
* 📋 **Custom Headers**: Full control over request headers
* 🚀 **High Performance**: Optimized for speed and reliability
* 📝 **Logging Support**: Configurable logging for debugging

Key Features
-----------

Simple Interface
~~~~~~~~~~~~~~~

The `AskPablos` class provides a straightforward interface focused on GET requests:

.. code-block:: python

   from askpablos_api import AskPablos

   client = AskPablos(api_key="your_key", secret_key="your_secret")
   response = client.get("https://example.com")

Advanced Browser Features
~~~~~~~~~~~~~~~~~~~~~~~~

Enable browser automation for JavaScript-heavy sites:

.. code-block:: python

   response = client.get(
       "https://spa-example.com",
       browser=True,
       screenshot=True,
       wait_for_load=True
   )

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Robust exception hierarchy for different error scenarios:

.. code-block:: python

   from askpablos_api import AskPablos, AskPablosError

   try:
       response = client.get("https://example.com")
   except AskPablosError as e:
       print(f"API error: {e}")

Getting Started
--------------

1. **Installation**: ``pip install askpablos-api``
2. **Get API credentials** from the AskPablos dashboard
3. **Initialize the client** with your credentials
4. **Make your first request**

Quick Example
~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import AskPablos

   # Initialize client
   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Make a simple request
   response = client.get("https://httpbin.org/ip")
   print(f"Your IP: {response.content}")

   # Make a request with browser features
   response = client.get(
       "https://example.com",
       browser=True,
       screenshot=True,
       timeout=60
   )

   # Save screenshot if available
   if response.screenshot:
       with open("screenshot.png", "wb") as f:
           f.write(response.screenshot)

Architecture
-----------

The library is structured with these main components:

**Core Classes**
- ``AskPablos``: Main user interface (GET requests only)
- ``ProxyClient``: Lower-level client with full HTTP method support
- ``HTTPClient``: HTTP communication handler

**Data Models**
- ``ResponseData``: Response container with all response information
- ``RequestOptions``: Configuration object for request parameters

**Authentication & Security**
- ``AuthManager``: HMAC-SHA256 signature generation
- ``ParameterValidator``: Request parameter validation

**Utilities**
- ``configure_logging``: Logging configuration
- Exception classes for error handling

Support & Resources
------------------

* **Documentation**: Complete API reference and examples
* **Error Handling**: Comprehensive exception system with specific error types
* **Validation**: Built-in parameter validation with clear error messages
* **Logging**: Configurable logging for debugging and monitoring
* **Community**: Active support for developers

Version Information
------------------

Current version: 0.2.0

The library follows semantic versioning principles for stable API evolution.
