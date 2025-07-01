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
   print(f"Status: {response.status_code}")
   print(f"Content length: {len(response.content)}")
   print(f"Response time: {response.elapsed:.2f}s")

Fetching with Custom Headers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Request with custom User-Agent and headers
   response = client.get(
       url="https://httpbin.org/headers",
       headers={
           "User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0)",
           "Accept": "text/html,application/xhtml+xml",
           "Accept-Language": "en-US,en;q=0.9"
       }
   )

   print("Request headers sent:")
   if response.json:
       headers_sent = response.json.get("headers", {})
       for key, value in headers_sent.items():
           print(f"  {key}: {value}")

JavaScript-Heavy Sites
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # For single-page applications or dynamic content
   response = client.get(
       url="https://spa-website.com",
       use_browser=True,
       timeout=60  # Allow more time for JS rendering
   )

   rendered_html = response.content
   print(f"Rendered content length: {len(rendered_html)}")

API Integration
---------------

REST API Calls
~~~~~~~~~~~~~~~

.. code-block:: python

   # Fetch data from a REST API
   response = client.get("https://jsonplaceholder.typicode.com/users")

   if response.status_code == 200 and response.json:
       users = response.json
       print(f"Found {len(users)} users:")
       for user in users[:3]:  # Show first 3 users
           print(f"  - {user['name']} ({user['email']})")
   else:
       print(f"Failed to fetch users: {response.status_code}")

Working with JSON APIs
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get current IP information
   response = client.get("https://httpbin.org/ip")

   if response.json:
       ip_info = response.json
       print(f"Your IP through proxy: {ip_info['origin']}")

   # Get request information
   response = client.get("https://httpbin.org/get")
   if response.json:
       request_info = response.json
       print(f"Request URL: {request_info['url']}")
       print(f"Request args: {request_info['args']}")

Error Handling Examples
-----------------------

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )
   import logging

   # Set up logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   def safe_request(url, max_retries=3):
       """Make a request with retry logic and proper error handling."""

       try:
           client = AskPablos(
               api_key="your_api_key",
               secret_key="your_secret_key"
           )
       except AuthenticationError as e:
           logger.error(f"Authentication failed: {e}")
           return None

       for attempt in range(max_retries):
           try:
               response = client.get(url, timeout=30)

               if response.status_code == 200:
                   logger.info(f"Successfully fetched {url}")
                   return response
               else:
                   logger.warning(f"HTTP {response.status_code} for {url}")

           except APIConnectionError as e:
               logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
               if attempt == max_retries - 1:
                   logger.error(f"Failed to connect to {url} after {max_retries} attempts")

           except ResponseError as e:
               logger.error(f"Response error for {url}: {e}")
               break

           except Exception as e:
               logger.error(f"Unexpected error: {e}")
               break

       return None

   # Usage
   response = safe_request("https://example.com")
   if response:
       print(f"Content: {response.content[:100]}...")

Batch Processing
----------------

Processing Multiple URLs
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from concurrent.futures import ThreadPoolExecutor, as_completed

   def fetch_url(client, url):
       """Fetch a single URL and return result."""
       try:
           response = client.get(url, timeout=30)
           return {
               "url": url,
               "status_code": response.status_code,
               "content_length": len(response.content),
               "elapsed": response.elapsed,
               "success": response.status_code == 200
           }
       except Exception as e:
           return {
               "url": url,
               "error": str(e),
               "success": False
           }

   def batch_fetch(urls, max_workers=5):
       """Fetch multiple URLs concurrently."""
       client = AskPablos(
           api_key="your_api_key",
           secret_key="your_secret_key"
       )

       results = []

       with ThreadPoolExecutor(max_workers=max_workers) as executor:
           # Submit all tasks
           future_to_url = {
               executor.submit(fetch_url, client, url): url
               for url in urls
           }

           # Collect results as they complete
           for future in as_completed(future_to_url):
               result = future.result()
               results.append(result)

               if result["success"]:
                   print(f"✅ {result['url']} - {result['status_code']} ({result['elapsed']:.2f}s)")
               else:
                   print(f"❌ {result['url']} - {result.get('error', 'Failed')}")

       return results

   # Usage
   urls = [
       "https://httpbin.org/delay/1",
       "https://httpbin.org/status/200",
       "https://httpbin.org/json",
       "https://example.com"
   ]

   results = batch_fetch(urls)

   # Summary
   successful = sum(1 for r in results if r["success"])
   print(f"\nResults: {successful}/{len(results)} successful")

Advanced Usage
--------------

Custom Proxy Client
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import ProxyClient

   # Use the lower-level ProxyClient for advanced control
   client = ProxyClient(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Direct request with custom options
   response = client.request(
       method="GET",
       url="https://example.com",
       headers={"Accept": "application/json"},
       options={
           "use_browser": True,
           "timeout": 45,
           "custom_option": "value"
       }
   )

   print(f"Response: {response.status_code}")

Rate Limiting and Delays
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from askpablos_api import AskPablos

   class RateLimitedClient:
       """Client wrapper with built-in rate limiting."""

       def __init__(self, api_key, secret_key, requests_per_minute=60):
           self.client = AskPablos(api_key=api_key, secret_key=secret_key)
           self.min_delay = 60.0 / requests_per_minute
           self.last_request_time = 0

       def get(self, url, **kwargs):
           """Make a rate-limited GET request."""
           # Calculate delay needed
           now = time.time()
           time_since_last = now - self.last_request_time

           if time_since_last < self.min_delay:
               delay = self.min_delay - time_since_last
               print(f"Rate limiting: waiting {delay:.2f}s...")
               time.sleep(delay)

           # Make the request
           response = self.client.get(url, **kwargs)
           self.last_request_time = time.time()

           return response

   # Usage
   client = RateLimitedClient(
       api_key="your_api_key",
       secret_key="your_secret_key",
       requests_per_minute=30  # 30 requests per minute
   )

   urls = ["https://httpbin.org/delay/1"] * 5
   for url in urls:
       response = client.get(url)
       print(f"Response {response.status_code} in {response.elapsed:.2f}s")

Data Extraction
---------------

HTML Parsing with BeautifulSoup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import AskPablos
   from bs4 import BeautifulSoup

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Fetch and parse HTML
   response = client.get("https://quotes.toscrape.com")

   if response.status_code == 200:
       soup = BeautifulSoup(response.content, 'html.parser')

       # Extract quotes
       quotes = soup.find_all('div', class_='quote')

       print(f"Found {len(quotes)} quotes:")
       for quote in quotes[:3]:
           text = quote.find('span', class_='text').get_text()
           author = quote.find('small', class_='author').get_text()
           print(f'"{text}" - {author}')

JSON Data Processing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Fetch and process JSON data
   response = client.get("https://jsonplaceholder.typicode.com/posts")

   if response.json:
       posts = response.json

       # Group posts by user
       posts_by_user = {}
       for post in posts:
           user_id = post['userId']
           if user_id not in posts_by_user:
               posts_by_user[user_id] = []
           posts_by_user[user_id].append(post['title'])

       # Show summary
       for user_id, titles in posts_by_user.items():
           print(f"User {user_id}: {len(titles)} posts")

Monitoring and Debugging
-------------------------

Request Logging
~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import AskPablos, configure_logging
   import logging

   # Configure detailed logging
   configure_logging(level="DEBUG")

   # Add custom logging
   logger = logging.getLogger(__name__)
   handler = logging.FileHandler('requests.log')
   formatter = logging.Formatter(
       '%(asctime)s - %(levelname)s - %(message)s'
   )
   handler.setFormatter(formatter)
   logger.addHandler(handler)

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   # Make requests with logging
   urls = ["https://httpbin.org/ip", "https://httpbin.org/user-agent"]

   for url in urls:
       logger.info(f"Requesting: {url}")
       response = client.get(url)
       logger.info(f"Response: {response.status_code} in {response.elapsed:.2f}s")

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from statistics import mean, median

   def benchmark_requests(urls, iterations=3):
       """Benchmark request performance."""
       client = AskPablos(
           api_key="your_api_key",
           secret_key="your_secret_key"
       )

       results = {}

       for url in urls:
           times = []
           status_codes = []

           print(f"Benchmarking {url}...")

           for i in range(iterations):
               start_time = time.time()
               response = client.get(url)
               elapsed = time.time() - start_time

               times.append(elapsed)
               status_codes.append(response.status_code)
               print(f"  Iteration {i+1}: {response.status_code} in {elapsed:.2f}s")

           results[url] = {
               "mean_time": mean(times),
               "median_time": median(times),
               "min_time": min(times),
               "max_time": max(times),
               "success_rate": sum(1 for code in status_codes if code == 200) / len(status_codes)
           }

       return results

   # Usage
   test_urls = [
       "https://httpbin.org/delay/1",
       "https://jsonplaceholder.typicode.com/posts/1"
   ]

   benchmark_results = benchmark_requests(test_urls)

   for url, stats in benchmark_results.items():
       print(f"\n{url}:")
       print(f"  Mean time: {stats['mean_time']:.2f}s")
       print(f"  Success rate: {stats['success_rate']:.1%}")

Environment-Specific Examples
-----------------------------

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from askpablos_api import AskPablos, configure_logging

   # Production setup with environment variables
   def create_production_client():
       # Configure logging for production
       configure_logging(level=os.getenv("LOG_LEVEL", "INFO"))

       # Get credentials from environment
       api_key = os.getenv("ASKPABLOS_API_KEY")
       secret_key = os.getenv("ASKPABLOS_SECRET_KEY")

       if not api_key or not secret_key:
           raise ValueError("Missing required environment variables")

       return AskPablos(api_key=api_key, secret_key=secret_key)

   # Usage in production
   try:
       client = create_production_client()
       response = client.get("https://api.example.com/data")
       # Process response...
   except ValueError as e:
       print(f"Configuration error: {e}")
   except Exception as e:
       print(f"Runtime error: {e}")

Testing Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Testing setup with mock responses
   from unittest.mock import patch, MagicMock

   def test_client_integration():
       """Example integration test."""
       with patch('askpablos_api.ProxyClient.request') as mock_request:
           # Mock successful response
           mock_response = MagicMock()
           mock_response.status_code = 200
           mock_response.content = '{"test": "data"}'
           mock_response.json = {"test": "data"}
           mock_request.return_value = mock_response

           # Test the client
           client = AskPablos(api_key="test", secret_key="test")
           response = client.get("https://test.com")

           assert response.status_code == 200
           assert response.json["test"] == "data"

   # Run test
   test_client_integration()
   print("✅ Integration test passed")
