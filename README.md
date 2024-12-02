# QA Bug Hunters Challenge - API Testing Project

Testing project for identifying and validating bugs in a game store API by comparing development and release environments.

## Overview

- **Time Frame**: Nov 29 - Dec 2, 2024
- **Goal**: Find and validate 25 bugs in Game Store API
- **Test Environments**:
  - Release API: `https://release-gs.qa-playground.com/api/v1`
  - Development API: `https://dev-gs.qa-playground.com/api/v1`

## Prerequisites

- Python 3.x
- Required packages:
  - pytest
  - requests

## Project Structure

- `test_25bugs.py` - Test file containing all test cases for bug validation
- Documentation of 25 reported bugs with detailed test scenarios

## Test Coverage

Tests cover the following API sections:
- Users (9 tests)
- Wishlist (3 tests)
- Games (2 tests)
- Categories (1 test)
- Avatars (1 test)
- Cart (4 tests)
- Orders (3 tests)
- Payments (2 tests)

## Running Tests

Run all tests:
```bash
pytest test_25bugs.py -v
```

Run specific test category:
```bash
pytest test_25bugs.py -k "test_users" -v
```

## Authentication

Required headers for all requests:
```python
headers = {
    "Authorization": "Bearer qahack2024:<your-email>",
    "X-Task-Id": "api-<number>"
}
```

## Initial Setup

Before running tests, execute setup endpoint:
```bash
POST /setup
Authorization: Bearer qahack2024:<your-email>
```


This project is under the MIT License.
