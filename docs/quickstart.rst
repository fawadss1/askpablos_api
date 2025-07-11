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
   # Content: b'{"origin": "123.456.789.0"}'
   # Headers: {'content-type': 'application/json', ...}

Working with Response Data
--------------------------

The client returns a ``ResponseData`` object with convenient attributes:

.. code-block:: python

   response = client.get("https://httpbin.org/json")

   # Access response properties
   print(f"Status: {response.status_code}")
   print(f"URL: {response.url}")
   print(f"Time taken: {response.elapsed_time}")
   print(f"Encoding: {response.encoding}")

   # For JSON responses, access parsed data
   if response.json:
       print(f"JSON data: {response.json}")

Adding Custom Headers and Parameters
-----------------------------------

.. code-block:: python

   # Request with custom headers and URL parameters
   response = client.get(
       url="https://httpbin.org/headers",
       headers={
           "User-Agent": "MyApp/1.0",
           "Accept": "application/json",
           "Custom-Header": "custom-value"
       },
       params={
           "page": "1",
       }
   )

Request Timeouts
---------------

The AskPablos API client supports configurable timeouts for requests. The timeout parameter controls how long the server will wait for the target website to respond before timing out.

**Basic Timeout Configuration**

.. code-block:: python

   # Set a custom timeout (default is 30 seconds)
   response = client.get(
       url="https://slow-website.com",
       timeout=60  # Wait up to 60 seconds
   )

**Timeout for Different Use Cases**

.. code-block:: python

   # Quick timeout for fast APIs
   response = client.get(
       url="https://api.example.com/health",
       timeout=10  # 10 seconds should be enough for API calls
   )

   # Longer timeout for complex web scraping
   response = client.get(
       url="https://heavy-website.com",
       browser=True,
       wait_for_load=True,
       timeout=120  # 2 minutes for complex JavaScript rendering
   )

   # Very long timeout for data processing endpoints
   response = client.get(
       url="https://data-processor.com/generate-report",
       timeout=300  # 5 minutes for heavy data processing
   )

**Timeout Error Handling**

.. code-block:: python

   from askpablos_api.exceptions import RequestTimeoutError

   try:
       response = client.get(
           url="https://slow-website.com",
           timeout=30
       )
   except RequestTimeoutError as e:
       print(f"Request timed out: {e}")
       # Handle timeout by retrying with longer timeout
       response = client.get(
           url="https://slow-website.com",
           timeout=60
       )

Using Browser Mode
-----------------

For JavaScript-heavy websites, enable browser mode:

.. code-block:: python

   # Enable browser mode for JavaScript rendering
   response = client.get(
       url="https://example-spa.com",
       browser=True,
       wait_for_load=True,
       timeout=45
   )

   print(f"Rendered content: {response.content}")

Advanced Browser Features
-------------------------

The browser mode supports several advanced features:

**Taking Screenshots**

.. code-block:: python

   # Take a screenshot of the page
   response = client.get(
       url="https://example.com",
       browser=True,
       screenshot=True
   )

   # Save the screenshot
   if response.screenshot:
       with open("screenshot.png", "wb") as f:
           f.write(response.screenshot)

**JavaScript Strategy Control**

.. code-block:: python

   # Default strategy - optimized browser behavior (recommended)
   response = client.get(
       url="https://example.com",
       browser=True,
       js_strategy="DEFAULT",  # Full JavaScript support
       wait_for_load=True
   )

   # Stealth mode - runs stealth script & minimal JS
   response = client.get(
       url="https://protected-site.com",
       browser=True,
       js_strategy=True,  # Bypasses bot detection
       wait_for_load=True
   )

   # No JavaScript - fastest performance
   response = client.get(
       url="https://static-content.com",
       browser=True,
       js_strategy=False,  # No JS execution
       wait_for_load=True
   )

**Proxy Rotation**

.. code-block:: python

   # Use proxy rotation to avoid rate limiting
   response = client.get(
       url="https://example.com",
       rotate_proxy=True,
       timeout=60


Combining Multiple Options
-------------------------

.. code-block:: python

   # Advanced request with multiple options
   response = client.get(
       url="https://complex-site.com/data",
       params={"category": "tech", "sort": "date"},
       headers={"Authorization": "Bearer token123"},
       browser=True,
       wait_for_load=True,
       screenshot=True,
       js_strategy="DEFAULT",
       rotate_proxy=True,
       timeout=60,
       # Additional options can be passed via **options
       user_agent="Custom-Bot/1.0",
       cookies={"session": "abc123"}
   )

   print(f"Status: {response.status_code}")
   print(f"Content length: {len(response.content)}")

   if response.screenshot:
       print("Screenshot captured successfully")
Error Handling
--------------

Always handle potential errors in your code:

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AskPablos,
       AuthenticationError,
       APIConnectionError,
   )

   try:
       client = AskPablos(
           api_key="your_api_key",
           secret_key="your_secret_key"
       )
       response = client.get("https://example.com")

       response = client.get(
           url="https://example.com",
           browser=True,
           timeout=30
       )

       print(f"Success: {response.status_code}")

       print(f"Authentication failed: {e}")
   except APIConnectionError as e:
       print(f"Connection error: {e}")
   except ResponseError as e:
       print(f"HTTP error: {e}")
   except Exception as e:
   except ValueError as e:
       print(f"Invalid parameters: {e}")
       print(f"Unexpected error: {e}")

Setting Up Logging
Parameter Validation
-------------------

The client validates browser-specific options:

.. code-block:: python

   # This will raise ValueError - browser features require browser=True
   try:
       response = client.get(
           url="https://example.com",
           browser=False,  # Browser mode disabled
           screenshot=True  # But screenshot requested
       )
   except ValueError as e:
       print(f"Error: {e}")
       # Output: browser=True is required for these actions: screenshot=True

Best Practices
--------------

1. **Keep credentials secure**: Store API keys in environment variables
2. **Handle timeouts**: Set appropriate timeouts for your use case
3. **Use browser mode sparingly**: Only when JavaScript rendering is needed
4. **Enable proxy rotation**: For high-volume scraping to avoid rate limits
5. **Handle errors gracefully**: Always implement proper error handling

.. code-block:: python

   import os
   from askpablos_api import AskPablos

   # Secure credential handling
   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

   # Optimized request for static content
   response = client.get(
       url="https://api.example.com/data",
       headers={"Accept": "application/json"},
       timeout=15  # Shorter timeout for API endpoints
   )

   # Optimized request for dynamic content
   response = client.get(
       url="https://spa-example.com",
       browser=True,
       wait_for_load=True,
       js_strategy="DEFAULT",
       timeout=45  # Longer timeout for browser rendering
   )
