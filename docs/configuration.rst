Configuration
=============

Client Setup
------------

.. code-block:: python

   import os
   from askpablos_api import AskPablos

   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

Request Options
---------------

All options available on ``client.get()``:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Default
     - Description
   * - ``url``
     - str
     - required
     - Target URL to fetch
   * - ``headers``
     - dict
     - None
     - Custom request headers
   * - ``params``
     - dict
     - None
     - URL query parameters
   * - ``browser``
     - bool
     - False
     - Enable browser/JS rendering
   * - ``screenshot``
     - bool
     - False
     - Capture page screenshot (requires ``browser=True``)
   * - ``operations``
     - list
     - None
     - Browser operations (e.g. ``waitForElement``)
   * - ``timeout``
     - int
     - 30
     - Seconds before request times out
   * - ``max_retries``
     - int
     - 3
     - Retry attempts on failure

Browser Operations
------------------

Use ``operations`` to interact with the page before HTML is captured:

.. code-block:: python

   response = client.get(
       url="https://example.com",
       browser=True,
       operations=[{
           "task": "waitForElement",
           "match": {
               "on": "xpath",
               "rule": "visible",
               "value": "//div[@id='content']"
           }
       }],
       timeout=45
   )

Logging
-------

.. code-block:: python

   import logging
   from askpablos_api import configure_logging

   configure_logging(level=logging.DEBUG)
