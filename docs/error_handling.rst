Error Handling
==============

The AskPablos API client provides a comprehensive exception hierarchy to help you handle different types of errors that may occur during API interactions.

Exception Hierarchy
-------------------

.. code-block:: text

   AskPablosError (base)
   ├── AuthenticationError
   ├── APIConnectionError
   └── ResponseError

All exceptions inherit from ``AskPablosError``, allowing you to catch all API-related errors with a single exception handler if needed.

Exception Types
---------------

AskPablosError
~~~~~~~~~~~~~~

The base exception class for all AskPablos API errors.

.. code-block:: python

   from askpablos_api import AskPablosError

   try:
       response = client.get("https://example.com")
   except AskPablosError as e:
       print(f"An API error occurred: {e}")

AuthenticationError
~~~~~~~~~~~~~~~~~~~

Raised when there are problems with authentication credentials.

**Common causes:**
- Empty or missing API key
- Empty or missing secret key
- Invalid credentials
- HMAC signature verification failure

.. code-block:: python

   from askpablos_api import AskPablos, AuthenticationError

   try:
       client = AskPablos(api_key="", secret_key="")
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")
       # Handle credential errors

APIConnectionError
~~~~~~~~~~~~~~~~~~

Raised when the client cannot connect to the AskPablos API.

**Common causes:**
- Network connectivity issues
- DNS resolution failures
- Connection timeouts
- SSL/TLS certificate problems
- API server unavailable

.. code-block:: python

   from askpablos_api import APIConnectionError

   try:
       response = client.get("https://example.com")
   except APIConnectionError as e:
       print(f"Connection failed: {e}")
       # Implement retry logic

ResponseError
~~~~~~~~~~~~~

Raised when the API returns an HTTP error status code (4xx or 5xx).

**Attributes:**
- ``status_code`` - The HTTP status code
- ``message`` - The error message from the API

**Common status codes:**
- **400** - Bad Request (invalid parameters)
- **401** - Unauthorized (authentication failed)
- **403** - Forbidden (access denied)
- **404** - Not Found (endpoint not found)
- **429** - Too Many Requests (rate limited)
- **500** - Internal Server Error
- **503** - Service Unavailable

.. code-block:: python

   from askpablos_api import ResponseError

   try:
       response = client.get("https://httpbin.org/status/500")
   except ResponseError as e:
       print(f"API error {e.status_code}: {e.message}")

       if e.status_code == 429:
           print("Rate limited - wait before retrying")
       elif e.status_code >= 500:
           print("Server error - may be temporary")

Error Handling Patterns
-----------------------

Basic Error Handling
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )

   def safe_request(url):
       try:
           client = AskPablos(
               api_key="your_api_key",
               secret_key="your_secret_key"
           )
           return client.get(url)

       except AuthenticationError:
           print("Check your API credentials")
           return None

       except APIConnectionError:
           print("Network or connection problem")
           return None

       except ResponseError as e:
           print(f"API responded with error {e.status_code}")
           return None

Retry Logic with Exponential Backoff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import random

   def request_with_retry(url, max_retries=3, base_delay=1):
       """Make request with exponential backoff retry logic."""

       client = AskPablos(
           api_key="your_api_key",
           secret_key="your_secret_key"
       )

       for attempt in range(max_retries):
           try:
               return client.get(url)

           except APIConnectionError as e:
               if attempt == max_retries - 1:
                   raise  # Last attempt, re-raise the exception

               # Exponential backoff with jitter
               delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
               print(f"Connection failed, retrying in {delay:.1f}s...")
               time.sleep(delay)

           except ResponseError as e:
               if e.status_code == 429:  # Rate limited
                   if attempt == max_retries - 1:
                       raise

                   delay = base_delay * (2 ** attempt)
                   print(f"Rate limited, waiting {delay}s...")
                   time.sleep(delay)

               elif 500 <= e.status_code < 600:  # Server errors
                   if attempt == max_retries - 1:
                       raise

                   delay = base_delay * (2 ** attempt)
                   print(f"Server error {e.status_code}, retrying in {delay}s...")
                   time.sleep(delay)

               else:
                   # Client errors (4xx) - don't retry
                   raise

Rate Limiting Handler
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def handle_rate_limiting(func):
       """Decorator to handle rate limiting automatically."""

       def wrapper(*args, **kwargs):
           max_retries = 3
           base_delay = 60  # Start with 1 minute delay

           for attempt in range(max_retries):
               try:
                   return func(*args, **kwargs)

               except ResponseError as e:
                   if e.status_code == 429:
                       if attempt == max_retries - 1:
                           raise

                       delay = base_delay * (attempt + 1)
                       print(f"Rate limited. Waiting {delay} seconds...")
                       time.sleep(delay)
                   else:
                       raise

           return None

       return wrapper

   @handle_rate_limiting
   def fetch_data(url):
       client = AskPablos(api_key="...", secret_key="...")
       return client.get(url)

Circuit Breaker Pattern
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import datetime, timedelta

   class CircuitBreaker:
       """Simple circuit breaker for API calls."""

       def __init__(self, failure_threshold=5, recovery_timeout=300):
           self.failure_threshold = failure_threshold
           self.recovery_timeout = recovery_timeout
           self.failure_count = 0
           self.last_failure_time = None
           self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

       def can_execute(self):
           if self.state == 'CLOSED':
               return True
           elif self.state == 'OPEN':
               if (datetime.now() - self.last_failure_time).seconds > self.recovery_timeout:
                   self.state = 'HALF_OPEN'
                   return True
               return False
           else:  # HALF_OPEN
               return True

       def record_success(self):
           self.failure_count = 0
           self.state = 'CLOSED'

       def record_failure(self):
           self.failure_count += 1
           self.last_failure_time = datetime.now()

           if self.failure_count >= self.failure_threshold:
               self.state = 'OPEN'

   # Usage
   circuit_breaker = CircuitBreaker()

   def safe_api_call(url):
       if not circuit_breaker.can_execute():
           print("Circuit breaker is OPEN - skipping request")
           return None

       try:
           client = AskPablos(api_key="...", secret_key="...")
           response = client.get(url)
           circuit_breaker.record_success()
           return response

       except (APIConnectionError, ResponseError) as e:
           circuit_breaker.record_failure()
           print(f"Request failed: {e}")
           return None

Logging for Debugging
----------------------

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import configure_logging
   import logging

   # Enable debug logging to see detailed information
   configure_logging(level=logging.DEBUG)

   # Now all requests will be logged with full details
   client = AskPablos(api_key="...", secret_key="...")

   try:
       response = client.get("https://example.com")
   except Exception as e:
       # Error details will be in the logs
       print(f"Request failed: {e}")

Custom Error Handler
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from askpablos_api import configure_logging, AskPablosError

   # Set up custom logging
   configure_logging(
       level=logging.INFO,
       format_string="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
   )

   logger = logging.getLogger(__name__)

   def log_and_handle_error(func):
       """Decorator to log errors with context."""

       def wrapper(*args, **kwargs):
           try:
               return func(*args, **kwargs)
           except AskPablosError as e:
               logger.error(f"API error in {func.__name__}: {e}")
               # Add custom error handling logic here
               raise
           except Exception as e:
               logger.error(f"Unexpected error in {func.__name__}: {e}")
               raise

       return wrapper

   @log_and_handle_error
   def fetch_user_data(user_id):
       client = AskPablos(api_key="...", secret_key="...")
       return client.get(f"https://api.example.com/users/{user_id}")

Best Practices
--------------

1. **Always handle AuthenticationError** - Check credentials before making requests
2. **Implement retry logic** - For connection errors and server errors (5xx)
3. **Respect rate limits** - Handle 429 responses appropriately
4. **Don't retry client errors** - 4xx errors usually indicate invalid requests
5. **Use circuit breakers** - For protecting against cascading failures
6. **Log errors appropriately** - Include context but avoid logging sensitive data
7. **Set reasonable timeouts** - Don't let requests hang indefinitely
8. **Monitor error rates** - Track failures to identify patterns

Production-Ready Error Handler
------------------------------

.. code-block:: python

   import logging
   import time
   import json
   from datetime import datetime
   from askpablos_api import AskPablos, AskPablosError, ResponseError

   class RobustAskPablosClient:
       """Production-ready wrapper with comprehensive error handling."""

       def __init__(self, api_key, secret_key, max_retries=3):
           self.client = AskPablos(api_key=api_key, secret_key=secret_key)
           self.max_retries = max_retries
           self.logger = logging.getLogger(__name__)

       def get_with_retry(self, url, **kwargs):
           """Make GET request with retry logic and comprehensive error handling."""

           for attempt in range(self.max_retries):
               try:
                   response = self.client.get(url, **kwargs)

                   # Log successful request
                   self.logger.info(
                       f"Request successful: {url} "
                       f"(status: {response['status_code']}, "
                       f"time: {response['time_taken']:.2f}s)"
                   )

                   return response

               except ResponseError as e:
                   if e.status_code == 429:  # Rate limited
                       delay = min(60 * (attempt + 1), 300)  # Max 5 minutes
                       self.logger.warning(f"Rate limited, waiting {delay}s")
                       time.sleep(delay)
                       continue

                   elif 500 <= e.status_code < 600:  # Server error
                       if attempt < self.max_retries - 1:
                           delay = 2 ** attempt
                           self.logger.warning(f"Server error {e.status_code}, retrying in {delay}s")
                           time.sleep(delay)
                           continue

                   # Don't retry client errors or final attempt
                   self.logger.error(f"API error {e.status_code}: {e.message}")
                   raise

               except Exception as e:
                   if attempt < self.max_retries - 1:
                       delay = 2 ** attempt
                       self.logger.warning(f"Request failed: {e}, retrying in {delay}s")
                       time.sleep(delay)
                       continue

                   self.logger.error(f"Request failed after {self.max_retries} attempts: {e}")
                   raise

           # Should never reach here, but just in case
           raise Exception(f"Request failed after {self.max_retries} attempts")

   # Usage
   robust_client = RobustAskPablosClient(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   try:
       response = robust_client.get_with_retry("https://api.example.com/data")
       print("Success!")
   except Exception as e:
       print(f"Final failure: {e}")
