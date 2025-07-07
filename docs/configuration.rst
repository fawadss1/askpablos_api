Configuration
=============

The AskPablos API client provides several configuration options to customize behavior for different use cases.

Client Configuration
-------------------

Basic Configuration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import AskPablos

   # Basic client setup
   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

Environment Variables
~~~~~~~~~~~~~~~~~~~

Store your credentials securely using environment variables:

.. code-block:: python

   import os
   from askpablos_api import AskPablos

   client = AskPablos(
       api_key=os.getenv("ASKPABLOS_API_KEY"),
       secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
   )

Request Configuration
--------------------

Timeout Settings
~~~~~~~~~~~~~~~

Configure timeouts for different types of requests:

.. code-block:: python

   # Short timeout for simple API calls
   response = client.get(
       "https://api.example.com/data",
       timeout=15
   )

   # Longer timeout for browser-heavy operations
   response = client.get(
       "https://spa-example.com",
       browser=True,
       screenshot=True,
       timeout=60
   )

Browser Configuration
~~~~~~~~~~~~~~~~~~~

Configure browser behavior for JavaScript rendering:

.. code-block:: python

   # Basic browser configuration
   browser_config = {
       "browser": True,
       "wait_for_load": True,
       "js_strategy": "DEFAULT",
       "timeout": 45
   }

   response = client.get("https://example.com", **browser_config)

   # Screenshot configuration
   screenshot_config = {
       "browser": True,
       "screenshot": True,
       "wait_for_load": True,
       "timeout": 60
   }

   response = client.get("https://example.com", **screenshot_config)

Proxy Configuration
~~~~~~~~~~~~~~~~~

Configure proxy rotation and behavior:

.. code-block:: python

   # Enable proxy rotation
   response = client.get(
       "https://example.com",
       rotate_proxy=True,
       timeout=30
   )

   # Combine with browser features
   response = client.get(
       "https://example.com",
       browser=True,
       rotate_proxy=True,
       wait_for_load=True,
       timeout=45
   )

Header Configuration
~~~~~~~~~~~~~~~~~~

Set custom headers for requests:

.. code-block:: python

   # Custom headers
   headers = {
       "User-Agent": "MyApp/1.0",
       "Accept": "application/json",
       "Authorization": "Bearer token123"
   }

   response = client.get(
       "https://api.example.com",
       headers=headers
   )

JavaScript Strategy Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Control JavaScript execution behavior with three distinct strategies:

.. code-block:: python

   # DEFAULT strategy (recommended for most use cases)
   # Uses optimized browser behavior with full JavaScript support
   response = client.get(
       "https://spa-example.com",
       browser=True,
       js_strategy="DEFAULT"
   )

   # Stealth mode (True) - runs stealth script & minimal JS
   # Best for bot-detection protected sites
   response = client.get(
       "https://protected-site.com",
       browser=True,
       js_strategy=True
   )

   # No JavaScript (False) - fastest option
   # Perfect for static content or when JS is not needed
   response = client.get(
       "https://static-content.com",
       browser=True,
       js_strategy=False
   )

**Strategy Comparison:**

- ``js_strategy="DEFAULT"``: Full browser behavior, best compatibility
- ``js_strategy=True``: Stealth mode with minimal JS, bypasses detection
- ``js_strategy=False``: No JavaScript execution, fastest performance

Logging Configuration
--------------------

Basic Logging Setup
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from askpablos_api import configure_logging
   import logging

   # Enable debug logging
   configure_logging(level=logging.DEBUG)

   # Basic logging
   configure_logging(level=logging.INFO)

Custom Logging Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging

   # Configure logging manually
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('askpablos_api.log'),
           logging.StreamHandler()
       ]
   )

   logger = logging.getLogger('askpablos_api')
   logger.setLevel(logging.DEBUG)

Configuration Patterns
---------------------

Reusable Configuration Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create configuration classes for consistent behavior:

.. code-block:: python

   class RequestConfig:
       """Base configuration for requests."""

       def __init__(self):
           self.default_timeout = 30
           self.default_headers = {
               "User-Agent": "MyApp/1.0"
           }

       def get_basic_config(self):
           return {
               "timeout": self.default_timeout,
               "headers": self.default_headers
           }

       def get_browser_config(self):
           return {
               **self.get_basic_config(),
               "browser": True,
               "wait_for_load": True,
               "js_strategy": "DEFAULT",
               "timeout": 60
           }

       def get_screenshot_config(self):
           return {
               **self.get_browser_config(),
               "screenshot": True,
               "timeout": 90
           }

   # Usage
   config = RequestConfig()

   # Simple request
   response = client.get("https://api.example.com", **config.get_basic_config())

   # Browser request
   response = client.get("https://spa.example.com", **config.get_browser_config())

   # Screenshot request
   response = client.get("https://page.example.com", **config.get_screenshot_config())

Environment-Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure behavior based on environment:

.. code-block:: python

   import os

   class EnvironmentConfig:
       def __init__(self):
           self.env = os.getenv("ENVIRONMENT", "development")

       def get_config(self):
           if self.env == "production":
               return {
                   "timeout": 45,
                   "rotate_proxy": True,
                   "retry_attempts": 3
               }
           elif self.env == "development":
               return {
                   "timeout": 30,
                   "rotate_proxy": False,
                   "retry_attempts": 1
               }
           else:  # testing
               return {
                   "timeout": 15,
                   "rotate_proxy": False,
                   "retry_attempts": 1
               }

   # Usage
   env_config = EnvironmentConfig()
   base_config = env_config.get_config()

Performance Configuration
------------------------

Optimized Configurations
~~~~~~~~~~~~~~~~~~~~~~

Different configurations for different performance needs:

.. code-block:: python

   # Fast configuration (minimal features)
   fast_config = {
       "browser": False,
       "timeout": 15
   }

   # Balanced configuration (good for most use cases)
   balanced_config = {
       "browser": True,
       "wait_for_load": True,
       "js_strategy": "DEFAULT",
       "timeout": 30
   }

   # Comprehensive configuration (all features)
   comprehensive_config = {
       "browser": True,
       "wait_for_load": True,
       "screenshot": True,
       "js_strategy": "DEFAULT",
       "rotate_proxy": True,
       "timeout": 60
   }

Best Practices
--------------

1. **Use environment variables** for API credentials
2. **Set appropriate timeouts** based on request complexity
3. **Enable proxy rotation** for high-volume usage
4. **Use browser mode only when needed** for better performance
5. **Configure logging** for debugging and monitoring
6. **Create reusable configurations** for consistency

Security Considerations
---------------------

- Never hardcode API credentials in source code
- Use environment variables or secure configuration files
- Rotate API keys regularly
- Monitor API usage and set appropriate rate limits
- Use HTTPS URLs only for sensitive requests
