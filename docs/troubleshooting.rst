Troubleshooting
===============

Authentication Errors
---------------------

**Problem**: ``AuthenticationError: Invalid API credentials``

- Verify your API key and secret key from the AskPablos dashboard
- Use environment variables instead of hardcoding keys

.. code-block:: python

   import os
   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

Connection / Timeout Errors
---------------------------

**Problem**: ``APIConnectionError`` or ``RequestTimeoutError``

- Increase the timeout value
- Increase ``max_retries``

.. code-block:: python

   response = client.get(
       "https://slow-website.com",
       timeout=60,
       max_retries=5
   )

XPath Returns No Results
------------------------

**Problem**: ``dom.xpath(...)`` returns an empty list even though the element exists on the site.

The page content is likely JavaScript-rendered. Use ``operations`` with ``waitForElement``
so the browser waits for the element to appear before capturing the HTML:

.. code-block:: python

   from lxml import etree

   response = client.get(
       url="https://example.com",
       browser=True,
       operations=[{
           "task": "waitForElement",
           "match": {
               "on": "xpath",
               "rule": "visible",
               "value": "//ul[@class='prod_list']"
           }
       }]
   )

   dom = etree.HTML(response.content)
   items = dom.xpath("//ul[@class='prod_list']/li")

.. note::
   Always use ``from lxml import etree``. Python's stdlib ``xml.etree`` has no
   ``HTML()`` method and will silently fail.

Screenshot Not Captured
-----------------------

**Problem**: ``response.screenshot`` is ``None``

``screenshot=True`` requires ``browser=True``:

.. code-block:: python

   response = client.get(
       "https://example.com",
       browser=True,   # required
       screenshot=True
   )

Parameter Validation Error
--------------------------

**Problem**: ``ValueError: browser=True is required for screenshot=True``

Any browser feature (``screenshot``, ``operations``) requires ``browser=True``.

Debugging
---------

Enable debug logging to inspect requests:

.. code-block:: python

   import logging
   from askpablos_api import configure_logging

   configure_logging(level=logging.DEBUG)
