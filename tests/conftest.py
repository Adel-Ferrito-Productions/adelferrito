"""
Pytest fixtures and configuration for all tests.
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
import yaml
from datetime import datetime

# Add project root to path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Provide a minimal valid configuration for testing."""
    return {
        'location': {
            'name': 'Malta',
            'center': {
                'latitude': 35.9375,
                'longitude': 14.3754
            },
            'monitoring_radius_km': 100,
            'bbox': {
                'min_lat': 35.0,
                'max_lat': 37.0,
                'min_lon': 13.0,
                'max_lon': 15.5
            }
        },
        'data_sources': {
            'blitzortung': {
                'enabled': True,
                'base_url': 'https://data.blitzortung.org',
                'fetch_interval': 60
            },
            'windy': {
                'enabled': True,
                'base_url': 'https://api.windy.com/api',
                'fetch_interval': 300
            },
            'eumetsat': {
                'enabled': False
            }
        },
        'processing': {
            'lightning': {
                'min_strikes_for_storm': 15,
                'cluster_radius_km': 30
            },
            'atmospheric': {
                'cape_threshold': 1000,
                'lifted_index_threshold': -3
            }
        },
        'alerts': {
            'levels': {
                'info': {
                    'conditions': ['strikes_10min > 5']
                },
                'watch': {
                    'conditions': ['strikes_10min > 15', 'cape > 1000']
                },
                'warning': {
                    'conditions': ['strikes_10min > 30', 'cape > 1500']
                }
            },
            'notifications': {
                'rate_limit': {
                    'suppress_duplicates_minutes': 15
                }
            }
        }
    }


@pytest.fixture
def config_file(temp_dir, sample_config):
    """Create a temporary config.yaml file."""
    config_path = Path(temp_dir) / 'config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(sample_config, f)
    return str(config_path)


@pytest.fixture
def sample_lightning_strikes():
    """Provide sample lightning strike data."""
    base_time = datetime(2024, 1, 1, 12, 0, 0)
    return [
        {
            'timestamp': base_time,
            'latitude': 35.9375,
            'longitude': 14.3754,
            'intensity': 1000,
            'source': 'blitzortung'
        },
        {
            'timestamp': base_time,
            'latitude': 36.0,
            'longitude': 14.4,
            'intensity': 1500,
            'source': 'blitzortung'
        },
        {
            'timestamp': base_time,
            'latitude': 35.9,
            'longitude': 14.3,
            'intensity': 800,
            'source': 'blitzortung'
        }
    ]


@pytest.fixture
def sample_atmospheric_data():
    """Provide sample atmospheric analysis data."""
    return {
        'cape': 1200,
        'lifted_index': -4,
        'temperature': 25,
        'pressure': 1013,
        'humidity': 70,
        'wind_speed': 15,
        'wind_direction': 180,
        'thunder_probability': 60,
        'instability_score': 75
    }


@pytest.fixture
def sample_lightning_analysis():
    """Provide sample lightning activity analysis."""
    return {
        'strikes_10min': 20,
        'strikes_30min': 45,
        'strike_rate': 10.5,
        'closest_strike_km': 25,
        'trend': 'increasing',
        'severity': 'moderate',
        'density': {
            'max': 15,
            'average': 8.5
        },
        'recent_strikes': 18,
        'peak_activity': datetime(2024, 1, 1, 12, 0, 0)
    }


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    env_vars = {
        'BLITZORTUNG_API_KEY': 'test_blitz_key',
        'WINDY_API_KEY': 'test_windy_key',
        'EUMETSAT_CONSUMER_KEY': 'test_eumetsat_key',
        'EUMETSAT_CONSUMER_SECRET': 'test_eumetsat_secret',
        'TELEGRAM_BOT_TOKEN': 'test_telegram_token',
        'TELEGRAM_CHAT_ID': '123456789',
        'EMAIL_FROM': 'test@example.com',
        'EMAIL_TO': 'recipient@example.com',
        'EMAIL_PASSWORD': 'test_password',
        'DATABASE_URL': 'sqlite:///:memory:',
        'DEBUG_MODE': 'false',
        'SILENT_MODE': 'false'
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    return env_vars


@pytest.fixture(autouse=True)
def reset_env(monkeypatch):
    """Reset environment variables after each test."""
    # Store original values
    original_env = dict(os.environ)
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

