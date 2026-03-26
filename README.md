# AskPablos API Client

[![PyPI Version](https://img.shields.io/pypi/v/askpablos-api.svg)](https://pypi.org/project/askpablos-api/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/askpablos-api.svg)](https://pypi.org/project/askpablos-api/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/askpablos-api.svg)](https://pypi.org/project/askpablos-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Issues](https://img.shields.io/github/issues/fawadss1/askpablos_api.svg)](https://github.com/fawadss1/askpablos_api/issues)

A Python client for making GET requests through the AskPablos proxy service with browser automation support.

**Documentation**: [https://askpablos-api.readthedocs.io/](https://askpablos-api.readthedocs.io/)

## Features

- **Secure Authentication** — HMAC-SHA256 signature-based
- **Browser Automation** — JavaScript rendering with `browser=True`
- **Browser Operations** — Wait for elements with `waitForElement` before capturing HTML
- **Screenshot Capture** — `screenshot=True`
- **Error Handling** — Specific exception types for each failure mode

## Installation

```bash
pip install askpablos-api

# With lxml for HTML/XPath parsing
pip install "askpablos-api[parsing]"
```

## Quick Start

```python
from askpablos_api import AskPablos

client = AskPablos(
    api_key="your_api_key",
    secret_key="your_secret_key"
)

# Simple request
response = client.get("https://httpbin.org/ip")
print(response.content)
```

## Browser Mode & HTML Parsing

For JavaScript-rendered pages, use `browser=True` with `operations` to wait for
content before capturing. Use `lxml` to parse the HTML.

```python
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
    }],
    timeout=45
)

dom = etree.HTML(response.content)
for li in dom.xpath("//ul[@class='prod_list']/li"):
    name = li.xpath(".//span[@class='pr_title']/text()")
    print(name[0].strip() if name else "")
```

## Screenshot

```python
response = client.get(
    url="https://example.com",
    browser=True,
    screenshot=True
)

if response.screenshot:
    with open("screenshot.png", "wb") as f:
        f.write(response.screenshot)
```

## Error Handling

```python
from askpablos_api import (
    AuthenticationError,
    APIConnectionError,
    RequestTimeoutError,
    ResponseError
)

try:
    response = client.get("https://example.com", timeout=30)
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except APIConnectionError as e:
    print(f"Connection error: {e}")
except RequestTimeoutError as e:
    print(f"Timed out: {e}")
except ResponseError as e:
    print(f"HTTP error: {e}")
```

## Development

```bash
git clone https://github.com/fawadss1/askpablos_api.git
cd askpablos-api
pip install -e ".[dev]"
```

## License

MIT — see [LICENSE](LICENSE) for details.

## Support

- **Email**: fawadstar6@gmail.com
- **Issues**: [GitHub Issues](https://github.com/fawadss1/askpablos_api/issues)
