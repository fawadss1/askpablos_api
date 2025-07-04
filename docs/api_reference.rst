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

   Make a GET request through the proxy service with comprehensive options for browser automation and proxy control.

   :param url: The target URL to fetch through the proxy
   :type url: str
   :param params: URL query parameters to append to the request
   :type params: dict, optional
   :param headers: Custom headers to send to the target URL
   :type headers: dict, optional
   :param browser: Enable browser automation for JavaScript rendering
   :type browser: bool, optional
   :param rotate_proxy: Use proxy rotation for this request to avoid rate limiting
   :type rotate_proxy: bool, optional
   :param wait_for_load: Wait for page load completion (requires browser=True)
   :type wait_for_load: bool, optional
   :param screenshot: Take a screenshot of the page (requires browser=True)
   :type screenshot: bool, optional
   :param js_strategy: JavaScript execution strategy ("DEFAULT", True, False)
   :type js_strategy: str or bool, optional
   :param timeout: Request timeout in seconds (default: 30)
   :type timeout: int, optional
   :param options: Additional proxy options like user_agent, cookies, etc.
   :type options: dict, optional
   :returns: Response data object with status, headers, content, and optional screenshot
   :rtype: ResponseData
   :raises APIConnectionError: If connection to the API fails
   :raises ResponseError: If the HTTP response indicates an error
   :raises AuthenticationError: If authentication fails
   :raises ValueError: If browser-specific options are used without browser=True

**Parameter Details**

.. list-table:: AskPablos.get() Parameters
   :header-rows: 1
   :widths: 15 10 10 15 50

   * - Parameter
     - Type
     - Default
     - Browser Required
     - Description
   * - ``url``
     - str
     - *Required*
     - No
     - Target URL to fetch through the proxy
   * - ``params``
     - dict
     - None
     - No
     - URL query parameters to append (e.g., ``{"page": "1", "limit": "10"}``)
   * - ``headers``
     - dict
     - None
     - No
     - Custom headers to send to the target URL
   * - ``browser``
     - bool
     - False
     - N/A
     - **Master switch**: Enable browser automation for JavaScript rendering
   * - ``rotate_proxy``
     - bool
     - False
     - No
     - Use proxy rotation to avoid rate limiting (works with/without browser)
   * - ``wait_for_load``
     - bool
     - False
     - **Yes**
     - Wait for page load completion. **Requires browser=True**
   * - ``screenshot``
     - bool
     - False
     - **Yes**
     - Take a screenshot of the page. **Requires browser=True**
   * - ``js_strategy``
     - str/bool
     - "DEFAULT"
     - **Yes***
     - JavaScript execution strategy. **Requires browser=True** if not "DEFAULT"
   * - ``timeout``
     - int
     - 30
     - No
     - Request timeout in seconds
   * - ``**options``
     - dict
     - {}
     - No
     - Additional proxy options (user_agent, cookies, etc.)

**Browser Dependency Rules**

.. important::

   The following parameters **require browser=True** to function properly:

   * ``wait_for_load=True`` - Cannot wait for page load without browser automation
   * ``screenshot=True`` - Cannot capture screenshots without browser rendering
   * ``js_strategy`` (non-"DEFAULT" values) - Cannot control JavaScript without browser

   **If you try to use these parameters with browser=False, a ValueError will be raised.**

**JavaScript Strategy Options**

.. list-table:: JavaScript Strategy Values
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Description
   * - ``"DEFAULT"``
     - Balanced approach with stealth techniques (works with browser=False)
   * - ``True``
     - Minimal JavaScript with stealth injection (**requires browser=True**)
   * - ``False``
     - No JavaScript execution (**requires browser=True**)

**Parameter Validation Examples**

.. code-block:: python

   # ✅ Valid: Basic request without browser features
   response = client.get("https://example.com")

   # ✅ Valid: Browser enabled with browser-specific features
   response = client.get(
       url="https://example.com",
       browser=True,           # Browser enabled
       wait_for_load=True,     # Valid with browser=True
       screenshot=True,        # Valid with browser=True
       js_strategy=True        # Valid with browser=True
   )

   # ✅ Valid: Proxy rotation works without browser
   response = client.get(
       url="https://example.com",
       rotate_proxy=True       # Works independently
   )

   # ❌ Invalid: Browser features without browser=True
   try:
       response = client.get(
           url="https://example.com",
           browser=False,      # Browser disabled
           screenshot=True     # But screenshot requested
       )
   except ValueError as e:
       print(e)  # "browser=True is required for these actions: screenshot=True"

   # ❌ Invalid: Multiple browser features without browser=True
   try:
       response = client.get(
           url="https://example.com",
           browser=False,        # Browser disabled
           wait_for_load=True,   # Browser feature
           screenshot=True,      # Browser feature
           js_strategy=False     # Browser feature
       )
   except ValueError as e:
       print(e)  # "browser=True is required for these actions: wait_for_load=True, screenshot=True, js_strategy=True"
