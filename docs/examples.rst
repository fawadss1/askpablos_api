Examples
========

This section provides practical examples of using the AskPablos API client for various scenarios.

Basic Usage Examples
-------------------

Simple GET Request
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import AskPablos

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Basic request
   response = client.get("https://httpbin.org/ip")
   print(f"Your IP: {response.content}")

Custom Headers and Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Request with custom headers and URL parameters
   response = client.get(
       "https://httpbin.org/headers",
       headers={"User-Agent": "AskPablosBot/1.0"},
       params={"foo": "bar"}
   )
   print(response.content)

Query Parameters
~~~~~~~~~~~~~~~~

.. note::
   The AskPablos client only supports GET requests. Use query parameters to pass data to the target URL.

.. code-block:: python

   # Pass parameters as query string
   params = {"name": "Alice", "age": "30"}
   response = client.get(
       "https://httpbin.org/get",
       params=params
   )
   print(response.content)

Timeout Configuration Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Quick timeout for fast APIs
   response = client.get(
       "https://api.example.com/status",
       timeout=5  # 5 seconds timeout
   )

   # Standard timeout for web pages
   response = client.get(
       "https://example.com",
       timeout=30  # 30 seconds (default)
   )

   # Extended timeout for slow sites
   response = client.get(
       "https://slow-loading-site.com",
       timeout=120  # 2 minutes timeout
   )

   # Browser mode with custom timeout
   response = client.get(
       "https://spa-app.com",
       browser=True,
       wait_for_load=True,
       timeout=90  # 90 seconds for JavaScript rendering
   )

Screenshot Capture
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Capture a screenshot of a web page using the get method
   response = client.get(
       "https://example.com",
       browser=True,  # Required for screenshot
       screenshot=True
   )

   # Screenshot data is available in the response
   if response.screenshot:
       with open("screenshot.png", "wb") as f:
           f.write(response.screenshot)

Browser Automation (JavaScript Rendering)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When browser=True is enabled, all browser-specific parameters (js_strategy, wait_for_load, screenshot) are always sent to the API server with their explicit values, ensuring precise control over browser behavior.

.. code-block:: python

   # Default browser behavior (recommended)
   response = client.get(
       "https://example.com/dynamic",
       browser=True,  # Required for js_strategy
       js_strategy="DEFAULT"  # Always sent when browser=True
   )

   # Stealth mode - runs stealth script & minimal JS
   response = client.get(
       "https://example.com/protected",
       browser=True,  # Required for js_strategy
       js_strategy=True  # Always sent when browser=True
   )

   # No JavaScript - faster for static content
   response = client.get(
       "https://example.com/static",
       browser=True,  # Required for js_strategy
       js_strategy=False  # Always sent when browser=True
   )

   print(response.content)

Waiting for Page Load
~~~~~~~~~~~~~~~~~~~~~

The wait_for_load parameter is always sent to the API when browser=True, ensuring the server knows your exact preference.

.. code-block:: python

   # Wait for page to fully load before capturing content
   response = client.get(
       "https://example.com/slow-loading",
       browser=True,  # Required for wait_for_load
       wait_for_load=True  # Always sent when browser=True
   )

   # Don't wait for page load (faster for simple pages)
   response = client.get(
       "https://example.com/fast-loading",
       browser=True,  # Required
       wait_for_load=False  # Always sent when browser=True
   )

   print(response.content)

Error Handling Example
---------------------

.. code-block:: python

   from askpablos_api import AskPablos, AskPablosError

   try:
       client = AskPablos(api_key="bad", secret_key="bad")
       client.get("https://httpbin.org/ip")
   except AskPablosError as e:
       print(f"API error: {e}")

Configuration Example
---------------------

.. code-block:: python

   # Basic client configuration with custom timeout
   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Set timeout per request
   response = client.get(
       "https://example.com",
       timeout=45  # Custom timeout in seconds
   )

   # Using environment variables for configuration
   import os

   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

   # Configure browser options for consistent behavior
   default_browser_options = {
       "browser": True,
       "wait_for_load": True,
       "js_strategy": "DEFAULT",
       "timeout": 60
   }

   response = client.get("https://example.com", **default_browser_options)

Advanced Use Cases
------------------

E-commerce Product Scraping
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Scrape dynamic product pages with screenshots
   products = [
       "https://shop.example.com/product/123",
       "https://shop.example.com/product/456"
   ]

   for i, product_url in enumerate(products):
       response = client.get(
           url=product_url,
           browser=True,
           wait_for_load=True,
           screenshot=True,
           rotate_proxy=True,
           timeout=60
       )

       # Save product data
       product_data = {
           "url": response.url,
           "status": response.status_code,
           "content_length": len(response.content)
       }

       # Save screenshot
       if response.screenshot:
           with open(f"product_{i+1}_screenshot.png", "wb") as f:
               f.write(response.screenshot)

       print(f"Product {i+1} scraped successfully")

API Testing with GET Requests Only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   The AskPablos client only supports GET requests. For other HTTP methods, you would need to use the lower-level ProxyClient directly.

.. code-block:: python

   # Only GET requests are supported with AskPablos client
   test_cases = [
       {
           "url": "https://httpbin.org/get",
           "params": {"test": "param"}
       },
       {
           "url": "https://httpbin.org/anything",
           "params": {"foo": "bar"}
       }
   ]

   for test in test_cases:
       response = client.get(
           test["url"],
           params=test.get("params")
       )
       print(f"GET request to {test['url']}: {response.status_code}")

Error Handling Examples
----------------------

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )

   def safe_request(url, **kwargs):
       """Make a safe request with proper error handling."""
       try:
           client = AskPablos(
               api_key="your_api_key",
               secret_key="your_secret_key"
           )

           response = client.get(url, **kwargs)
           return response

       except AuthenticationError as e:
           print(f"Authentication failed: {e}")
           return None
       except APIConnectionError as e:
           print(f"Connection error: {e}")
           return None
       except ResponseError as e:
           print(f"HTTP error: {e}")
           return None
       except ValueError as e:
           print(f"Invalid parameters: {e}")
           return None
       except Exception as e:
           print(f"Unexpected error: {e}")
           return None

   # Use the safe function
   response = safe_request(
       "https://example.com",
       browser=True,
       screenshot=True,
       timeout=30
   )

   if response:
       print(f"Success: {response.status_code}")

Parameter Validation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # This demonstrates parameter validation for browser dependencies
   def make_browser_request(url, take_screenshot=False):
       """Example of proper parameter usage."""

       # Correct: browser features require browser=True
       if take_screenshot:
           response = client.get(
               url=url,
               browser=True,      # Required for all browser features
               screenshot=True,   # Requires browser=True
               wait_for_load=True,# Requires browser=True
               js_strategy="DEFAULT"  # Requires browser=True
           )
       else:
           response = client.get(
               url=url,
               browser=True,
               wait_for_load=True
           )

       return response

   # These would all raise ValueError because browser=False
   try:
       # Error: wait_for_load requires browser=True
       response = client.get(
           url="https://example.com",
           browser=False,
           wait_for_load=True
       )
   except ValueError as e:
       print(f"Parameter error: {e}")

   try:
       # Error: screenshot requires browser=True
       response = client.get(
           url="https://example.com",
           browser=False,
           screenshot=True
       )
   except ValueError as e:
       print(f"Parameter error: {e}")

   try:
       # Error: js_strategy requires browser=True
       response = client.get(
           url="https://example.com",
           browser=False,
           js_strategy=True
       )
   except ValueError as e:
       print(f"Parameter error: {e}")

   # Correct usage - all browser features together
   response = client.get(
       url="https://example.com",
       browser=True,           # Required for all below features
       wait_for_load=True,     # Browser feature
       screenshot=True,        # Browser feature
       js_strategy="DEFAULT"   # Browser feature
   )

Performance Optimization
-----------------------

Smart Timeout Management
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def adaptive_request(url, is_spa=False, needs_screenshot=False):
       """Adjust timeouts based on request type."""

       if is_spa or needs_screenshot:
           # Longer timeout for browser-heavy operations
           timeout = 60
           browser_options = {
               "browser": True,
               "wait_for_load": True,
               "js_strategy": "DEFAULT"
           }
       else:
           # Shorter timeout for simple requests
           timeout = 15
           browser_options = {}

       if needs_screenshot:
           browser_options["screenshot"] = True

       response = client.get(
           url=url,
           timeout=timeout,
           **browser_options
       )

       return response

   # Usage examples
   static_page = adaptive_request("https://static-site.com")
   spa_page = adaptive_request("https://react-app.com", is_spa=True)
   screenshot_page = adaptive_request(
       "https://dashboard.com",
       is_spa=True,
       needs_screenshot=True
   )
