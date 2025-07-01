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
    rotate_proxy: bool = True, timeout: int = 30, **options) -> Dict[str, Any]
```

Send a GET request through the proxy.

**Parameters:**
- `url` (str): Target URL to fetch
- `params` (dict, optional): Query parameters
- `headers` (dict, optional): Custom headers
- `browser` (bool, optional): Use browser automation (default: False)
- `rotate_proxy` (bool, optional): Enable proxy rotation (default: True)
- `timeout` (int): Request timeout in seconds (default: 30)
- `**options`: Additional proxy options

**Returns:** Dictionary containing the API response

**Example:**
```python
response = client.get("https://api.example.com/users", params={"page": 1})
```

### ProxyClient Class

Lower-level client for direct API communication.

#### Methods

##### request()

```python
request(url: str, method: str = "GET", data: dict = None,
        headers: dict = None, params: dict = None,
        options: dict = None, timeout: int = 30) -> dict
```

Send a request with full control over options.

### Proxy Options

All request methods accept these options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `browser` | bool | `False` | Use browser automation for JavaScript rendering |
| `rotate_proxy` | bool | `True` | Enable proxy rotation |
| `user_agent` | str | None | Custom user agent string |
| `cookies` | dict | None | Cookies to send with request |
| `timeout` | int | 30 | Request timeout in seconds |

### Response Format

All successful API calls return a dictionary with the following structure:

```python
{
    "status_code": 200,
    "headers": {"content-type": "application/json", ...},
    "content": "Response body",
    "url": "Final URL after redirects",
    "proxy_used": "proxy.example.com:8080",
    "time_taken": 1.23
}
```

## Examples

### Web Scraping

```python
# Scrape a static website
response = client.get("https://quotes.toscrape.com/")
html_content = response["content"]

# Scrape a JavaScript-heavy site
response = client.get("https://spa-website.com/", browser=True)
rendered_html = response["content"]
```

### API Integration

```python
# Fetch data from a REST API
users = client.get("https://jsonplaceholder.typicode.com/users")

# API with authentication
response = client.get(
    "https://api.example.com/protected",
    headers={"Authorization": "Bearer your_token_here"}
)
```

### Monitoring Multiple URLs

```python
urls_to_check = [
    "https://site1.com",
    "https://site2.com/api/health", 
    "https://site3.com/status"
]

for url in urls_to_check:
    try:
        response = client.get(url)
        print(f"✅ {url} - Status: {response['status_code']}")
    except Exception as e:
        print(f"❌ {url} - Error: {e}")
```

## Error Handling

### Exception Hierarchy

```
AskPablosError
├── AuthenticationError
├── APIConnectionError
└── ResponseError
```

### Common Error Scenarios

#### Authentication Issues

```python
from askpablos_api import AuthenticationError

try:
    client = AskPablos("", "")  # Empty credentials
except AuthenticationError as e:
    print(f"Auth error: {e}")
```

#### Network Problems

```python
from askpablos_api import APIConnectionError

try:
    response = client.get("https://example.com")
except APIConnectionError as e:
    print(f"Connection failed: {e}")
    # Implement retry logic here
```

#### API Errors

```python
from askpablos_api import ResponseError

try:
    response = client.get("https://httpbin.org/status/500")
except ResponseError as e:
    print(f"API returned error {e.status_code}: {e.message}")
```

## Advanced Usage

### Custom Headers and Authentication

```python
# API with bearer token
response = client.get(
    "https://api.example.com/protected",
    headers={"Authorization": "Bearer your_token_here"}
)

# API with API key in header
response = client.get(
    "https://api.example.com/data",
    headers={"X-API-Key": "your_api_key"}
)
```

### Session Management

```python
# Use session cookies for subsequent requests
protected_data = client.get(
    "https://example.com/protected",
    cookies={"session": "session_cookie_value"}
)
```

### Rate Limiting

```python
import time

urls = ["https://api.example.com/endpoint1", 
        "https://api.example.com/endpoint2"]

for url in urls:
    response = client.get(url)
    print(f"Fetched {url}: {response['status_code']}")
    time.sleep(1)  # Rate limit to 1 request per second
```

### Debugging

```python
from askpablos_api import configure_logging
import logging

# Enable detailed logging
configure_logging(level=logging.DEBUG)

# All requests will now be logged with details
client = AskPablos(api_key="...", secret_key="...")
response = client.get("https://example.com")
```

## Performance Tips

1. **Reuse Client Instance**: Create one client and reuse it for multiple requests
2. **Disable Browser Mode**: Only use `browser=True` when necessary for JavaScript
3. **Connection Pooling**: The underlying requests library handles this automatically
4. **Timeout Settings**: Set appropriate timeouts for your use case
5. **Proxy Rotation**: Keep `rotate_proxy=True` for better reliability

## Troubleshooting

### Common Issues

**Issue**: `AuthenticationError: API key is required`
**Solution**: Ensure your API key is not empty and properly set

**Issue**: `APIConnectionError: Failed to connect to API`
**Solution**: Check your internet connection and API availability

**Issue**: `ResponseError: API response error (status 429)`
**Solution**: You're being rate limited. Implement delays between requests

**Issue**: Requests timing out
**Solution**: Increase the timeout parameter or check target website availability

## Contact

For support and questions:
- **Author**: Fawad Ali
- **Email**: fawadstar6@gmail.com
- **Version**: 0.1.0
