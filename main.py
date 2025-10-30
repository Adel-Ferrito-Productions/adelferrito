#!/usr/bin/env python3
"""
Malta Lightning Monitoring System - Main Entry Point

Orchestrates real-time lightning monitoring, weather analysis, and alerting.
"""

import sys
import logging
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from lightning_monitor.utils.config import ConfigLoader
from lightning_monitor.utils.database import DatabaseHandler
from lightning_monitor.ingestion.blitzortung import BlitzortungClient
from lightning_monitor.ingestion.windy import WindyClient
from lightning_monitor.ingestion.eumetsat import EumetsatClient
from lightning_monitor.processing.data_fusion import DataFusionEngine
from lightning_monitor.processing.storm_analysis import StormAnalyzer
from lightning_monitor.alerting.rules_engine import AlertRulesEngine
from lightning_monitor.alerting.telegram_notifier import TelegramNotifier
from lightning_monitor.alerting.email_notifier import EmailNotifier

logger = logging.getLogger(__name__)


class LightningMonitor:
    """Main orchestrator for lightning monitoring system."""

    def __init__(self, config_path: str = None):
        """
        Initialize lightning monitor.

        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.get_config()
        self.api_keys = self.config_loader.get_api_keys()

        # Setup logging
        self._setup_logging()

        logger.info("=" * 60)
        logger.info("Malta Lightning Monitoring System Starting")
        logger.info("=" * 60)

        # Initialize database
        db_url = self.config_loader.get_database_url()
        db_path = db_url.replace('sqlite:///', '')
        self.db = DatabaseHandler(db_path)

        # Initialize data sources
        self._init_data_sources()

        # Initialize processing
        self.fusion_engine = DataFusionEngine(self.config)
        self.storm_analyzer = StormAnalyzer(self.config)
        self.rules_engine = AlertRulesEngine(self.config)

        # Initialize notifiers
        self._init_notifiers()

        # Scheduler
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

        # Previous storm cells for tracking
        self.previous_cells = None

        logger.info("Lightning monitor initialized successfully")

    def _setup_logging(self):
        """Setup logging configuration."""
        log_config = self.config.get('logging', {})
        log_level = log_config.get('level', 'INFO')
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = log_config.get('file', 'lightning_monitor/data/logs/monitor.log')

        # Create logs directory
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    def _init_data_sources(self):
        """Initialize data source clients."""
        data_sources_config = self.config.get('data_sources', {})

        # Blitzortung
        if data_sources_config.get('blitzortung', {}).get('enabled', True):
            self.blitzortung = BlitzortungClient(
                data_sources_config['blitzortung'],
                self.api_keys.get('blitzortung_api_key')
            )
        else:
            self.blitzortung = None

        # Windy
        if data_sources_config.get('windy', {}).get('enabled', True):
            windy_key = self.api_keys.get('windy_api_key')
            if windy_key:
                self.windy = WindyClient(windy_key, data_sources_config['windy'])
            else:
                logger.warning("Windy API key not found, Windy client disabled")
                self.windy = None
        else:
            self.windy = None

        # EUMETSAT
        if data_sources_config.get('eumetsat', {}).get('enabled', False):
            consumer_key = self.api_keys.get('eumetsat_consumer_key')
            consumer_secret = self.api_keys.get('eumetsat_consumer_secret')
            if consumer_key and consumer_secret:
                self.eumetsat = EumetsatClient(
                    consumer_key,
                    consumer_secret,
                    data_sources_config['eumetsat']
                )
            else:
                logger.warning("EUMETSAT credentials not found, EUMETSAT client disabled")
                self.eumetsat = None
        else:
            self.eumetsat = None

        logger.info("Data sources initialized")

    def _init_notifiers(self):
        """Initialize notification channels."""
        notifications_config = self.config.get('alerts', {}).get('notifications', {})

        # Telegram
        if notifications_config.get('telegram', {}).get('enabled', True):
            bot_token = self.api_keys.get('telegram_bot_token')
            chat_id = self.api_keys.get('telegram_chat_id')
            if bot_token and chat_id:
                self.telegram = TelegramNotifier(bot_token, chat_id, self.config)
            else:
                logger.warning("Telegram credentials not found, notifications disabled")
                self.telegram = None
        else:
            self.telegram = None

        # Email
        if notifications_config.get('email', {}).get('enabled', True):
            email_config = self.config_loader.get_email_config()
            if all(email_config.values()):
                self.email = EmailNotifier(
                    email_config['smtp_host'],
                    email_config['smtp_port'],
                    email_config['from_email'],
                    email_config['password'],
                    email_config['to_email'],
                    self.config
                )
            else:
                logger.warning("Email configuration incomplete, email notifications disabled")
                self.email = None
        else:
            self.email = None

        logger.info("Notifiers initialized")

    async def fetch_and_process(self):
        """Main monitoring loop - fetch data, analyze, and alert."""
        try:
            logger.info("Starting monitoring cycle...")

            # Get bounding box
            bbox = self.config['location']['bbox']

            # Fetch lightning data
            lightning_strikes = []
            if self.blitzortung:
                strikes = self.blitzortung.get_strikes(
                    bbox,
                    time_window_minutes=60
                )
                lightning_strikes.extend(strikes)
                logger.info(f"Fetched {len(strikes)} lightning strikes")

            # Store strikes in database
            if lightning_strikes:
                self.db.store_lightning_strikes(lightning_strikes)

            # Create GeoDataFrame
            lightning_gdf = self.fusion_engine.create_lightning_geodataframe(
                lightning_strikes
            )

            # Fetch weather data
            weather_data = {}
            if self.windy:
                center = self.config['location']['center']
                weather_data = self.windy.get_area_forecast(
                    bbox,
                    parameters=['cape', 'lifted_index', 'temp', 'pressure', 'wind']
                )
                if weather_data:
                    self.db.store_weather_data('windy_forecast', weather_data)
                    logger.info("Fetched Windy weather data")

            # Fetch satellite data (if available)
            satellite_data = None
            if self.eumetsat:
                satellite_data = self.eumetsat.get_cloud_top_data(bbox)
                if satellite_data:
                    self.db.store_weather_data('satellite_cloud_tops', satellite_data)
                    logger.info("Fetched satellite data")

            # Fuse data
            if not lightning_gdf.empty and weather_data:
                lightning_gdf = self.fusion_engine.fuse_weather_data(
                    lightning_gdf,
                    weather_data,
                    satellite_data
                )

            # Analyze lightning activity
            lightning_analysis = self.storm_analyzer.analyze_lightning_activity(
                lightning_gdf
            )

            # Analyze atmospheric conditions
            atmospheric_analysis = {}
            if weather_data:
                atmospheric_analysis = self.storm_analyzer.analyze_atmospheric_instability(
                    weather_data
                )

            # Track storm motion
            storm_tracking = None
            if not lightning_gdf.empty:
                storm_cells = self.fusion_engine.create_storm_cells(lightning_gdf)
                if not storm_cells.empty:
                    storm_tracking = self.storm_analyzer.track_storm_motion(
                        storm_cells,
                        self.previous_cells
                    )
                    self.previous_cells = storm_cells

            # Log analysis results
            logger.info(f"Lightning: {lightning_analysis.get('strikes_10min', 0)} strikes (10min), "
                       f"trend: {lightning_analysis.get('trend', 'unknown')}")
            logger.info(f"Atmosphere: CAPE={atmospheric_analysis.get('cape', 0):.0f}, "
                       f"LI={atmospheric_analysis.get('lifted_index', 0):.1f}")

            # Evaluate alert conditions
            alerts = self.rules_engine.evaluate_conditions(
                lightning_analysis,
                atmospheric_analysis,
                storm_tracking
            )

            # Send alerts
            for alert in alerts:
                await self._send_alert(alert)

            logger.info("Monitoring cycle completed successfully")

        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}", exc_info=True)

    async def _send_alert(self, alert: Dict):
        """Send alert through configured channels."""
        try:
            sent_telegram = False
            sent_email = False

            # Send via Telegram
            if self.telegram and not self.config_loader.is_silent_mode():
                sent_telegram = await self.telegram.send_alert(alert)

            # Send via Email (only for warning/urgent)
            if self.email and alert.get('level') in ['warning', 'urgent']:
                if not self.config_loader.is_silent_mode():
                    sent_email = self.email.send_alert_email(alert)

            # Store in database
            self.db.store_alert(alert, sent_telegram, sent_email)

            logger.info(f"Alert sent: {alert['level']} - {alert['title']}")

        except Exception as e:
            logger.error(f"Error sending alert: {e}")

    async def send_daily_summary(self):
        """Generate and send daily summary."""
        try:
            logger.info("Generating daily summary...")

            # Get yesterday's statistics
            stats = self.db.get_statistics(hours=24)

            # Get today's forecast
            bbox = self.config['location']['bbox']
            forecast = {}
            if self.windy:
                center = self.config['location']['center']
                forecast_data = self.windy.get_instability_indices(
                    center['latitude'],
                    center['longitude']
                )
                forecast = {
                    'cape': forecast_data.get('cape', 0),
                    'lifted_index': forecast_data.get('lifted_index', 0),
                    'risk_level': forecast_data.get('instability_score', 0) > 50 and 'high' or 'moderate'
                }

            # Build summary
            summary = {
                'date': datetime.utcnow().strftime('%Y-%m-%d'),
                'statistics': {
                    'total_strikes': stats.get('total_strikes', 0),
                    'storm_cells': 0,  # Would need to calculate from stored data
                    'closest_strike_km': 'N/A'
                },
                'forecast': forecast,
                'shooting_windows': [],  # Could be enhanced
                'recommendations': self._generate_recommendations(forecast)
            }

            # Send via Telegram
            if self.telegram:
                await self.telegram.send_daily_summary(summary)

            # Send via Email
            if self.email:
                self.email.send_daily_summary(summary)

            logger.info("Daily summary sent")

        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")

    def _generate_recommendations(self, forecast: Dict) -> str:
        """Generate weather recommendations."""
        risk_level = forecast.get('risk_level', 'unknown')

        recommendations = {
            'extreme': 'Severe thunderstorms likely. Avoid outdoor activities. Excellent photography opportunities expected.',
            'high': 'Strong thunderstorms possible. Monitor conditions closely. Good photography potential.',
            'moderate': 'Isolated thunderstorms may develop. Stay alert. Fair photography conditions.',
            'low': 'Thunderstorms unlikely. Safe outdoor conditions.',
            'minimal': 'Stable weather expected. No significant storm activity anticipated.'
        }

        return recommendations.get(risk_level, 'Monitor weather conditions.')

    def start(self):
        """Start the monitoring system."""
        try:
            self.is_running = True

            # Get scheduler config
            scheduler_config = self.config.get('scheduler', {})
            main_interval = scheduler_config.get('main_loop_interval', 60)

            # Schedule main monitoring loop
            self.scheduler.add_job(
                self.fetch_and_process,
                'interval',
                seconds=main_interval,
                id='main_monitor',
                next_run_time=datetime.now()  # Run immediately
            )

            # Schedule daily summary
            email_config = self.config.get('alerts', {}).get('notifications', {}).get('email', {})
            daily_summary_cron = email_config.get('daily_summary', '0 8 * * *')

            self.scheduler.add_job(
                self.send_daily_summary,
                CronTrigger.from_crontab(daily_summary_cron),
                id='daily_summary'
            )

            # Schedule cleanup
            self.scheduler.add_job(
                self._cleanup_database,
                'cron',
                hour=3,  # 3 AM
                id='cleanup'
            )

            # Start scheduler
            self.scheduler.start()

            logger.info("Monitoring system started")
            logger.info(f"Main loop interval: {main_interval} seconds")
            logger.info(f"Daily summary schedule: {daily_summary_cron}")

            # Keep running
            asyncio.get_event_loop().run_forever()

        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            self.stop()
        except Exception as e:
            logger.error(f"Error starting monitoring system: {e}", exc_info=True)
            self.stop()

    async def _cleanup_database(self):
        """Clean up old database entries."""
        try:
            retention_days = self.config.get('storage', {}).get('database', {}).get('retention_days', 30)
            self.db.cleanup_old_data(retention_days)
            logger.info("Database cleanup completed")
        except Exception as e:
            logger.error(f"Error during database cleanup: {e}")

    def stop(self):
        """Stop the monitoring system."""
        logger.info("Stopping monitoring system...")
        self.is_running = False

        if self.scheduler.running:
            self.scheduler.shutdown()

        logger.info("Monitoring system stopped")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Malta Lightning Monitoring System')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--test', action='store_true', help='Run in test mode (send test notifications)')

    args = parser.parse_args()

    # Create monitor
    monitor = LightningMonitor(args.config)

    # Test mode
    if args.test:
        async def test_notifications():
            logger.info("Running test mode...")
            if monitor.telegram:
                await monitor.telegram.send_test_message()
            logger.info("Test completed")
            monitor.stop()

        asyncio.run(test_notifications())
        return

    # Setup signal handlers
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}")
        monitor.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start monitoring
    monitor.start()


if __name__ == '__main__':
    main()
