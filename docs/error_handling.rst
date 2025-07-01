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
       client = AskPablos(api_key="", secret_key="")  # Empty credentials
       response = client.get("https://example.com")
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")
       # Handle: prompt for valid credentials, exit, etc.

APIConnectionError
~~~~~~~~~~~~~~~~~~

Raised when there are network or connection issues.

**Common causes:**
- Network timeouts
- DNS resolution failures
- Connection refused errors
- SSL/TLS certificate errors
- Proxy service unavailable

.. code-block:: python

   from askpablos_api import APIConnectionError

   try:
       response = client.get("https://example.com", timeout=5)
   except APIConnectionError as e:
       print(f"Connection failed: {e}")
       # Handle: retry logic, fallback, etc.

ResponseError
~~~~~~~~~~~~~

Raised when the API returns an HTTP error response.

**Common causes:**
- 4xx client errors (bad request, unauthorized, not found, etc.)
- 5xx server errors (internal server error, service unavailable, etc.)
- Malformed response data
- Unexpected response format

.. code-block:: python

   from askpablos_api import ResponseError

   try:
       response = client.get("https://httpbin.org/status/404")
   except ResponseError as e:
       print(f"HTTP error: {e}")
       # Handle: log error, try alternative URL, etc.

Best Practices
--------------

Specific Exception Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle specific exceptions for different recovery strategies:

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )
   import time
   import logging

   logger = logging.getLogger(__name__)

   def robust_request(url, max_retries=3, backoff_factor=1.0):
       """Make a request with comprehensive error handling and retry logic."""

       # Initialize client (this may raise AuthenticationError)
       try:
           client = AskPablos(
               api_key="your_api_key",
               secret_key="your_secret_key"
           )
       except AuthenticationError as e:
           logger.error(f"Invalid credentials: {e}")
           raise  # Re-raise as this is not recoverable

       # Attempt request with retries for recoverable errors
       for attempt in range(max_retries):
           try:
               response = client.get(url, timeout=30)
               logger.info(f"Successfully fetched {url}")
               return response

           except APIConnectionError as e:
               # Retry on connection errors with exponential backoff
               if attempt < max_retries - 1:
                   delay = backoff_factor * (2 ** attempt)
                   logger.warning(f"Connection failed (attempt {attempt + 1}), retrying in {delay}s: {e}")
                   time.sleep(delay)
               else:
                   logger.error(f"Connection failed after {max_retries} attempts: {e}")
                   raise

           except ResponseError as e:
               # Don't retry on client errors (4xx), but retry on server errors (5xx)
               response_code = getattr(e, 'status_code', None)
               if response_code and 500 <= response_code < 600 and attempt < max_retries - 1:
                   delay = backoff_factor * (2 ** attempt)
                   logger.warning(f"Server error {response_code} (attempt {attempt + 1}), retrying in {delay}s")
                   time.sleep(delay)
               else:
                   logger.error(f"HTTP error (not retrying): {e}")
                   raise

   # Usage
   try:
       response = robust_request("https://example.com")
       print(f"Success: {response.status_code}")
   except AuthenticationError:
       print("Please check your API credentials")
   except (APIConnectionError, ResponseError) as e:
       print(f"Request failed: {e}")

Context Manager Pattern
~~~~~~~~~~~~~~~~~~~~~~

Use context managers for resource cleanup:

.. code-block:: python

   from contextlib import contextmanager
   from askpablos_api import AskPablos, AskPablosError
   import logging

   logger = logging.getLogger(__name__)

   @contextmanager
   def api_client(api_key, secret_key):
       """Context manager for AskPablos client with automatic error logging."""
       client = None
       try:
           client = AskPablos(api_key=api_key, secret_key=secret_key)
           yield client
       except AskPablosError as e:
           logger.error(f"API client error: {e}")
           raise
       finally:
           # Cleanup if needed
           if client:
               logger.info("Client session completed")

   # Usage
   try:
       with api_client("api_key", "secret_key") as client:
           response = client.get("https://example.com")
           print(response.content)
   except AskPablosError:
       print("API operation failed")

Custom Error Handling
~~~~~~~~~~~~~~~~~~~~~

Create custom error handlers for your application:

.. code-block:: python

   import logging

   class APIErrorHandler:
       """Custom error handler with application-specific logic."""

       def __init__(self, notify_admin=False, log_file=None):
           self.notify_admin = notify_admin
           self.logger = logging.getLogger(__name__)

           if log_file:
               handler = logging.FileHandler(log_file)
               formatter = logging.Formatter(
                   '%(asctime)s - %(levelname)s - %(message)s'
               )
               handler.setFormatter(formatter)
               self.logger.addHandler(handler)

       def handle_error(self, error, context=None):
           """Handle different types of API errors."""
           from askpablos_api import AuthenticationError, APIConnectionError, ResponseError

           context = context or {}

           if isinstance(error, AuthenticationError):
               self.logger.critical(f"Authentication failed: {error}")
               if self.notify_admin:
                   self._notify_admin("Authentication Error", str(error))
               return "CREDENTIALS_INVALID"

           elif isinstance(error, APIConnectionError):
               self.logger.error(f"Connection error: {error}")
               return "CONNECTION_FAILED"

           elif isinstance(error, ResponseError):
               self.logger.warning(f"Response error: {error}")
               return "REQUEST_FAILED"

           else:
               self.logger.error(f"Unexpected error: {error}")
               return "UNKNOWN_ERROR"

       def _notify_admin(self, subject, message):
           """Send notification to admin (implement based on your needs)."""
           print(f"ADMIN ALERT - {subject}: {message}")

   # Usage
   from askpablos_api import AskPablos, AskPablosError

   error_handler = APIErrorHandler(notify_admin=True, log_file="api_errors.log")

   try:
       client = AskPablos(api_key="key", secret_key="secret")
       response = client.get("https://example.com")
   except AskPablosError as e:
       error_code = error_handler.handle_error(e, {"url": "https://example.com"})
       print(f"Error handled with code: {error_code}")

Logging and Monitoring
----------------------

Error Logging Setup
~~~~~~~~~~~~~~~~~~~

Set up comprehensive logging for error tracking:

.. code-block:: python

   import logging
   import sys
   from askpablos_api import configure_logging

   def setup_error_logging():
       """Configure logging for error tracking and debugging."""

       # Configure library logging
       configure_logging(level="INFO")

       # Create application logger
       logger = logging.getLogger("app")
       logger.setLevel(logging.INFO)

       # Console handler for immediate feedback
       console_handler = logging.StreamHandler(sys.stdout)
       console_formatter = logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
       )
       console_handler.setFormatter(console_formatter)

       # File handler for persistent logs
       file_handler = logging.FileHandler("app_errors.log")
       file_formatter = logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
       )
       file_handler.setFormatter(file_formatter)

       # Add handlers
       logger.addHandler(console_handler)
       logger.addHandler(file_handler)

       return logger

   # Usage
   from askpablos_api import AskPablos, AuthenticationError, APIConnectionError

   logger = setup_error_logging()

   try:
       client = AskPablos(api_key="key", secret_key="secret")
       response = client.get("https://example.com")
       logger.info(f"Request successful: {response.status_code}")
   except AuthenticationError as e:
       logger.error(f"Authentication failed: {e}", exc_info=True)
   except APIConnectionError as e:
       logger.warning(f"Connection issue: {e}", exc_info=True)
   except Exception as e:
       logger.critical(f"Unexpected error: {e}", exc_info=True)

Health Checks
~~~~~~~~~~~~~

Implement health checks to monitor API availability:

.. code-block:: python

   import time
   from askpablos_api import AskPablos, AskPablosError

   class APIHealthChecker:
       """Monitor API health and availability."""

       def __init__(self, api_key, secret_key, check_interval=60):
           self.client = AskPablos(api_key=api_key, secret_key=secret_key)
           self.check_interval = check_interval
           self.last_check = 0
           self.is_healthy = None

       def check_health(self):
           """Perform a health check against the API."""
           try:
               # Use a lightweight endpoint for health checks
               response = self.client.get("https://httpbin.org/status/200", timeout=10)

               if response.status_code == 200:
                   self.is_healthy = True
                   return {"status": "healthy", "response_time": response.elapsed}
               else:
                   self.is_healthy = False
                   return {"status": "unhealthy", "status_code": response.status_code}

           except AskPablosError as e:
               self.is_healthy = False
               return {"status": "error", "error": str(e)}

       def ensure_healthy(self):
           """Ensure API is healthy, check if needed."""
           from askpablos_api import APIConnectionError

           now = time.time()

           if now - self.last_check > self.check_interval:
               result = self.check_health()
               self.last_check = now

               if not self.is_healthy:
                   raise APIConnectionError(f"API health check failed: {result}")

           elif self.is_healthy is False:
               raise APIConnectionError("API is marked as unhealthy")

   # Usage
   health_checker = APIHealthChecker("api_key", "secret_key")

   try:
       health_checker.ensure_healthy()
       # Proceed with actual API calls
       response = health_checker.client.get("https://example.com")
   except APIConnectionError as e:
       print(f"API unavailable: {e}")

Testing Error Scenarios
-----------------------

Unit Testing Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test your error handling logic:

.. code-block:: python

   import unittest
   from unittest.mock import patch, MagicMock
   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )

   class TestErrorHandling(unittest.TestCase):
       """Test error handling scenarios."""

       def setUp(self):
           self.client = AskPablos(api_key="test", secret_key="test")

       @patch('askpablos_api.ProxyClient.request')
       def test_authentication_error(self, mock_request):
           """Test authentication error handling."""
           mock_request.side_effect = AuthenticationError("Invalid credentials")

           with self.assertRaises(AuthenticationError):
               self.client.get("https://example.com")

       @patch('askpablos_api.ProxyClient.request')
       def test_connection_error(self, mock_request):
           """Test connection error handling."""
           mock_request.side_effect = APIConnectionError("Connection timeout")

           with self.assertRaises(APIConnectionError):
               self.client.get("https://example.com")

       @patch('askpablos_api.ProxyClient.request')
       def test_response_error(self, mock_request):
           """Test response error handling."""
           mock_request.side_effect = ResponseError("HTTP 404 Not Found")

           with self.assertRaises(ResponseError):
               self.client.get("https://example.com")

       def test_retry_logic(self):
           """Test retry logic with mocked failures."""
           with patch.object(self.client, 'get') as mock_get:
               # First two calls fail, third succeeds
               mock_get.side_effect = [
                   APIConnectionError("Timeout"),
                   APIConnectionError("Timeout"),
                   MagicMock(status_code=200, content="Success")
               ]

               # Implement and test your retry logic here
               # result = your_retry_function(self.client, "https://example.com")
               # self.assertEqual(result.status_code, 200)

   # Run tests
   if __name__ == "__main__":
       unittest.main()

Error Recovery Patterns
-----------------------

Circuit Breaker Pattern
~~~~~~~~~~~~~~~~~~~~~~~

Implement circuit breaker for failing services:

.. code-block:: python

   import time
   from enum import Enum
   from askpablos_api import AskPablosError, APIConnectionError

   class CircuitState(Enum):
       CLOSED = "closed"      # Normal operation
       OPEN = "open"          # Blocking requests
       HALF_OPEN = "half_open"  # Testing if service recovered

   class CircuitBreaker:
       """Circuit breaker for API requests."""

       def __init__(self, failure_threshold=5, timeout=60):
           self.failure_threshold = failure_threshold
           self.timeout = timeout
           self.failure_count = 0
           self.last_failure_time = 0
           self.state = CircuitState.CLOSED

       def call(self, func, *args, **kwargs):
           """Execute function with circuit breaker protection."""
           if self.state == CircuitState.OPEN:
               if time.time() - self.last_failure_time >= self.timeout:
                   self.state = CircuitState.HALF_OPEN
               else:
                   raise APIConnectionError("Circuit breaker is OPEN")

           try:
               result = func(*args, **kwargs)
               self._on_success()
               return result
           except AskPablosError as e:
               self._on_failure()
               raise

       def _on_success(self):
           """Handle successful request."""
           self.failure_count = 0
           self.state = CircuitState.CLOSED

       def _on_failure(self):
           """Handle failed request."""
           self.failure_count += 1
           self.last_failure_time = time.time()

           if self.failure_count >= self.failure_threshold:
               self.state = CircuitState.OPEN

   # Usage
   from askpablos_api import AskPablos

   circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=30)
   client = AskPablos(api_key="key", secret_key="secret")

   try:
       response = circuit_breaker.call(client.get, "https://example.com")
       print("Request successful")
   except APIConnectionError as e:
       print(f"Request blocked or failed: {e}")

Summary
-------

Key points for effective error handling:

1. **Use specific exception types** for different recovery strategies
2. **Implement retry logic** for transient failures
3. **Log errors appropriately** for debugging and monitoring
4. **Set up health checks** to monitor API availability
5. **Test error scenarios** to ensure robust error handling
6. **Use patterns like circuit breakers** for resilient systems
7. **Provide meaningful error messages** to users and developers

By following these practices, you can build robust applications that gracefully handle various error conditions when using the AskPablos API client.
