Examples
========

This section provides practical examples of using the AskPablos API client for various scenarios.

Basic Web Scraping
-------------------

Simple Page Fetching
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import AskPablos

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Fetch a simple webpage
   response = client.get("https://example.com")
   html_content = response["content"]
   print(f"Status: {response['status_code']}")
   print(f"Content length: {len(html_content)}")

JavaScript-Heavy Sites
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # For single-page applications or dynamic content
   response = client.get(
       "https://spa-website.com",
       browser=True,
       timeout=60  # Allow more time for JS rendering
   )

   rendered_html = response["content"]

API Integration
---------------

REST API Calls
~~~~~~~~~~~~~~~

.. code-block:: python

   # Fetch data from a REST API
   response = client.get("https://jsonplaceholder.typicode.com/users")
   users = response["content"]  # JSON string

   # Parse JSON if needed
   import json
   users_data = json.loads(users)
   print(f"Found {len(users_data)} users")

API with Authentication
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # API requiring bearer token
   response = client.get(
       "https://api.example.com/protected/data",
       headers={"Authorization": "Bearer your_access_token"}
   )

API with Query Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Search API with pagination
   response = client.get(
       "https://api.example.com/search",
       params={
           "q": "python programming",
           "page": 1,
           "per_page": 20,
           "sort": "relevance"
       }
   )

Advanced Options
----------------

Custom User Agent
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   response = client.get(
       "https://example.com",
       user_agent="Mozilla/5.0 (Custom Bot 1.0)"
   )

Session Management with Cookies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Step 1: Login (if needed through another service)
   # Step 2: Use session cookies
   response = client.get(
       "https://example.com/protected",
       cookies={
           "session_id": "abc123def456",
           "csrf_token": "xyz789"
       }
   )

Disable Proxy Rotation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use the same proxy for consistency
   response = client.get(
       "https://example.com",
       rotate_proxy=False
   )

Error Handling Examples
-----------------------

Robust Request Handling
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )
   import time

   def make_robust_request(url, max_retries=3):
       """Make a request with retry logic."""

       client = AskPablos(
           api_key="your_api_key",
           secret_key="your_secret_key"
       )

       for attempt in range(max_retries):
           try:
               response = client.get(url)
               return response

           except APIConnectionError as e:
               print(f"Connection failed (attempt {attempt + 1}): {e}")
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Exponential backoff
               else:
                   raise

           except ResponseError as e:
               if e.status_code == 429:  # Rate limited
                   print("Rate limited, waiting...")
                   time.sleep(60)
                   continue
               elif e.status_code >= 500:  # Server error
                   print(f"Server error {e.status_code}, retrying...")
                   time.sleep(5)
                   continue
               else:
                   raise  # Client error, don't retry

   # Usage
   try:
       response = make_robust_request("https://api.example.com/data")
       print("Success:", response["status_code"])
   except Exception as e:
       print(f"Failed after retries: {e}")

Logging and Debugging
---------------------

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import configure_logging, AskPablos
   import logging

   # Enable detailed logging
   configure_logging(level=logging.DEBUG)

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # All requests will now be logged with details
   response = client.get("https://httpbin.org/ip")

Custom Logging Format
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import configure_logging
   import logging

   # Custom log format
   configure_logging(
       level=logging.INFO,
       format_string="[%(asctime)s] %(levelname)s: %(message)s"
   )

Performance Optimization
------------------------

Reuse Client Instance
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Good: Reuse the same client
   client = AskPablos(api_key="...", secret_key="...")

   urls = [
       "https://api.example.com/endpoint1",
       "https://api.example.com/endpoint2",
       "https://api.example.com/endpoint3"
   ]

   responses = []
   for url in urls:
       response = client.get(url)
       responses.append(response)

Batch Processing with Rate Limiting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from askpablos_api import AskPablos

   def process_urls_with_rate_limit(urls, requests_per_second=1):
       """Process multiple URLs with rate limiting."""

       client = AskPablos(api_key="...", secret_key="...")
       delay = 1.0 / requests_per_second

       results = []
       for i, url in enumerate(urls):
           try:
               response = client.get(url)
               results.append({"url": url, "response": response})
               print(f"Processed {i+1}/{len(urls)}: {url}")

           except Exception as e:
               results.append({"url": url, "error": str(e)})
               print(f"Failed {i+1}/{len(urls)}: {url} - {e}")

           # Rate limiting
           if i < len(urls) - 1:  # Don't sleep after last request
               time.sleep(delay)

       return results

   # Usage
   urls_to_scrape = [
       "https://example1.com",
       "https://example2.com",
       "https://example3.com"
   ]

   results = process_urls_with_rate_limit(urls_to_scrape, requests_per_second=0.5)

Real-World Use Cases
--------------------

Website Status Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def check_website_status(urls):
       """Monitor multiple websites for availability."""

       client = AskPablos(api_key="...", secret_key="...")

       for url in urls:
           try:
               response = client.get(url, timeout=10)
               status = response["status_code"]
               time_taken = response["time_taken"]

               if status == 200:
                   print(f"✅ {url} - OK ({time_taken:.2f}s)")
               else:
                   print(f"⚠️  {url} - Status {status}")

           except Exception as e:
               print(f"❌ {url} - Error: {e}")

   # Monitor websites
   websites = [
       "https://example.com",
       "https://api.service.com/health",
       "https://status.company.com"
   ]

   check_website_status(websites)

Data Collection Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from datetime import datetime

   def collect_api_data(endpoints):
       """Collect data from multiple API endpoints."""

       client = AskPablos(api_key="...", secret_key="...")
       collected_data = {
           "timestamp": datetime.now().isoformat(),
           "results": []
       }

       for endpoint in endpoints:
           try:
               response = client.get(
                   endpoint["url"],
                   headers=endpoint.get("headers", {}),
                   params=endpoint.get("params", {})
               )

               collected_data["results"].append({
                   "endpoint": endpoint["name"],
                   "status": "success",
                   "data": json.loads(response["content"]),
                   "response_time": response["time_taken"]
               })

           except Exception as e:
               collected_data["results"].append({
                   "endpoint": endpoint["name"],
                   "status": "error",
                   "error": str(e)
               })

       return collected_data

   # Data collection configuration
   api_endpoints = [
       {
           "name": "user_stats",
           "url": "https://api.example.com/stats/users",
           "headers": {"Authorization": "Bearer token123"}
       },
       {
           "name": "sales_data",
           "url": "https://api.example.com/sales",
           "params": {"period": "daily"}
       }
   ]

   data = collect_api_data(api_endpoints)
   print(json.dumps(data, indent=2))
