Installation
============

Requirements
------------

* Python 3.9 or higher
* requests >= 2.25.0

Install from PyPI
-----------------

.. code-block:: bash

   pip install askpablos-api

Install from Source
-------------------

.. code-block:: bash

   git clone https://github.com/yourusername/askpablos-api.git
   cd askpablos-api
   pip install -e .

Verify Installation
-------------------

.. code-block:: python

   import askpablos_api
   print(askpablos_api.__version__)

Dependencies
------------

The package has minimal dependencies:

* **requests** - For HTTP communication

Development Installation
------------------------

For development, install with optional dependencies:

.. code-block:: bash

   pip install askpablos-api[dev]

This installs additional tools for testing and development:

* pytest - Testing framework
* black - Code formatting
* flake8 - Linting
* mypy - Type checking
