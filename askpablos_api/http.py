"""
askpablos_api.http

HTTP communication and client functionality for the AskPablos API.

This module handles HTTP communication with the AskPablos API, including
request construction, response parsing, error handling, and provides
the main ProxyClient class for API interactions.
"""

import json
from base64 import b64decode
from typing import Optional, Dict, Any, List, Union
from urllib.parse import urljoin

import requests

from .auth import AuthManager
from .models import ResponseData, RequestOptions
from .validators import ParameterValidator
from .exceptions import APIConnectionError, ResponseError, RequestTimeoutError
from .config import DEFAULT_API_URL


class HTTPClient:
    """
    Handles low-level HTTP communication with the AskPablos API.

    This class manages the HTTP requests, response parsing,
    and error handling for the proxy service communication.
    """

    def __init__(self, auth_manager: AuthManager, api_url: str):
        """
        Initialize the HTTP client.

        Args:
            auth_manager: Authentication manager for request signing
            api_url: Base URL for the API service
        """
        self.auth_manager = auth_manager
        self.api_url = urljoin(api_url.rstrip('/'), '/api/proxy')

    def send_request(
            self,
            url: str,
            method: str = "GET",
            options: Optional[RequestOptions] = None,
            is_bulk: bool = False
    ) -> ResponseData:
        """
        Send an HTTP request through the proxy service.

        Args:
            url: Target URL to fetch through the proxy
            method: HTTP method (GET, POST, etc.)
            options: Request options and proxy settings
            is_bulk: Whether this is a bulk request

        Returns:
            ResponseData: Parsed response from the API

        Raises:
            APIConnectionError: If connection to API fails
            ResponseError: If API returns an error response
        """
        if options is None:
            options = RequestOptions()

        # Validate options
        options.validate()

        # Build the request payload
        request_data = self._build_request_payload(
            url=url,
            method=method,
            options=options,
            is_bulk=is_bulk
        )

        # Convert to JSON
        payload = json.dumps(request_data, separators=(',', ':'), sort_keys=True)

        # Build authentication headers
        auth_headers = self.auth_manager.build_auth_headers(payload)

        api_url = self.api_url + '/bulk' if is_bulk else self.api_url

        try:
            # Send the request
            response = requests.post(
                api_url,
                data=payload,
                headers=auth_headers,
                timeout=options.timeout
            )

            # Handle HTTP errors
            if response.status_code != 200:
                error_msg = self._extract_error_message(response)
                raise ResponseError(response.status_code, error_msg)

            # Parse and return the response
            return self._parse_response(response, url, is_bulk=is_bulk)

        except requests.Timeout as e:
            raise RequestTimeoutError("The request to the AskPablos server timed out. "
                                      "Please check your network connection or try increasing the timeout setting.") from e

        except requests.RequestException as e:
            raise APIConnectionError("Failed to connect to the askpablos server it may be down or unreachable "
                                     "if the problem persists contact the administrator.") from e

    @staticmethod
    def _build_request_payload(
            url,
            method: str,
            options: RequestOptions,
            is_bulk: bool = False
    ) -> Dict[str, Any]:
        """
        Build the request payload for the API.

        Args:
            url: Target URL (str) or list of URLs when is_bulk=True
            method: HTTP method
            options: Request options
            is_bulk: Whether to build a bulk request payload

        Returns:
            Dict[str, Any]: Complete request payload
        """
        payload = {
            "urls" if is_bulk else "url": [url] if is_bulk else url,
            "method": method.upper(),
            "browser": options.browser,
            "timeout": options.timeout,
            "maxRetries": options.max_retries
        }

        # Add optional fields if present
        optional_fields = ['screenshot', 'operations']

        for field in optional_fields:
            if field in options.additional_options:
                payload[field] = options.additional_options[field]
            elif field == 'screenshot' and options.screenshot:
                payload[field] = options.screenshot

        return payload

    def _parse_response(self, response: requests.Response, url: str, is_bulk: bool) -> ResponseData:
        """
        Parse the API response into a ResponseData object.

        Args:
            response: Raw HTTP response from the API
            url: The requested URL used as key in the response dict
            is_bulk: Indicates if the request was a bulk request

        Returns:
            ResponseData: Parsed response object
        """
        # responseBody is base64-encoded JSON keyed by requested URL
        api_response = response.json()
        decoded_body = b64decode(api_response.get('responseBody'))
        if not is_bulk:
            return ResponseData(
                status_code=response.status_code,
                headers=response.headers,
                content=decoded_body,
                url=url,
                elapsed_time=f"{response.elapsed.total_seconds():.2f}s",
                encoding=self._extract_encoding(response.headers.get('Content-Type')),
                json_data=api_response,
                screenshot=api_response.get('screenshots')
            )

        url_keyed_data = json.loads(decoded_body.decode())
        url_data = url_keyed_data.get(url, {})

        content = url_data.get('content', '')
        if isinstance(content, str):
            content = content.encode()

        # Decode screenshot if present
        screenshot_content = None
        if url_data.get('screenshot'):
            screenshot_content = b64decode(url_data.get('screenshot'))

        return ResponseData(
            status_code=url_data.get('status_code', response.status_code),
            headers={},
            content=content,
            url=url,
            elapsed_time=f"{response.elapsed.total_seconds():.2f}s",
            encoding=self._extract_encoding(url_data.get('contentType')),
            json_data=api_response,
            screenshot=screenshot_content,
        )

    @staticmethod
    def _extract_encoding(content_type: Optional[str]) -> Optional[str]:
        if content_type and 'charset=' in content_type:
            return content_type.split('charset=')[-1]
        return None

    @staticmethod
    def _extract_error_message(response: requests.Response) -> str:
        """
        Extract error message from API response.

        Args:
            response: HTTP response with error

        Returns:
            str: Error message
        """
        response_body = json.loads(response.content)
        try:
            if response_body.get('error'):
                return response_body.get('error')
            else:
                return 'No error details provided'
        except (ValueError, json.JSONDecodeError):
            return f'HTTP {response.status_code} error'


class ProxyClient:
    """
    High-level client for the AskPablos proxy service.

    This class orchestrates the authentication, HTTP communication,
    and validation components to provide a clean interface for
    making proxy requests.
    """

    def __init__(self, api_key: str, secret_key: str, api_url: str = DEFAULT_API_URL):
        """
        Initialize the proxy client.

        Args:
            api_key: Your API key from the AskPablos dashboard
            secret_key: Your secret key for HMAC signing
            api_url: The proxy API base URL
        """
        # Initialize components
        self.auth_manager = AuthManager(api_key, secret_key)
        self.http_client = HTTPClient(self.auth_manager, api_url)
        self.validator = ParameterValidator()

    def request(
            self,
            url: str,
            method: str = "GET",
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, str]] = None,
            options: Optional[Dict[str, Any]] = None,
            timeout: int = 30,
            max_retries: int = 3,
            is_bulk: bool = False
    ) -> ResponseData:
        """
        Send a request through the AskPablos proxy.

        When browser mode is enabled (browser=True), all browser-specific parameters
        (wait_for_load, screenshot, js_strategy) are always sent to the API server
        with their explicit values, ensuring precise control over browser behavior.

        Args:
            url: Target URL to fetch through the proxy
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            headers: Custom headers to send to the target URL
            params: Query parameters to append to the target URL
            options: Proxy-specific options for request processing. When browser=True
                    is included, all browser-specific options are sent to the API.
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on failure
            is_bulk: Whether this is a bulk request

        Returns:
            ResponseData: Response object with all request results
        """
        # Convert options dict to RequestOptions object
        if options is None:
            options = {}

        request_options = RequestOptions(
            browser=options.get("browser", False),
            screenshot=options.get("screenshot", False),
            timeout=timeout,
            max_retries=max_retries,
            **{k: v for k, v in options.items() if k not in [
                "browser", "screenshot"
            ]}
        )

        # Validate all parameters
        self.validator.validate_request_params(
            url=url,
            headers=headers,
            browser=request_options.browser,
            screenshot=request_options.screenshot,
            timeout=timeout,
        )

        # Send the request
        return self.http_client.send_request(
            url=url,
            method=method,
            options=request_options,
            is_bulk=is_bulk
        )
