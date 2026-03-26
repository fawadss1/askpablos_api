Installation
============

Requirements
------------

* Python 3.9+
* ``requests >= 2.25.0`` (installed automatically)
* ``lxml >= 4.6`` — optional, required for HTML/XPath parsing

.. code-block:: bash

   pip install askpablos-api

   # With lxml for HTML parsing
   pip install "askpablos-api[parsing]"

   # Or install lxml separately
   pip install lxml

.. note::
   Use ``from lxml import etree`` for HTML parsing — Python's stdlib ``xml.etree``
   has no ``HTML()`` method and does not support full XPath.

Virtual Environment (Recommended)
----------------------------------

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows

   pip install askpablos-api

Environment Variables
---------------------

Store credentials securely:

**macOS/Linux:**

.. code-block:: bash

   export ASKPABLOS_API_KEY="your_api_key"
   export ASKPABLOS_SECRET_KEY="your_secret_key"

**Windows:**

.. code-block:: batch

   set ASKPABLOS_API_KEY=your_api_key
   set ASKPABLOS_SECRET_KEY=your_secret_key

Then in Python:

.. code-block:: python

   import os
   from askpablos_api import AskPablos

   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

Verify Installation
-------------------

.. code-block:: python

   import askpablos_api
   print(askpablos_api.__version__)
