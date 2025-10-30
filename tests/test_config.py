"""
Tests for configuration management.
"""

import pytest
import os
import tempfile
from pathlib import Path
import yaml
from lightning_monitor.utils.config import ConfigLoader


@pytest.mark.unit
class TestConfigLoader:
    """Test configuration loader functionality."""

    def test_load_config_success(self, config_file, sample_config):
        """Test successful configuration loading."""
        loader = ConfigLoader(config_file)
        config = loader.get_config()
        
        assert config is not None
        assert config['location']['name'] == 'Malta'
        assert config['location']['center']['latitude'] == 35.9375

    def test_load_config_missing_file(self):
        """Test error when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            ConfigLoader('/nonexistent/config.yaml')

    def test_validate_config_missing_sections(self, temp_dir):
        """Test validation fails when required sections are missing."""
        invalid_config = {
            'location': {},
            'data_sources': {}
            # Missing 'processing' and 'alerts'
        }
        
        config_path = Path(temp_dir) / 'invalid_config.yaml'
        with open(config_path, 'w') as f:
            yaml.dump(invalid_config, f)
        
        with pytest.raises(ValueError, match="Missing required config section"):
            ConfigLoader(str(config_path))

    def test_get_api_keys(self, config_file, mock_env_vars):
        """Test API key retrieval from environment variables."""
        loader = ConfigLoader(config_file)
        api_keys = loader.get_api_keys()
        
        assert api_keys['blitzortung_api_key'] == 'test_blitz_key'
        assert api_keys['windy_api_key'] == 'test_windy_key'
        assert api_keys['telegram_bot_token'] == 'test_telegram_token'

    def test_get_api_keys_missing(self, config_file):
        """Test API keys return None when not set."""
        loader = ConfigLoader(config_file)
        api_keys = loader.get_api_keys()
        
        # All keys should be None when not in environment
        assert api_keys['blitzortung_api_key'] is None
        assert api_keys['windy_api_key'] is None

    def test_get_email_config(self, config_file, mock_env_vars):
        """Test email configuration retrieval."""
        loader = ConfigLoader(config_file)
        email_config = loader.get_email_config()
        
        assert email_config['from_email'] == 'test@example.com'
        assert email_config['to_email'] == 'recipient@example.com'
        assert email_config['smtp_host'] == 'smtp.gmail.com'
        assert email_config['smtp_port'] == 587

    def test_get_database_url_from_env(self, config_file, mock_env_vars):
        """Test database URL from environment variable."""
        loader = ConfigLoader(config_file)
        db_url = loader.get_database_url()
        
        assert db_url == 'sqlite:///:memory:'

    def test_get_database_url_from_config(self, config_file, sample_config):
        """Test database URL falls back to config file."""
        sample_config['storage'] = {
            'database': {
                'path': '/tmp/test.db'
            }
        }
        
        # Write updated config
        with open(config_file, 'w') as f:
            yaml.dump(sample_config, f)
        
        loader = ConfigLoader(config_file)
        db_url = loader.get_database_url()
        
        assert 'sqlite:///' in db_url
        assert 'test.db' in db_url

    def test_is_debug_mode(self, config_file, monkeypatch):
        """Test debug mode detection."""
        loader = ConfigLoader(config_file)
        
        monkeypatch.setenv('DEBUG_MODE', 'true')
        assert loader.is_debug_mode() is True
        
        monkeypatch.setenv('DEBUG_MODE', 'false')
        assert loader.is_debug_mode() is False

    def test_is_silent_mode(self, config_file, monkeypatch):
        """Test silent mode detection."""
        loader = ConfigLoader(config_file)
        
        monkeypatch.setenv('SILENT_MODE', 'true')
        assert loader.is_silent_mode() is True
        
        monkeypatch.setenv('SILENT_MODE', 'false')
        assert loader.is_silent_mode() is False

    def test_default_config_path_lookup(self, temp_dir, sample_config):
        """Test automatic config path discovery."""
        # Create config in expected location
        project_root = Path(__file__).parent.parent
        config_dir = project_root / 'config'
        config_dir.mkdir(exist_ok=True)
        
        config_path = config_dir / 'config.yaml'
        with open(config_path, 'w') as f:
            yaml.dump(sample_config, f)
        
        try:
            # Should find config without explicit path
            loader = ConfigLoader()
            assert loader.config_path == str(config_path)
        finally:
            # Cleanup
            if config_path.exists():
                config_path.unlink()

