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
       # ... make a request ...
       pass
   except AskPablosError as e:
       print(f"API error: {e}")

AuthenticationError
~~~~~~~~~~~~~~~~~~~

Raised when authentication fails due to invalid or missing credentials.

.. code-block:: python

   from askpablos_api import AskPablos, AuthenticationError

   try:
       client = AskPablos(api_key="bad", secret_key="bad")
       client.get("https://example.com")
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")

APIConnectionError
~~~~~~~~~~~~~~~~~~

Raised when there is a network or connection problem.

.. code-block:: python

   from askpablos_api import AskPablos, APIConnectionError

   try:
       client = AskPablos(api_key="your_api_key", secret_key="your_secret_key")
       client.get("https://unreachable.example.com")
   except APIConnectionError as e:
       print(f"Connection error: {e}")

ResponseError
~~~~~~~~~~~~~

Raised for HTTP errors (e.g., 4xx or 5xx responses).

.. code-block:: python

   from askpablos_api import AskPablos, ResponseError

   try:
       client = AskPablos(api_key="your_api_key", secret_key="your_secret_key")
       client.get("https://httpbin.org/status/404")
   except ResponseError as e:
       print(f"HTTP error: {e}")

ValueError (Parameter Validation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised for invalid parameters or usage errors.

.. code-block:: python

   try:
       # This will fail if browser features are requested without enabling browser mode
       client.get(url="https://example.com", browser=False, screenshot=True)
   except ValueError as e:
       print(f"Parameter error: {e}")

Best Practices
--------------

- Always catch AskPablosError for general API errors.
- Catch specific exceptions (AuthenticationError, APIConnectionError, ResponseError) for granular error handling.
- Use ValueError to validate parameters before making requests.
- Log errors for debugging and monitoring.
- Use retry logic for transient network errors (APIConnectionError).

Example: Robust Error Handling
-----------------------------

.. code-block:: python

   from askpablos_api import (
       AskPablos, AuthenticationError, APIConnectionError, ResponseError
   )

   def safe_request(url, **kwargs):
       try:
           client = AskPablos(api_key="your_api_key", secret_key="your_secret_key")
           return client.get(url, **kwargs)
       except AuthenticationError as e:
           print(f"Auth failed: {e}")
       except APIConnectionError as e:
           print(f"Network error: {e}")
       except ResponseError as e:
           print(f"HTTP error: {e}")
       except ValueError as e:
           print(f"Parameter error: {e}")
       except Exception as e:
           print(f"Unexpected error: {e}")
       return None

   # Usage
   response = safe_request("https://example.com")
   if response:
       print(response.status_code)
