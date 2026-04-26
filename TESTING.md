"""
Testing Guide for Enhanced Torrench

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_site.py
```

### Run specific test class
```bash
pytest tests/test_site.py::TestTorrent
```

### Run specific test function
```bash
pytest tests/test_site.py::TestTorrent::test_torrent_creation
```

### Run tests with coverage
```bash
pytest --cov=endpoints --cov=torrench --cov-report=html
```

### Run only unit tests (marked)
```bash
pytest -m unit
```

## Test Structure

```
tests/
├── __init__.py           # Package marker
├── conftest.py           # Shared fixtures and configuration
├── test_site.py          # Tests for endpoints.site module
├── test_endpoints.py     # Tests for torrent site endpoints
└── test_torrench.py      # Tests for main torrench module
```

## Test Coverage

### tests/test_site.py
- Torrent dataclass creation and methods
- TorrentSite base class and abstract methods
- Formatted output generation
- Color coding for VIP/Trusted users

### tests/test_endpoints.py
- PirateBay endpoint
- Kickass endpoint
- Torrentz2 endpoint (relative imports)
- LimeTorrents endpoint (relative imports)
- RARBG endpoint (relative imports)
- Search URL building
- Connection testing
- Error handling

### tests/test_torrench.py
- TorrentSearcher initialization
- Multi-site searching
- Result formatting
- Result sorting by seeds
- Result details display
- Command-line argument handling

## Fixtures Available

All fixtures are defined in `conftest.py`:

- `mock_torrent`: Standard torrent object
- `mock_vip_torrent`: VIP-flagged torrent
- `mock_trusted_torrent`: Trusted-flagged torrent
- `mock_requests_get`: Mocked requests.get
- `sample_html_response`: Sample HTML for parser testing

## Writing New Tests

### Example: Testing a new endpoint

```python
class TestNewSite:
    def test_site_initialization(self):
        from endpoints.new_site import NewSite
        site = NewSite()
        assert site.name == "New Site"
    
    def test_search_functionality(self, mock_torrent):
        site = NewSite()
        site.working_url = "https://example.com"
        # Your test code here
```

### Example: Testing with mocks

```python
from unittest.mock import patch, Mock

@patch('requests.get')
def test_with_mock(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html>...</html>"
    mock_get.return_value = mock_response
    
    # Your test code here
```

## CI/CD Integration

These tests are ready to be integrated with:
- GitHub Actions
- GitLab CI
- Travis CI
- Jenkins

Example GitHub Actions workflow can be added to `.github/workflows/tests.yml`

## Best Practices

1. Use descriptive test names that explain what is being tested
2. Use fixtures for common setup
3. Mock external API calls (don't make real network requests)
4. Keep tests focused and isolated
5. Use parametrize for testing multiple scenarios
6. Add docstrings to test functions

## Troubleshooting

### Import errors in tests
- Ensure `conftest.py` is in the tests directory
- Check that `sys.path` is correctly configured

### Mock not working
- Make sure you're patching at the right location
- Use full import paths in patch decorators

### Tests failing locally but passing in CI
- Check Python version compatibility
- Verify all dependencies are installed
- Check for hardcoded paths or environment assumptions
"""
