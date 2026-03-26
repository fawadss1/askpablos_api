Error Handling
==============

Exception Hierarchy
-------------------

.. code-block:: text

   AskPablosError (base)
   ├── AuthenticationError   — invalid/missing credentials
   ├── APIConnectionError    — network or connection failure
   ├── RequestTimeoutError   — request exceeded timeout
   ├── ResponseError         — HTTP 4xx/5xx from target server
   └── ValueError            — invalid parameter combination

All exceptions inherit from ``AskPablosError`` so you can catch everything at once,
or handle each type individually for granular control.

Example
-------

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       RequestTimeoutError,
       ResponseError
   )

   client = AskPablos(api_key="...", secret_key="...")

   try:
       response = client.get("https://example.com", timeout=30)
       print(response.status_code)
   except AuthenticationError as e:
       print(f"Auth failed: {e}")
   except APIConnectionError as e:
       print(f"Network error: {e}")
   except RequestTimeoutError as e:
       print(f"Timed out: {e}")
   except ResponseError as e:
       print(f"HTTP error: {e}")
   except ValueError as e:
       print(f"Parameter error: {e}")
