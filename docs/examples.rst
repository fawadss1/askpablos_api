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
       url="https://api.example.com/search",
       params={
           "q": "python",
           "limit": "10",
           "page": "1"
       },
       headers={
           "User-Agent": "MyApp/1.0",
           "Accept": "application/json",
           "Authorization": "Bearer your-token"
       }
   )

   print(f"Search results: {response.json}")

Browser Mode Examples
--------------------

JavaScript Rendering
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Render JavaScript-heavy pages
   response = client.get(
       url="https://spa-example.com",
       browser=True,
       wait_for_load=True,
       timeout=45
   )

   print(f"Rendered content: {response.content}")

Taking Screenshots
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Capture screenshots of web pages
   response = client.get(
       url="https://example.com",
       browser=True,
       screenshot=True,
       wait_for_load=True
   )

   if response.screenshot:
       with open("page_screenshot.png", "wb") as f:
           f.write(response.screenshot)
       print("Screenshot saved successfully!")

JavaScript Strategy Control
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Fine-tune JavaScript execution

   # Minimal JavaScript (stealth + basic JS)
   response = client.get(
       url="https://protected-site.com",
       browser=True,
       js_strategy=True,
       wait_for_load=True
   )

   # No JavaScript execution
   response = client.get(
       url="https://simple-site.com",
       browser=True,
       js_strategy=False
   )

   # Default strategy (balanced approach)
   response = client.get(
       url="https://normal-site.com",
       browser=True,
       js_strategy="DEFAULT"
   )

Proxy Rotation Examples
----------------------

Avoiding Rate Limits
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use proxy rotation for multiple requests
   urls = [
       "https://api.example.com/data/1",
       "https://api.example.com/data/2",
       "https://api.example.com/data/3"
   ]

   results = []
   for url in urls:
       response = client.get(
           url=url,
           rotate_proxy=True,
           timeout=30
       )
       results.append(response.json)
       print(f"Fetched data from {url}")

All Browser Features Combined
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use all browser features together
   response = client.get(
       url="https://advanced-webapp.com",
       browser=True,
       rotate_proxy=True,
       wait_for_load=True,
       screenshot=True,
       js_strategy="DEFAULT",
       timeout=45
   )

   print(f"Status: {response.status_code}")
   print(f"Content length: {len(response.content)}")
   print(f"Request time: {response.elapsed_time}")

   if response.screenshot:
       with open("webapp_screenshot.png", "wb") as f:
           f.write(response.screenshot)
       print("Screenshot captured and saved!")

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

API Testing with Different Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import ProxyClient

   # Use ProxyClient for more control
   client = ProxyClient(
       api_key="your_api_key",
       secret_key="your_secret_key",
       api_url="https://api.askpablos.com/proxy"
   )

   # Test different HTTP methods
   test_cases = [
       {
           "method": "GET",
           "url": "https://httpbin.org/get",
           "params": {"test": "param"}
       },
       {
           "method": "POST",
           "url": "https://httpbin.org/post",
           "data": {"key": "value"}
       }
   ]

   for test in test_cases:
       response = client.request(
           method=test["method"],
           url=test["url"],
           data=test.get("data"),
           params=test.get("params"),
           options={"rotate_proxy": True}
       )
       print(f"{test['method']} request: {response.status_code}")

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

   # This demonstrates parameter validation
   def make_browser_request(url, take_screenshot=False):
       """Example of proper parameter usage."""

       # Correct: browser features require browser=True
       if take_screenshot:
           response = client.get(
               url=url,
               browser=True,  # Required for screenshot
               screenshot=True,
               wait_for_load=True
           )
       else:
           response = client.get(
               url=url,
               browser=True,
               wait_for_load=True
           )

       return response

   # This would raise ValueError
   try:
       response = client.get(
           url="https://example.com",
           browser=False,  # Browser disabled
           screenshot=True  # But screenshot requested
       )
   except ValueError as e:
       print(f"Parameter error: {e}")

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
