# Zepto Product Search & Price Scraper

A Python utility for searching and scraping product information from Zepto with cryptographic request signing.

**⚠️ Disclaimer**: This is a reverse-engineered implementation of Zepto's undocumented API endpoints. It uses intercepted request patterns and cryptographic signatures to authenticate with Zepto's backend services. Use responsibly and in accordance with Zepto's terms of service.

## Overview

This repository provides tools to interact with Zepto's API to search for products and extract pricing information. It implements request signature generation for authentication and automated product search with pagination.

## Components

### `genhash.py`
Cryptographic signature generator for Zepto API requests.
- **`generate_signature()`** - Creates SHA-256 signatures for authenticated API calls
- **`extract_path_and_params()`** - Parses and merges URL paths and query parameters
- **`to_slug()`** - Converts product names to URL-friendly slugs

### `search_zepto.py`
Product search and scraping module for Zepto.
- **`searchZepto()`** - Searches Zepto API with pagination, returns product layout data
- Scrapes product details: name, size, MRP, discounted price, discount percentage
- Generates product links and exports results to pandas DataFrame
- Filters products by discount threshold (>10%)

## Features

- ✅ Request signature generation with SHA-256 hashing
- ✅ Paginated API search with automatic parameter handling
- ✅ Product data extraction and normalization
- ✅ URL slug generation for product links
- ✅ Discount filtering and sorting
- ✅ Results export to structured DataFrame

## Use Cases

- Price monitoring across product categories
- Deal finding based on discount percentage
- Product availability tracking by store
- Competitive pricing analysis
