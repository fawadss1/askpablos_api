AskPablos API Documentation
===========================

A Python client for making web requests through the AskPablos proxy service.

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

Features
--------

* **Secure Authentication**: HMAC-SHA256 signature-based
* **Browser Automation**: JavaScript rendering with ``browser=True``
* **Browser Operations**: Wait for elements with ``waitForElement``
* **Screenshot Capture**: ``screenshot=True``
* **Custom Headers & Params**: Full control over requests
* **Error Handling**: Specific exception types for each failure mode

Quick Example
-------------

.. code-block:: python

   from askpablos_api import AskPablos
   from lxml import etree

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Static page
   response = client.get("https://httpbin.org/ip")
   print(response.content)

   # JS-rendered page — wait for element, then parse
   response = client.get(
       "https://example.com",
       browser=True,
       operations=[{
           "task": "waitForElement",
           "match": {"on": "xpath", "rule": "visible", "value": "//body"}
       }]
   )
   dom = etree.HTML(response.content)

Architecture
------------

- ``AskPablos``: Main interface (GET requests)
- ``ProxyClient``: Lower-level client with full HTTP method support
- ``ResponseData``: Response object (``status_code``, ``content``, ``headers``, ``screenshot``, ``elapsed_time``)
- ``AuthManager``: HMAC-SHA256 signing

Current version: 0.3.0
