"""
Configuration Management

Loads and validates configuration from YAML files and environment variables.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional
import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Loads and manages application configuration."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to config.yaml file
        """
        # Load environment variables
        load_dotenv()

        # Determine config file path
        if config_path is None:
            # Try default locations
            possible_paths = [
                Path(__file__).parent.parent.parent / 'config' / 'config.yaml',
                Path('config') / 'config.yaml',
                Path('config.yaml')
            ]

            for path in possible_paths:
                if path.exists():
                    config_path = str(path)
                    break

        if config_path is None:
            raise FileNotFoundError("Configuration file not found")

        self.config_path = config_path
        self.config = self._load_config()

        logger.info(f"Configuration loaded from {config_path}")

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Validate config
            self._validate_config(config)

            return config

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

    def _validate_config(self, config: Dict):
        """Validate configuration structure."""
        required_sections = ['location', 'data_sources', 'processing', 'alerts']

        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required config section: {section}")

        logger.info("Configuration validation passed")

    def get_config(self) -> Dict:
        """Get full configuration dictionary."""
        return self.config

    def get_api_keys(self) -> Dict:
        """Get API keys from environment variables."""
        keys = {
            'blitzortung_api_key': os.getenv('BLITZORTUNG_API_KEY'),
            'windy_api_key': os.getenv('WINDY_API_KEY'),
            'openweather_api_key': os.getenv('OPENWEATHER_API_KEY'),
            'eumetsat_consumer_key': os.getenv('EUMETSAT_CONSUMER_KEY'),
            'eumetsat_consumer_secret': os.getenv('EUMETSAT_CONSUMER_SECRET'),
            'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID')
        }

        return keys

    def get_email_config(self) -> Dict:
        """Get email configuration from environment variables."""
        return {
            'smtp_host': os.getenv('EMAIL_SMTP_HOST', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('EMAIL_SMTP_PORT', '587')),
            'from_email': os.getenv('EMAIL_FROM'),
            'password': os.getenv('EMAIL_PASSWORD'),
            'to_email': os.getenv('EMAIL_TO')
        }

    def get_database_url(self) -> str:
        """Get database URL."""
        db_url = os.getenv('DATABASE_URL')

        if db_url is None:
            # Use default from config
            db_path = self.config.get('storage', {}).get('database', {}).get('path')
            if db_path:
                db_url = f"sqlite:///{db_path}"
            else:
                db_url = "sqlite:///lightning_monitor/data/cache/weather_data.db"

        return db_url

    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    def is_silent_mode(self) -> bool:
        """Check if silent mode (no notifications) is enabled."""
        return os.getenv('SILENT_MODE', 'false').lower() == 'true'


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Convenience function to load configuration.

    Args:
        config_path: Optional path to config file

    Returns:
        Configuration dictionary
    """
    loader = ConfigLoader(config_path)
    return loader.get_config()
