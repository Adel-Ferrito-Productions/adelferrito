# Test Suite

This directory contains the test suite for the Malta Lightning Monitoring System.

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=lightning_monitor --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_config.py
```

### Run specific test
```bash
pytest tests/test_config.py::TestConfigLoader::test_load_config_success
```

### Run tests by marker
```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m "not slow"    # Skip slow tests
```

## Test Structure

- `conftest.py` - Shared fixtures and test configuration
- `test_config.py` - Configuration management tests
- `test_rules_engine.py` - Alert rules engine tests
- `test_data_fusion.py` - Data fusion engine tests

## Test Markers

- `@pytest.mark.unit` - Unit tests (no external dependencies)
- `@pytest.mark.integration` - Integration tests (may require services)
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.api` - Tests that make API calls
- `@pytest.mark.database` - Tests that require database access

## Coverage

The test suite aims for high coverage of core functionality:
- Configuration loading and validation
- Alert rule evaluation
- Data fusion operations
- Geographic calculations

Coverage reports are generated in HTML format in `htmlcov/` directory after running tests with coverage.

