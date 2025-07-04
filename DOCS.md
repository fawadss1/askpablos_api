# API Documentation

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [API Reference](#api-reference)
4. [Examples](#examples)
5. [Error Handling](#error-handling)
6. [Advanced Usage](#advanced-usage)

## Getting Started

### Installation

```bash
pip install askpablos-api
```

### Basic Setup

```python
from askpablos_api import AskPablos

client = AskPablos(
    api_key="your_api_key",
    secret_key="your_secret_key"
)
```

## Authentication

The AskPablos API uses HMAC-SHA256 signature authentication to ensure request integrity and authenticity.

### How It Works

1. Your request payload is JSON-encoded
2. An HMAC-SHA256 signature is generated using your secret key
3. The signature is base64-encoded and sent in the `X-Signature` header
4. Your API key is sent in the `X-API-Key` header

### Security Best Practices

- **Never expose your secret key** in client-side code
- Store credentials as environment variables
- Use different API keys for different environments
- Rotate your keys regularly

```python
import os
from askpablos_api import AskPablos

client = AskPablos(
    api_key=os.getenv("ASKPABLOS_API_KEY"),
    secret_key=os.getenv("ASKPABLOS_SECRET_KEY")
)
```

## API Reference

### AskPablos Class

The main client class providing a simple interface for GET requests.

#### Constructor

```python
AskPablos(api_key: str, secret_key: str)
```

**Parameters:**
- `api_key` (str): Your API key from the AskPablos dashboard
- `secret_key` (str): Your secret key for HMAC signing

**Raises:**
- `AuthenticationError`: If any credentials are missing or invalid

#### Methods

##### get()

```python
get(url: str, params: Optional[Dict[str, str]] = None, 
    headers: Optional[Dict[str, str]] = None, browser: bool = False,
    rotate_proxy: bool = False, wait_for_load: bool = False,
    screenshot: bool = False, js_strategy: str = "DEFAULT",
    timeout: int = 30, **options) -> ResponseData
```

Send a GET request through the proxy with advanced browser automation support.

**Parameters:**
- `url` (str): Target URL to fetch
- `params` (dict, optional): Query parameters
- `headers` (dict, optional): Custom headers
- `browser` (bool, optional): Use browser automation (default: False)
- `rotate_proxy` (bool, optional): Enable proxy rotation (default: False)
- `wait_for_load` (bool, optional): Wait for complete page load (requires browser=True)
- `screenshot` (bool, optional): Capture page screenshot (requires browser=True)
- `js_strategy` (str|bool, optional): JavaScript execution strategy when using browser.
                                       Options: True (stealth script & minimal JS), 
                                       False (no stealth injection, no JS rendering),
                                       "DEFAULT" (follows our techniques).
                                       Requires browser=True. Defaults to "DEFAULT".
            timeout (int): Request timeout in seconds (default: 30)
            **options: Additional proxy options

**Returns:** `ResponseData` object containing the API response

**Raises:**
- `ValueError`: If browser-specific options are used without browser=True
- `APIConnectionError`: If connection to API fails
- `ResponseError`: If API returns an error
- `AuthenticationError`: If authentication fails

## Browser Automation Features

### Overview

The AskPablos API now supports advanced browser automation for handling JavaScript-heavy websites, SPAs, and dynamic content. These features require `browser=True` to be enabled.

### Browser Parameters

#### browser (bool)
Enable headless browser automation for JavaScript rendering.

```python
response = client.get("https://spa-website.com", browser=True)
```

#### wait_for_load (bool)
Wait for complete page load including dynamic content. Useful for Single Page Applications.

```python
response = client.get(
    "https://dynamic-site.com",
    browser=True,
    wait_for_load=True,
    timeout=60  # Longer timeout for complex pages
)
```

#### screenshot (bool)
Capture a screenshot of the rendered page. Returns base64-encoded PNG data.

```python
response = client.get(
    "https://example.com",
    browser=True,
    screenshot=True
)

# Save screenshot
if response.screenshot:
    with open("screenshot.png", "wb") as f:
        f.write(response.screenshot)
```

#### js_strategy (str|bool)
Control JavaScript execution strategy:

- **`True`**: Runs stealth script & minimal JS (best for protected sites)
- **`False`**: No stealth injection, no JS rendering (fastest performance)
- **`"DEFAULT"`**: Follows our optimized techniques (balanced approach)

```python
# For protected sites requiring stealth
response = client.get(
    "https://protected-site.com",
    browser=True,
    js_strategy=True,
    wait_for_load=True
)

# For fast loading without JS
response = client.get(
    "https://simple-site.com",
    browser=True,
    js_strategy=False
)

# Default balanced approach
response = client.get(
    "https://normal-site.com",
    browser=True,
    js_strategy="DEFAULT"
)
```

#### rotate_proxy (bool)
Use rotating proxy IP addresses to avoid rate limiting and IP blocks.

```python
response = client.get(
    "https://protected-site.com",
    browser=True,
    rotate_proxy=True
)
```

### Browser Feature Validation

The API validates that browser-specific features are only used when `browser=True`:

```python
# ❌ This will raise ValueError
client.get("https://example.com", screenshot=True)
# Error: browser=True is required for these actions: screenshot=True

# ❌ This will raise ValueError with multiple issues
client.get("https://example.com", 
          wait_for_load=True, 
          screenshot=True, 
          js_strategy=True)
# Error: browser=True is required for these actions: wait_for_load=True, screenshot=True, js_strategy=True

# ✅ This is correct
client.get("https://example.com", browser=True, screenshot=True)
```

### ResponseData Object

The response object now includes browser-specific data:

```python
class ResponseData:
    status_code: int        # HTTP status code
    headers: Dict[str, str] # Response headers
    content: str           # Response body
    url: str              # Final URL after redirects
    elapsed_time: str        # Request duration in seconds
    encoding: str         # Response encoding
    json: dict           # Parsed JSON (if available)
    screenshot: str      # Base64 screenshot (if requested)
```

### Complete Browser Example

```python
# Use all browser features together
response = client.get(
    url="https://advanced-webapp.com",
    browser=True,
    rotate_proxy=True,
    wait_for_load=True,
    screenshot=True,
    js_strategy="DEFAULT",
    timeout=45
)

print(f"Status: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Request time: {response.elapsed_time}")

if response.screenshot:
    # Save screenshot
    with open("webapp_screenshot.png", "wb") as f:
        f.write(response.screenshot)
    print("Screenshot saved!")
```
