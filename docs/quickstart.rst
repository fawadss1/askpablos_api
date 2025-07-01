Quick Start Guide
================

This guide will help you get started with the AskPablos API client in just a few minutes.

Installation
------------

Install the package using pip:

.. code-block:: bash

   pip install askpablos-api

Basic Setup
-----------

First, import the client and create an instance:

.. code-block:: python

   from askpablos_api import AskPablos

   # Initialize the client with your credentials
   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

Authentication
--------------

The AskPablos API uses HMAC-SHA256 signature-based authentication. You need two credentials:

1. **API Key**: Your unique identifier from the AskPablos dashboard
2. **Secret Key**: Your private signing key for HMAC authentication

.. code-block:: python

   # These credentials should be kept secure
   client = AskPablos(
       api_key="ak_1234567890abcdef",
       secret_key="sk_abcdef1234567890"
   )

Making Your First Request
-------------------------

.. code-block:: python

   # Simple GET request
   response = client.get("https://httpbin.org/ip")

   # Print response details
   print(f"Status Code: {response.status_code}")
   print(f"Content: {response.content}")
   print(f"Headers: {response.headers}")

   # Expected output:
   # Status Code: 200
   # Content: {"origin": "123.456.789.0"}
   # Headers: {'content-type': 'application/json', ...}

Working with Response Data
--------------------------

The client returns a ``ResponseData`` object with convenient attributes:

.. code-block:: python

   response = client.get("https://httpbin.org/json")

   # Access response properties
   print(f"Status: {response.status_code}")
   print(f"URL: {response.url}")
   print(f"Time taken: {response.elapsed} seconds")
   print(f"Encoding: {response.encoding}")

   # For JSON responses, access parsed data
   if response.json:
       print(f"JSON data: {response.json}")

Adding Custom Headers
--------------------

.. code-block:: python

   # Request with custom headers
   response = client.get(
       url="https://httpbin.org/headers",
       headers={
           "User-Agent": "MyApp/1.0",
           "Accept": "application/json",
           "Custom-Header": "custom-value"
       }
   )

Using Browser Mode
-----------------

For JavaScript-heavy websites, enable browser mode:

.. code-block:: python

   # Enable browser mode for JavaScript rendering
   response = client.get(
       url="https://example.com/spa-app",
       use_browser=True,
       timeout=30
   )

Error Handling
--------------

Always handle potential errors in your code:

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )

   try:
       client = AskPablos(
           api_key="your_api_key",
           secret_key="your_secret_key"
       )
       response = client.get("https://example.com")

       if response.status_code == 200:
           print("Success!")
           print(response.content)

   except AuthenticationError as e:
       print(f"Authentication failed: {e}")
   except APIConnectionError as e:
       print(f"Connection error: {e}")
   except ResponseError as e:
       print(f"HTTP error: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Setting Up Logging
------------------

Enable logging to debug your requests:

.. code-block:: python

   from askpablos_api import configure_logging
   import logging

   # Enable debug logging for the library
   configure_logging(level="DEBUG")

   # Or configure manually
   logger = logging.getLogger("askpablos_api")
   logger.setLevel(logging.INFO)

   # Create console handler
   handler = logging.StreamHandler()
   formatter = logging.Formatter(
       '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   handler.setFormatter(formatter)
   logger.addHandler(handler)

Complete Example
---------------

Here's a complete example that demonstrates all the key features:

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       configure_logging,
       AuthenticationError
   )

   # Enable logging
   configure_logging(level="INFO")

   try:
       # Initialize client
       client = AskPablos(
           api_key="your_api_key",
           secret_key="your_secret_key"
       )

       # Make a request with all options
       response = client.get(
           url="https://httpbin.org/user-agent",
           headers={
               "User-Agent": "AskPablos-Client/1.0",
               "Accept": "application/json"
           },
           use_browser=False,
           timeout=30
       )

       # Process response
       if response.status_code == 200:
           print(f"✅ Request successful!")
           print(f"Response time: {response.elapsed:.2f}s")

           if response.json:
               print(f"JSON data: {response.json}")
           else:
               print(f"Content: {response.content[:200]}...")
       else:
           print(f"❌ Request failed with status {response.status_code}")

   except AuthenticationError:
       print("❌ Please check your API credentials")
   except Exception as e:
       print(f"❌ Error: {e}")

Next Steps
----------

Now that you're up and running:

1. Check out the :doc:`examples` for more practical use cases
2. Read the :doc:`api_reference` for detailed API documentation
3. Learn about :doc:`error_handling` for robust error management
4. Configure logging for better debugging and monitoring

Environment Variables
---------------------

For production use, consider storing your credentials in environment variables:

.. code-block:: python

   import os
   from askpablos_api import AskPablos

   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )
