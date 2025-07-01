# AskPablos API Client

[![PyPI Version](https://img.shields.io/pypi/v/askpablos-api.svg)](https://pypi.org/project/askpablos-api/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/askpablos-api.svg)](https://pypi.org/project/askpablos-api/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/askpablos-api.svg)](https://pypi.org/project/askpablos-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/fawadss1/askpablos_api.svg)](https://github.com/fawadss1/askpablos_api/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/fawadss1/askpablos_api.svg)](https://github.com/fawadss1/askpablos_api/issues)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/fawadss1/askpablos_api.svg)](https://github.com/fawadss1/askpablos_api/commits)

[![Documentation Status](https://readthedocs.org/projects/askpablos-api/badge/?version=latest)](https://askpablos-api.readthedocs.io/en/latest/?badge=latest)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type Checking: MyPy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](https://github.com/python/mypy)
[![Testing: Pytest](https://img.shields.io/badge/testing-pytest-blue.svg)](https://github.com/pytest-dev/pytest)

A professional Python client library for making GET requests through the AskPablos proxy API service. This library provides a clean, secure, and easy-to-use interface for fetching web pages and APIs through the AskPablos proxy infrastructure with rotating IP addresses and browser support.

## Documentation

Full documentation is available at: [https://askpablos-api.readthedocs.io/en/latest/](https://askpablos-api.readthedocs.io/en/latest/)

## Key Features

- 🔐 **Secure Authentication**: HMAC-SHA256 signature-based authentication
- 🌐 **Proxy Support**: Route requests through rotating proxies
- 🤖 **Browser Integration**: Support for JavaScript-heavy websites
- 🛡️ **Error Handling**: Comprehensive exception handling with specific error types
- 📊 **Logging**: Built-in logging support for debugging and monitoring
- 🎯 **Simple Interface**: GET-only requests for clean and focused API
- 🚀 **High Performance**: Optimized for speed and reliability
- 📦 **Zero Dependencies**: Only requires the standard `requests` library

## Installation

```bash
pip install askpablos-api
```

## Development

### Setting up for Development

```bash
git clone https://github.com/fawadss1/askpablos_api.git
cd askpablos-api
pip install -e ".[dev]"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

- **Email**: fawadstar6@gmail.com
- **Documentation**: [https://askpablos-api.readthedocs.io/](https://askpablos-api.readthedocs.io/)
- **Issues**: Please report bugs and feature requests at [GitHub Issues](https://github.com/fawadss1/askpablos_api/issues)

## Changelog

### v0.1.0 (Current)

- Initial release
- HMAC-SHA256 authentication
- GET request support through proxy service
- Comprehensive error handling
- Built-in logging support
- Browser integration for JavaScript-heavy sites
