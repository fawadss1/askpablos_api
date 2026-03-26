Quick Start Guide
================

Installation
------------

.. code-block:: bash

   pip install askpablos-api

For HTML parsing with XPath, also install ``lxml``:

.. code-block:: bash

   pip install lxml

Basic Setup
-----------

.. code-block:: python

   from askpablos_api import AskPablos

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

Store credentials in environment variables for production:

.. code-block:: python

   import os

   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

Making Requests
---------------

.. code-block:: python

   # Simple GET request
   response = client.get("https://httpbin.org/ip")
   print(response.status_code)
   print(response.content)

   # With headers, params, and timeout
   response = client.get(
       url="https://api.example.com/data",
       headers={"Accept": "application/json"},
       params={"page": "1"},
       timeout=15
   )

Browser Mode
------------

Enable ``browser=True`` for JavaScript-rendered pages. Use ``operations`` with
``waitForElement`` to ensure dynamic content is loaded before the HTML is captured.

.. code-block:: python

   from lxml import etree

   response = client.get(
       url="https://example.com/catalog",
       browser=True,
       operations=[{
           "task": "waitForElement",
           "match": {
               "on": "xpath",
               "rule": "visible",
               "value": "//ul[@class='prod_list']"
           }
       }],
       timeout=45
   )

   dom = etree.HTML(response.content)
   items = dom.xpath("//ul[@class='prod_list']/li")

Screenshots
-----------

.. code-block:: python

   response = client.get(
       url="https://example.com",
       browser=True,
       screenshot=True
   )

   if response.screenshot:
       with open("screenshot.png", "wb") as f:
           f.write(response.screenshot)

Error Handling
--------------

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError,
       RequestTimeoutError
   )

   try:
       response = client.get("https://example.com", timeout=30)
       print(f"Success: {response.status_code}")
   except AuthenticationError as e:
       print(f"Auth failed: {e}")
   except APIConnectionError as e:
       print(f"Connection error: {e}")
   except ResponseError as e:
       print(f"HTTP error: {e}")
   except RequestTimeoutError as e:
       print(f"Timed out: {e}")
