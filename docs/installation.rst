Installation
============

System Requirements
-------------------

* **Python**: 3.9 or higher
* **Operating System**: Windows, macOS, Linux
* **Dependencies**: requests >= 2.25.0

The AskPablos API client has minimal dependencies to keep your environment clean and avoid conflicts.

Installation Methods
--------------------

Install from PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install the AskPablos API client is using pip:

.. code-block:: bash

   pip install askpablos-api

This will install the latest stable version from the Python Package Index (PyPI).

Install Specific Version
~~~~~~~~~~~~~~~~~~~~~~~~

To install a specific version:

.. code-block:: bash

   pip install askpablos-api==0.1.0

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade askpablos-api

Install from Source
~~~~~~~~~~~~~~~~~~~

For development or to get the latest features:

.. code-block:: bash

   git clone https://github.com/fawadss1/askpablos_api.git
   cd askpablos-api
   pip install -e .

The `-e` flag installs in "editable" mode, so changes to the source code are immediately reflected.

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For contributors or developers who want to run tests and build documentation:

.. code-block:: bash

   git clone https://github.com/fawadss1/askpablos_api.git
   cd askpablos-api
   pip install -e ".[dev]"


This installs additional development dependencies including:

* pytest for testing
* pytest-cov for coverage reports
* black for code formatting
* flake8 for linting
* sphinx for documentation
* twine for publishing

Virtual Environment Setup
-------------------------

It's recommended to use a virtual environment to avoid dependency conflicts:

Using venv (Python 3.3+)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create virtual environment
   python -m venv askpablos-env

   # Activate on Windows
   askpablos-env\Scripts\activate

   # Activate on macOS/Linux
   source askpablos-env/bin/activate

   # Install the package
   pip install askpablos-api

Using conda
~~~~~~~~~~~

.. code-block:: bash

   # Create conda environment
   conda create -n askpablos-env python=3.9

   # Activate environment
   conda activate askpablos-env

   # Install the package
   pip install askpablos-api

Using pipenv
~~~~~~~~~~~~

.. code-block:: bash

   # Create Pipfile and install
   pipenv install askpablos-api

   # Activate shell
   pipenv shell

Verify Installation
-------------------

Test Basic Import
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import askpablos_api
   print(f"AskPablos API version: {askpablos_api.__version__}")

Test Client Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import AskPablos

   # This should not raise any errors
   try:
       client = AskPablos(api_key="test", secret_key="test")
       print("✅ Client created successfully")
   except Exception as e:
       print(f"❌ Installation issue: {e}")

Check Available Classes
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       ProxyClient,
       AuthenticationError,
       APIConnectionError,
       ResponseError,
       configure_logging
   )

   print("✅ All components imported successfully")

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

For production deployments, set up environment variables:

**Windows (Command Prompt):**

.. code-block:: batch

   set ASKPABLOS_API_KEY=your_api_key_here
   set ASKPABLOS_SECRET_KEY=your_secret_key_here

**Windows (PowerShell):**

.. code-block:: powershell

   $env:ASKPABLOS_API_KEY="your_api_key_here"
   $env:ASKPABLOS_SECRET_KEY="your_secret_key_here"

**macOS/Linux (Bash):**

.. code-block:: bash

   export ASKPABLOS_API_KEY="your_api_key_here"
   export ASKPABLOS_SECRET_KEY="your_secret_key_here"

**Using .env file:**

Create a `.env` file in your project root:

.. code-block:: text

   ASKPABLOS_API_KEY=your_api_key_here
   ASKPABLOS_SECRET_KEY=your_secret_key_here

Then load it in your Python code:

.. code-block:: python

   import os
   from dotenv import load_dotenv  # pip install python-dotenv
   from askpablos_api import AskPablos

   # Load environment variables
   load_dotenv()

   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

Docker Installation
-------------------

Using Docker for isolated deployment:

**Dockerfile:**

.. code-block:: dockerfile

   FROM python:3.9-slim

   WORKDIR /app

   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Install askpablos-api
   RUN pip install askpablos-api

   # Copy application
   COPY . .

   CMD ["python", "your_app.py"]

**requirements.txt:**

.. code-block:: text

   askpablos-api>=0.1.0
   python-dotenv>=0.19.0

**docker-compose.yml:**

.. code-block:: yaml

   version: '3.8'
   services:
     app:
       build: .
       environment:
         - ASKPABLOS_API_KEY=${ASKPABLOS_API_KEY}
         - ASKPABLOS_SECRET_KEY=${ASKPABLOS_SECRET_KEY}
       volumes:
         - .:/app

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'askpablos_api'**

Solution:

.. code-block:: bash

   pip install askpablos-api

**SSL Certificate Errors**

On some systems, you might encounter SSL errors. Try:

.. code-block:: bash

   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org askpablos-api

**Permission Denied (Windows)**

Run Command Prompt or PowerShell as Administrator:

.. code-block:: bash

   # Alternative: Install for current user only
   pip install --user askpablos-api

**Python Version Compatibility**

Ensure you're using Python 3.9 or higher:

.. code-block:: bash

   python --version
   # or
   python3 --version

**Proxy/Firewall Issues**

If behind a corporate firewall:

.. code-block:: bash

   pip install --proxy http://proxy.company.com:8080 askpablos-api

Network Connectivity Test
~~~~~~~~~~~~~~~~~~~~~~~~~

Test if you can reach the required endpoints:

.. code-block:: python

   import requests

   try:
       response = requests.get("https://httpbin.org/ip", timeout=10)
       print(f"✅ Network connectivity OK: {response.status_code}")
   except Exception as e:
       print(f"❌ Network issue: {e}")

Version Compatibility
~~~~~~~~~~~~~~~~~~~~~

Check compatibility with your Python version:

.. code-block:: python

   import sys

   python_version = sys.version_info
   print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")

   if python_version >= (3, 9):
       print("✅ Python version compatible")
   else:
       print("❌ Python 3.9+ required")

Next Steps
----------

After successful installation:

1. **Get API Credentials**: Sign up at the AskPablos dashboard to get your API key and secret key
2. **Read the Quick Start**: Check the :doc:`quickstart` guide for your first API call
3. **Explore Examples**: Review :doc:`examples` for practical use cases
4. **Set Up Error Handling**: Learn about :doc:`error_handling` for robust applications

Support
-------

If you encounter installation issues:

- **Documentation**: Check the troubleshooting section above
- **GitHub Issues**: Report bugs at the project's GitHub repository
- **Email Support**: Contact fawadstar6@gmail.com for assistance

**System Information for Support**

When reporting issues, include:

.. code-block:: python

   import sys
   import platform
   import askpablos_api

   print(f"Python: {sys.version}")
   print(f"Platform: {platform.platform()}")
   print(f"AskPablos API: {askpablos_api.__version__}")

   # Check requests version
   import requests
   print(f"Requests: {requests.__version__}")
