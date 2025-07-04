Error Handling
==============

The AskPablos API client provides a comprehensive exception hierarchy to help you handle different types of errors that may occur during API interactions.

Exception Hierarchy
-------------------

.. code-block:: text

   AskPablosError (base)
   ├── AuthenticationError
   ├── APIConnectionError
   ├── ResponseError
   └── ValueError (parameter validation)

All exceptions inherit from ``AskPablosError``, allowing you to catch all API-related errors with a single exception handler if needed. Parameter validation errors use Python's built-in ``ValueError``.

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

ValueError (Parameter Validation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when invalid parameter combinations are provided, particularly for browser-specific features.

**Common causes:**
- Using browser-specific options without enabling browser mode
- Invalid parameter combinations
- Incorrect parameter types

.. code-block:: python

   try:
       # This will raise ValueError - browser features require browser=True
       response = client.get(
           url="https://example.com",
           browser=False,      # Browser disabled
           screenshot=True,    # But screenshot requested
           wait_for_load=True  # And page load waiting requested
       )
   except ValueError as e:
       print(f"Parameter validation error: {e}")
       # Output: browser=True is required for these actions: screenshot=True, wait_for_load=True

Browser Parameter Validation
----------------------------

The client validates that browser-specific features are only used when browser mode is enabled:

**Validated Parameters:**
- ``wait_for_load=True`` requires ``browser=True``
- ``screenshot=True`` requires ``browser=True``
- ``js_strategy`` (non-DEFAULT values) requires ``browser=True``

.. code-block:: python

   # Valid usage - browser features with browser enabled
   response = client.get(
       url="https://example.com",
       browser=True,          # Browser enabled
       screenshot=True,       # Valid with browser=True
       wait_for_load=True,    # Valid with browser=True
       js_strategy="DEFAULT"  # Valid with browser=True
   )

   # Invalid usage - will raise ValueError
   try:
       response = client.get(
           url="https://example.com",
           browser=False,         # Browser disabled
           js_strategy=True       # But JS strategy specified
       )
   except ValueError as e:
       print(f"Error: {e}")

Best Practices
--------------

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Always handle specific exceptions for better error management:

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError
   )

   def safe_request(url, **kwargs):
       """Make a request with comprehensive error handling."""
       try:
           client = AskPablos(
               api_key="your_api_key",
               secret_key="your_secret_key"
           )

           response = client.get(url, **kwargs)
           return response

       except ValueError as e:
           print(f"Parameter error: {e}")
           return None
       except AuthenticationError as e:
           print(f"Authentication failed: {e}")
           return None
       except APIConnectionError as e:
           print(f"Connection error: {e}")
           return None
       except ResponseError as e:
           print(f"HTTP error: {e}")
           return None
       except Exception as e:
           print(f"Unexpected error: {e}")
           return None

Retry Logic
~~~~~~~~~~~

Implement retry logic for transient errors:

.. code-block:: python

   import time
   from askpablos_api import APIConnectionError, ResponseError

   def request_with_retry(url, max_retries=3, **kwargs):
       """Request with exponential backoff retry logic."""
       for attempt in range(max_retries):
           try:
               response = client.get(url, **kwargs)
               return response

           except APIConnectionError as e:
               if attempt == max_retries - 1:
                   raise
               wait_time = 2 ** attempt  # Exponential backoff
               print(f"Connection failed, retrying in {wait_time}s... ({attempt + 1}/{max_retries})")
               time.sleep(wait_time)

           except ResponseError as e:
               # Don't retry client errors (4xx), only server errors (5xx)
               if hasattr(e, 'status_code') and 400 <= e.status_code < 500:
                   raise
               if attempt == max_retries - 1:
                   raise
               wait_time = 2 ** attempt
               print(f"Server error, retrying in {wait_time}s... ({attempt + 1}/{max_retries})")
               time.sleep(wait_time)

Logging for Debugging
~~~~~~~~~~~~~~~~~~~~~

Enable logging to help with debugging:

.. code-block:: python

   from askpablos_api import configure_logging

   # Enable debug logging
   configure_logging(level="DEBUG")

   try:
       response = client.get(
           url="https://example.com",
           browser=True,
           timeout=30
       )
   except Exception as e:
       print(f"Request failed: {e}")
       # Check logs for detailed error information

Parameter Validation Helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create helper functions to validate parameters before making requests:

.. code-block:: python

   def validate_browser_options(**kwargs):
       """Validate browser-related parameters."""
       browser_enabled = kwargs.get('browser', False)
       browser_features = []

       if kwargs.get('wait_for_load', False) and not browser_enabled:
           browser_features.append('wait_for_load=True')
       if kwargs.get('screenshot', False) and not browser_enabled:
           browser_features.append('screenshot=True')
       if kwargs.get('js_strategy', 'DEFAULT') != 'DEFAULT' and not browser_enabled:
           browser_features.append('custom js_strategy')

       if browser_features:
           features_str = ', '.join(browser_features)
           raise ValueError(f"browser=True is required for: {features_str}")

   def safe_browser_request(url, **kwargs):
       """Make a browser request with validation."""
       try:
           validate_browser_options(**kwargs)
           return client.get(url, **kwargs)
       except ValueError as e:
           print(f"Invalid parameters: {e}")
           return None

Error Recovery Strategies
~~~~~~~~~~~~~~~~~~~~~~~~

Implement fallback strategies for different error types:

.. code-block:: python

   def robust_request(url, use_browser=True):
       """Request with fallback strategies."""
       try:
           # Try with browser first
           if use_browser:
               return client.get(
                   url=url,
                   browser=True,
                   wait_for_load=True,
                   timeout=45
               )
           else:
               return client.get(url, timeout=15)

       except ValueError:
           # Parameter validation failed, try without browser features
           print("Browser features invalid, falling back to simple request")
           return client.get(url, timeout=15)

       except APIConnectionError:
           # Network issue, try with proxy rotation
           print("Connection failed, trying with proxy rotation")
           return client.get(url, rotate_proxy=True, timeout=30)

       except ResponseError as e:
           # HTTP error, log and re-raise
           print(f"HTTP error {e}, cannot recover")
           raise

Common Error Scenarios
---------------------

Scenario 1: Invalid Browser Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Problem: Browser features without browser mode
   try:
       response = client.get(
           "https://example.com",
           screenshot=True,      # Requires browser=True
           browser=False         # But browser is disabled
       )
   except ValueError as e:
       print(f"Fix: Enable browser mode - {e}")

Scenario 2: Network Timeouts
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Problem: Timeout too short for browser operations
   try:
       response = client.get(
           "https://heavy-spa.com",
           browser=True,
           wait_for_load=True,
           timeout=5  # Too short for browser rendering
       )
   except APIConnectionError as e:
       print(f"Fix: Increase timeout for browser operations - {e}")

Scenario 3: Authentication Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Problem: Invalid or missing credentials
   try:
       client = AskPablos(api_key="invalid", secret_key="invalid")
       response = client.get("https://example.com")
   except AuthenticationError as e:
       print(f"Fix: Check credentials in dashboard - {e}")

Testing Error Conditions
------------------------

Create tests to verify error handling:

.. code-block:: python

   import pytest
   from askpablos_api import AskPablos, AuthenticationError, ValueError

   def test_parameter_validation():
       client = AskPablos(api_key="test", secret_key="test")

       # Test browser parameter validation
       with pytest.raises(ValueError, match="browser=True is required"):
           client.get(
               url="https://example.com",
               browser=False,
               screenshot=True
           )

   def test_authentication_error():
       # Test authentication with empty credentials
       with pytest.raises(AuthenticationError):
           AskPablos(api_key="", secret_key="")

   def test_error_recovery():
       client = AskPablos(api_key="valid", secret_key="valid")

       # Test graceful handling of invalid parameters
       result = safe_request(
           "https://example.com",
           browser=False,
           screenshot=True  # Should be caught and handled
       )
       assert result is None  # Should return None on parameter error
