Troubleshooting
===============

This guide helps you resolve common issues when using the AskPablos API client.

Common Issues
-------------

Authentication Errors
~~~~~~~~~~~~~~~~~~~~

**Problem**: Getting authentication errors when initializing the client.

.. code-block:: python

   # Error: AuthenticationError: Invalid API credentials
   client = AskPablos(api_key="wrong_key", secret_key="wrong_secret")

**Solutions**:

1. **Verify your credentials**:

   .. code-block:: python

      # Check your credentials from the AskPablos dashboard
      client = AskPablos(
          api_key="ak_1234567890abcdef",  # Should start with 'ak_'
          secret_key="sk_abcdef1234567890"  # Should start with 'sk_'
      )

2. **Use environment variables**:

   .. code-block:: bash

      # Set environment variables
      export ASKPABLOS_API_KEY="your_api_key"
      export ASKPABLOS_SECRET_KEY="your_secret_key"

   .. code-block:: python

      import os
      client = AskPablos(
          api_key=os.getenv("ASKPABLOS_API_KEY"),
          secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
      )

Connection Issues
~~~~~~~~~~~~~~~

**Problem**: Getting connection errors or timeouts.

.. code-block:: python

   # Error: APIConnectionError: Connection timeout
   response = client.get("https://slow-website.com")

**Solutions**:

1. **Increase timeout**:

   .. code-block:: python

      response = client.get(
          "https://slow-website.com",
          timeout=60  # Increase from default 30 seconds
      )

2. **Check network connectivity**:

   .. code-block:: python

      # Test with a reliable endpoint first
      response = client.get("https://httpbin.org/ip")
      print(f"Connection test: {response.status_code}")

3. **Enable proxy rotation**:

   .. code-block:: python

      response = client.get(
          "https://example.com",
          rotate_proxy=True
      )

Browser Mode Issues
~~~~~~~~~~~~~~~~~

**Problem**: Browser features not working as expected.

.. code-block:: python

   # Error: ValueError: browser=True is required for screenshot=True
   response = client.get("https://example.com", screenshot=True)

**Solutions**:

1. **Enable browser mode for all browser features**:

   .. code-block:: python

      # All browser features require browser=True
      response = client.get(
          "https://example.com",
          browser=True,          # Required for all browser features
          screenshot=True,       # Requires browser=True
          wait_for_load=True,    # Requires browser=True
          js_strategy="DEFAULT"  # Requires browser=True
      )

2. **Individual browser feature validation**:

   .. code-block:: python

      # Each browser feature must have browser=True

      # For screenshots
      response = client.get(
          "https://example.com",
          browser=True,      # Required
          screenshot=True
      )

      # For waiting for page load
      response = client.get(
          "https://spa-example.com",
          browser=True,      # Required
          wait_for_load=True
      )

      # For JavaScript strategies
      response = client.get(
          "https://example.com",
          browser=True,      # Required
          js_strategy=True   # Any js_strategy value requires browser=True
      )

3. **Common validation errors and fixes**:

   .. code-block:: python

      # These will ALL raise ValueError:

      # ❌ Wrong: wait_for_load without browser=True
      try:
          client.get("https://example.com", wait_for_load=True)
      except ValueError as e:
          print(e)  # browser=True is required for wait_for_load=True

      # ❌ Wrong: screenshot without browser=True
      try:
          client.get("https://example.com", screenshot=True)
      except ValueError as e:
          print(e)  # browser=True is required for screenshot=True

      # ❌ Wrong: js_strategy without browser=True
      try:
          client.get("https://example.com", js_strategy=False)
      except ValueError as e:
          print(e)  # browser=True is required for js_strategy=False

      # ✅ Correct: All browser features with browser=True
      response = client.get(
          "https://example.com",
          browser=True,
          wait_for_load=True,
          screenshot=True,
          js_strategy="DEFAULT"
      )

Parameter Validation Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Getting parameter validation errors.

.. code-block:: python

   # Error: ValueError: Invalid URL format
   response = client.get("not-a-valid-url")

**Solutions**:

1. **Use proper URL format**:

   .. code-block:: python

      # Always include protocol
      response = client.get("https://example.com")  # Correct
      # response = client.get("example.com")        # Wrong

2. **Check parameter dependencies**:

   .. code-block:: python

      # Browser features require browser=True
      response = client.get(
          "https://example.com",
          browser=True,      # Required
          screenshot=True,   # Depends on browser=True
          wait_for_load=True # Depends on browser=True
      )

Screenshot Issues
~~~~~~~~~~~~~~~

**Problem**: Screenshots not being captured or saved properly.

**Solutions**:

1. **Verify browser mode is enabled**:

   .. code-block:: python

      response = client.get(
          "https://example.com",
          browser=True,      # Required
          screenshot=True
      )

2. **Check if screenshot data exists**:

   .. code-block:: python

      response = client.get(
          "https://example.com",
          browser=True,
          screenshot=True
      )

      if response.screenshot:
          with open("screenshot.png", "wb") as f:
              f.write(response.screenshot)
          print("Screenshot saved successfully")
      else:
          print("No screenshot data received")

3. **Increase timeout for screenshot capture**:

   .. code-block:: python

      response = client.get(
          "https://complex-page.com",
          browser=True,
          screenshot=True,
          wait_for_load=True,
          timeout=90  # Longer timeout for complex pages
      )

Performance Issues
~~~~~~~~~~~~~~~~

**Problem**: Requests are too slow or timing out frequently.

**Solutions**:

1. **Optimize browser usage**:

   .. code-block:: python

      # Only use browser mode when necessary
      if url_needs_javascript:
          response = client.get(url, browser=True, timeout=45)
      else:
          response = client.get(url, timeout=15)  # Faster

2. **Use appropriate JavaScript strategy**:

   .. code-block:: python

      # For faster requests when minimal JS is needed
      response = client.get(
          "https://example.com",
          browser=True,
          js_strategy=True,  # Minimal JS
          timeout=30
      )

3. **Enable proxy rotation for rate limiting**:

   .. code-block:: python

      response = client.get(
          "https://example.com",
          rotate_proxy=True
      )

Debugging Techniques
------------------

Enable Logging
~~~~~~~~~~~~~

Add detailed logging to troubleshoot issues:

.. code-block:: python

   import logging
   from askpablos_api import configure_logging

   # Enable debug logging
   configure_logging(level=logging.DEBUG)

   # Or configure manually
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger('askpablos_api')

Response Inspection
~~~~~~~~~~~~~~~~~

Examine response details for debugging:

.. code-block:: python

   response = client.get("https://example.com")

   print(f"Status Code: {response.status_code}")
   print(f"Headers: {response.headers}")
   print(f"URL: {response.url}")
   print(f"Elapsed Time: {response.elapsed_time}")
   print(f"Content Length: {len(response.content)}")
   print(f"Encoding: {response.encoding}")

Error Handling for Debugging
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use comprehensive error handling to identify issues:

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError,
       AskPablosError
   )

   def debug_request(url, **kwargs):
       try:
           client = AskPablos(
               api_key=os.getenv("ASKPABLOS_API_KEY"),
               secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
           )

           print(f"Making request to: {url}")
           print(f"Parameters: {kwargs}")

           response = client.get(url, **kwargs)

           print(f"Success! Status: {response.status_code}")
           return response

       except AuthenticationError as e:
           print(f"Authentication failed: {e}")
           print("Check your API credentials")
       except APIConnectionError as e:
           print(f"Connection error: {e}")
           print("Check network connectivity and try again")
       except ResponseError as e:
           print(f"HTTP error: {e}")
           print("The target server returned an error")
       except ValueError as e:
           print(f"Parameter error: {e}")
           print("Check your request parameters")
       except Exception as e:
           print(f"Unexpected error: {e}")
           print("Contact support if this persists")

       return None

   # Usage
   response = debug_request(
       "https://example.com",
       browser=True,
       screenshot=True,
       timeout=60
   )

Common Error Messages
-------------------

Authentication Errors
~~~~~~~~~~~~~~~~~~~~

- **"Invalid API credentials"**: Check your API key and secret key
- **"Authentication signature mismatch"**: Verify your secret key is correct
- **"API key not found"**: Ensure your API key is active

Connection Errors
~~~~~~~~~~~~~~~

- **"Connection timeout"**: Increase timeout or check network
- **"DNS resolution failed"**: Check URL spelling and connectivity
- **"Proxy connection failed"**: Try again or enable proxy rotation

Parameter Errors
~~~~~~~~~~~~~~~

- **"browser=True is required for X"**: Enable browser mode for browser features
- **"Invalid URL format"**: Use complete URLs with http:// or https://
- **"Timeout must be positive integer"**: Use valid timeout values

Best Practices for Troubleshooting
---------------------------------

1. **Start simple**: Test with basic requests before adding complex features
2. **Check credentials**: Verify API keys are correct and active
3. **Enable logging**: Use debug logging to see detailed request/response info
4. **Test incrementally**: Add features one at a time to isolate issues
5. **Check examples**: Compare your code with working examples in documentation
6. **Monitor timeouts**: Adjust timeouts based on request complexity
7. **Handle errors gracefully**: Always implement proper error handling

Getting Help
-----------

If you continue to experience issues:

1. **Check the documentation** for similar use cases
2. **Enable debug logging** and review the output
3. **Try the examples** in the documentation
4. **Check your network connectivity**
5. **Verify your API credentials** are active
6. **Contact support** with specific error messages and request details
