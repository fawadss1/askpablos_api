"""
Simple test file for AskPablos API package.

This file demonstrates how to use the AskPablos API client to make real requests.
Replace the placeholder credentials with your actual API keys to test.
"""

from askpablos_api import AskPablos
import json


def test_basic_get_request():
    """Test basic GET request functionality."""
    print("Testing basic GET request...")

    # Initialize the client with your credentials
    client = AskPablos(
        api_key="SNXLjcXYG4RSCHA2uFPeMXaeyOTVTdhI",
        secret_key="485A4373B3452B7D27A2F25A45865"
    )

    try:
        # Simple GET request
        response = client.get("https://httpbin.org/ip", browser=True, )
        print(response.elapsed_time)
        print("-" * 50)
        return True
    except Exception as e:
        print(e)
        return False


test_basic_get_request()
