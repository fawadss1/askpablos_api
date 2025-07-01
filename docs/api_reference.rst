API Reference
=============

This section provides detailed documentation for all classes and methods in the AskPablos API client.

Core Classes
------------

AskPablos
~~~~~~~~~

.. autoclass:: askpablos_api.AskPablos
   :members:
   :undoc-members:
   :show-inheritance:

The main client class for making requests through the AskPablos proxy service. This is the primary interface that most users will interact with.

**Constructor**

.. automethod:: askpablos_api.AskPablos.__init__

   Initialize the AskPablos client with authentication credentials.

   :param api_key: Your unique API key from the AskPablos dashboard
   :type api_key: str
   :param secret_key: Your private secret key for HMAC signing
   :type secret_key: str
   :raises AuthenticationError: If credentials are missing or invalid

**Methods**

.. automethod:: askpablos_api.AskPablos.get

   Make a GET request through the proxy service.

   :param url: The URL to request
   :type url: str
   :param headers: Optional custom headers to send with the request
   :type headers: dict, optional
   :param use_browser: Enable browser mode for JavaScript rendering
   :type use_browser: bool, optional
   :param timeout: Request timeout in seconds (default: 30)
   :type timeout: int, optional
   :returns: Response data object
   :rtype: ResponseData
   :raises APIConnectionError: If connection to the API fails
   :raises ResponseError: If the HTTP response indicates an error
   :raises AuthenticationError: If authentication fails

ProxyClient
~~~~~~~~~~~,

.. autoclass:: askpablos_api.ProxyClient
   :members:
   :undoc-members:
   :show-inheritance:

Lower-level client that handles direct communication with the AskPablos API service, including authentication and request signing. This class is used internally by the AskPablos class but can be used directly for advanced use cases.

**Constructor**

.. automethod:: askpablos_api.ProxyClient.__init__

   Initialize the ProxyClient with authentication credentials.

   :param api_key: Your unique API key
   :type api_key: str
   :param secret_key: Your private secret key
   :type secret_key: str
   :param api_url: Custom API URL (optional)
   :type api_url: str, optional

**Methods**

.. automethod:: askpablos_api.ProxyClient.request

   Make a low-level request to the proxy service.

   :param method: HTTP method (only "GET" is supported)
   :type method: str
   :param url: Target URL to request
   :type url: str
   :param headers: Optional headers
   :type headers: dict, optional
   :param options: Additional proxy options
   :type options: dict, optional
   :returns: Response data object
   :rtype: ResponseData

Response Objects
----------------

ResponseData
~~~~~~~~~~~~

.. autoclass:: askpablos_api.client.ResponseData
   :members:
   :undoc-members:
   :show-inheritance:

Response object that provides structured access to HTTP response data.

**Attributes**

.. attribute:: ResponseData.status_code

   HTTP status code of the response.

   :type: int

.. attribute:: ResponseData.headers

   Response headers as a dictionary.

   :type: dict

.. attribute:: ResponseData.content

   Response body as a string.

   :type: str

.. attribute:: ResponseData.url

   Final URL after any redirects.

   :type: str

.. attribute:: ResponseData.elapsed

   Request duration in seconds.

   :type: float

.. attribute:: ResponseData.encoding

   Response text encoding.

   :type: str or None

.. attribute:: ResponseData.json

   Parsed JSON data if the response is JSON, None otherwise.

   :type: dict or None

Exception Classes
-----------------

The library provides a comprehensive exception hierarchy for proper error handling:

.. automodule:: askpablos_api.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

AskPablosError
~~~~~~~~~~~~~~

.. autoexception:: askpablos_api.AskPablosError
   :members:
   :show-inheritance:

Base exception class for all AskPablos API errors. All other exceptions inherit from this class.

AuthenticationError
~~~~~~~~~~~~~~~~~~~

.. autoexception:: askpablos_api.AuthenticationError
   :members:
   :show-inheritance:

Raised when there are authentication problems:

- Missing or empty API key
- Missing or empty secret key
- Invalid credentials
- HMAC signature verification failure

APIConnectionError
~~~~~~~~~~~~~~~~~~

.. autoexception:: askpablos_api.APIConnectionError
   :members:
   :show-inheritance:

Raised when there are network or connection issues:

- Network timeouts
- DNS resolution failures
- Connection refused errors
- SSL/TLS errors

ResponseError
~~~~~~~~~~~~~

.. autoexception:: askpablos_api.ResponseError
   :members:
   :show-inheritance:

Raised when the API returns an HTTP error response:

- 4xx client errors
- 5xx server errors
- Malformed response data

Utility Functions
-----------------

configure_logging
~~~~~~~~~~~~~~~~~~

.. autofunction:: askpablos_api.configure_logging

   Configure logging for the AskPablos API client.

   :param level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
   :type level: str
   :param format_string: Custom log format string
   :type format_string: str, optional

**Example usage:**

.. code-block:: python

   from askpablos_api import configure_logging

   # Enable debug logging
   configure_logging(level="DEBUG")

   # Custom format
   configure_logging(
       level="INFO",
       format_string="%(asctime)s [%(levelname)s] %(message)s"
   )

build_proxy_options
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: askpablos_api.utils.build_proxy_options

   Build proxy options dictionary for API requests.

   :param use_browser: Enable browser mode
   :type use_browser: bool
   :param timeout: Request timeout
   :type timeout: int
   :param additional_options: Additional options
   :type additional_options: dict, optional
   :returns: Formatted options dictionary
   :rtype: dict

Constants
---------

.. autodata:: askpablos_api.config.DEFAULT_API_URL

   Default API endpoint URL.

   :type: str

.. autodata:: askpablos_api.__version__

   Current library version.

   :type: str

Usage Examples
--------------

**Basic Usage**

.. code-block:: python

   from askpablos_api import AskPablos

   client = AskPablos(api_key="key", secret_key="secret")
   response = client.get("https://example.com")

**Advanced Usage with ProxyClient**

.. code-block:: python

   from askpablos_api import ProxyClient

   client = ProxyClient(api_key="key", secret_key="secret")
   response = client.request(
       method="GET",
       url="https://example.com",
       headers={"User-Agent": "Custom"},
       options={"use_browser": True, "timeout": 30}
   )

**Error Handling**

.. code-block:: python

   from askpablos_api import AskPablos, AuthenticationError, APIConnectionError

   try:
       client = AskPablos(api_key="key", secret_key="secret")
       response = client.get("https://example.com")
   except AuthenticationError:
       print("Check your credentials")
   except APIConnectionError:
       print("Network issue")
   except Exception as e:
       print(f"Other error: {e}")
