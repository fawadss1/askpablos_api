Examples
========

Simple GET Request
------------------

.. code-block:: python

   from askpablos_api import AskPablos

   client = AskPablos(
       api_key="your_api_key",
       secret_key="your_secret_key"
   )

   response = client.get("https://httpbin.org/ip")
   print(response.content)

Headers and Parameters
----------------------

.. code-block:: python

   response = client.get(
       "https://httpbin.org/headers",
       headers={"User-Agent": "AskPablosBot/1.0"},
       params={"page": "1", "limit": "10"}
   )
   print(response.content)

Screenshot Capture
------------------

.. code-block:: python

   response = client.get(
       "https://example.com",
       browser=True,
       screenshot=True
   )

   if response.screenshot:
       with open("screenshot.png", "wb") as f:
           f.write(response.screenshot)

HTML Parsing with XPath
-----------------------

Use ``lxml`` to parse response HTML and extract data with XPath.

.. note::
   Always use ``from lxml import etree``. Python's stdlib ``xml.etree`` does not
   provide an ``HTML()`` parser or full XPath support.

.. code-block:: python

   from lxml import etree

   response = client.get(
       url="https://example.com/catalog",
       browser=True,
       operations=[{
           "task": "waitForElement",
           "match": {
               "on": "xpath",
               "rule": "visible",
               "value": "//ul[@class='prod_list']"
           }
       }]
   )

   dom = etree.HTML(response.content)
   categories = []

   for li in dom.xpath("//ul[@class='prod_list']/li"):
       name = li.xpath(".//a[@class='ctg_heading']//span[@class='pr_title']/text()")
       links = li.xpath(".//div[@class='bot_list']//a/@href")

       if name and links:
           categories.append({
               "cat_name": name[0].strip(),
               "links": [l.strip() for l in links]
           })

   print(categories)

E-commerce Product Scraping
---------------------------

.. code-block:: python

   products = [
       "https://shop.example.com/product/123",
       "https://shop.example.com/product/456"
   ]

   for i, url in enumerate(products):
       response = client.get(
           url=url,
           browser=True,
           screenshot=True,
           timeout=60
       )

       if response.screenshot:
           with open(f"product_{i+1}.png", "wb") as f:
               f.write(response.screenshot)

       print(f"Product {i+1}: status {response.status_code}")

Error Handling
--------------

.. code-block:: python

   from askpablos_api import (
       AskPablos,
       AuthenticationError,
       APIConnectionError,
       ResponseError,
       RequestTimeoutError
   )

   def safe_request(url, **kwargs):
       try:
           return client.get(url, **kwargs)
       except AuthenticationError as e:
           print(f"Auth failed: {e}")
       except APIConnectionError as e:
           print(f"Connection error: {e}")
       except ResponseError as e:
           print(f"HTTP error: {e}")
       except RequestTimeoutError as e:
           print(f"Timed out: {e}")
       return None

   response = safe_request("https://example.com", browser=True, timeout=30)
   if response:
       print(f"Success: {response.status_code}")
