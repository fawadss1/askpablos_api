"""
askpablos_api.models

Data models and response objects for the AskPablos API client.

This module contains all data structures used to represent API responses
and internal data objects. Keeping models separate improves maintainability
and makes it easier to extend data structures.
"""

from typing import Optional, Dict, Any


class ResponseData:
    """
    Response object that provides structured access to HTTP response data.

    This class encapsulates all response information from a proxy request,
    including headers, content, timing, and optional screenshot data.

    Attributes:
        status_code (int): HTTP status code from the target server
        headers (Dict[str, str]): Response headers from target server
        content (bytes): Response body/content as bytes
        url (str): Final URL after any redirects
        elapsed_time (str): Time taken to complete the request (formatted string)
        encoding (Optional[str]): Response text encoding
        json (Optional[Dict[str, Any]]): Parsed JSON data if available
        screenshot (Optional[bytes]): Base64 decoded screenshot if requested
    """

    def __init__(
        self,
        status_code: int,
        headers: Dict[str, str],
        content: bytes,
        url: str,
        elapsed_time: str,
        encoding: Optional[str],
        json_data: Optional[Dict[str, Any]] = None,
        screenshot: Optional[bytes] = None
    ):
        """Initialize a ResponseData object."""
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self.url = url
        self.elapsed_time = elapsed_time
        self.encoding = encoding
        self.json = json_data
        self.screenshot = screenshot

    def __repr__(self) -> str:
        """String representation of the response."""
        return (
            f"ResponseData(status_code={self.status_code}, "
            f"url='{self.url}', elapsed_time='{self.elapsed_time}')"
        )

    @property
    def text(self) -> str:
        """
        Get response content as text.

        Returns:
            str: Response content decoded as text using the response encoding
        """
        if self.content:
            encoding = self.encoding or 'utf-8'
            return self.content.decode(encoding, errors='replace')
        return ""

    @property
    def ok(self) -> bool:
        """
        Check if the response was successful.

        Returns:
            bool: True if status code is between 200-299
        """
        return 200 <= self.status_code < 300

    def raise_for_status(self) -> None:
        """
        Raise an exception if the response was unsuccessful.

        Raises:
            HTTPError: If the status code indicates an error
        """
        if not self.ok:
            from .exceptions import ResponseError
            raise ResponseError(
                self.status_code,
                f"HTTP {self.status_code} error for URL: {self.url}"
            )


class RequestOptions:
    """
    Container for request options and parameters.

    This class encapsulates all options that can be passed to a proxy request,
    providing validation and default values.
    """

    def __init__(
        self,
        browser: bool = False,
        screenshot: bool = False,
        timeout: int = 30,
        max_retries: int = 3,
        **additional_options
    ):
        """
        Initialize request options.

        Args:
            browser: Enable browser automation
            screenshot: Take page screenshot
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on failure (default: 3)
            **additional_options: Additional proxy options (e.g., operations)
        """
        self.browser = browser
        self.screenshot = screenshot
        self.timeout = timeout
        self.max_retries = max_retries
        self.additional_options = additional_options

    def validate(self) -> None:
        """
        Validate the request options.

        Raises:
            ValueError: If invalid parameter combinations are detected
        """
        if not self.browser and self.screenshot:
            raise ValueError("browser=True is required for screenshot=True")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert options to dictionary format.

        Returns:
            Dict[str, Any]: Options as dictionary
        """
        options = {
            "browser": self.browser,
            "timeout": self.timeout,
        }

        if self.browser and self.screenshot:
            options["screenshot"] = self.screenshot

        # Add any additional options (like operations)
        options.update(self.additional_options)

        return options
