"""
Telegram Notification Module

Sends lightning and weather alerts via Telegram bot.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Sends notifications via Telegram."""

    def __init__(self, bot_token: str, chat_id: str, config: Dict):
        """
        Initialize Telegram notifier.

        Args:
            bot_token: Telegram bot token
            chat_id: Target chat ID
            config: Configuration dictionary
        """
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
        self.config = config
        self.notifications_config = config.get('alerts', {}).get('notifications', {}).get('telegram', {})
        self.enabled = self.notifications_config.get('enabled', True)

        # Rate limiting
        self.rate_limit_config = self.notifications_config.get('rate_limit', {})
        self.max_per_hour = self.rate_limit_config.get('max_per_hour', 10)
        self.sent_messages = []

        logger.info("Telegram notifier initialized")

    async def send_alert(self, alert: Dict) -> bool:
        """
        Send alert notification.

        Args:
            alert: Alert dictionary with level, title, message

        Returns:
            True if sent successfully
        """
        try:
            if not self.enabled:
                logger.debug("Telegram notifications disabled")
                return False

            # Check rate limit
            if not self._check_rate_limit():
                logger.warning("Telegram rate limit exceeded, skipping notification")
                return False

            # Format message
            message = self._format_alert_message(alert)

            # Send message
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )

            # Track sent message
            self._track_sent_message()

            logger.info(f"Telegram alert sent: {alert['level']}")
            return True

        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
            return False

    async def send_daily_summary(self, summary: Dict) -> bool:
        """
        Send daily weather summary.

        Args:
            summary: Summary dictionary with forecast and statistics

        Returns:
            True if sent successfully
        """
        try:
            if not self.enabled:
                return False

            message = self._format_summary_message(summary)

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )

            logger.info("Daily summary sent via Telegram")
            return True

        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
            return False

    async def send_test_message(self) -> bool:
        """
        Send test message to verify bot configuration.

        Returns:
            True if sent successfully
        """
        try:
            message = (
                "🧪 *Malta Lightning Monitor - Test Message*\n\n"
                "✅ Telegram bot is configured correctly and working!\n\n"
                f"Bot is monitoring lightning activity around Malta.\n"
                f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )

            logger.info("Test message sent successfully")
            return True

        except Exception as e:
            logger.error(f"Error sending test message: {e}")
            return False

    def _format_alert_message(self, alert: Dict) -> str:
        """Format alert as Telegram message with Markdown."""
        try:
            level = alert.get('level', 'info')
            title = alert.get('title', 'Weather Alert')
            message = alert.get('message', '')
            timestamp = alert.get('timestamp', datetime.utcnow().isoformat())

            # Level emoji
            level_emoji = {
                'info': 'ℹ️',
                'watch': '👀',
                'warning': '⚠️',
                'urgent': '🚨'
            }

            emoji = level_emoji.get(level, 'ℹ️')

            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%H:%M:%S UTC')
            except:
                time_str = 'Now'

            # Build message
            formatted = f"{emoji} *{title}*\n\n{message}\n\n🕒 {time_str}"

            return formatted

        except Exception as e:
            logger.error(f"Error formatting alert message: {e}")
            return f"Alert: {alert.get('title', 'Weather Alert')}"

    def _format_summary_message(self, summary: Dict) -> str:
        """Format daily summary as Telegram message."""
        try:
            date_str = summary.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

            message_parts = [
                f"📊 *Malta Lightning Monitor - Daily Summary*",
                f"📅 {date_str}\n",
            ]

            # Statistics
            if 'statistics' in summary:
                stats = summary['statistics']
                message_parts.append("*Yesterday's Activity:*")
                message_parts.append(f"⚡ Total strikes: {stats.get('total_strikes', 0)}")
                message_parts.append(f"🌩️ Storm cells: {stats.get('storm_cells', 0)}")
                message_parts.append(f"📍 Closest: {stats.get('closest_strike_km', 'N/A')} km")
                message_parts.append("")

            # Forecast
            if 'forecast' in summary:
                forecast = summary['forecast']
                message_parts.append("*Today's Forecast:*")
                message_parts.append(f"🌡️ CAPE: {forecast.get('cape', 0):.0f} J/kg")
                message_parts.append(f"📉 Lifted Index: {forecast.get('lifted_index', 0):.1f}")
                message_parts.append(f"⛈️ Thunderstorm risk: {forecast.get('risk_level', 'unknown')}")
                message_parts.append("")

            # Best shooting windows (for lightning photography)
            if 'shooting_windows' in summary:
                windows = summary['shooting_windows']
                if windows:
                    message_parts.append("*Best Lightning Photography Windows:*")
                    for window in windows[:3]:  # Top 3
                        message_parts.append(
                            f"• {window.get('time_range', 'TBD')}: "
                            f"{window.get('probability', 'unknown')} probability"
                        )
                    message_parts.append("")

            # Recommendations
            if 'recommendations' in summary:
                message_parts.append(f"💡 {summary['recommendations']}")

            return "\n".join(message_parts)

        except Exception as e:
            logger.error(f"Error formatting summary message: {e}")
            return "Daily Summary (formatting error)"

    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        try:
            # Clean old messages
            cutoff = datetime.utcnow() - timedelta(hours=1)
            self.sent_messages = [
                ts for ts in self.sent_messages
                if ts >= cutoff
            ]

            # Check limit
            return len(self.sent_messages) < self.max_per_hour

        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Fail open

    def _track_sent_message(self):
        """Track sent message for rate limiting."""
        self.sent_messages.append(datetime.utcnow())

    def get_rate_limit_status(self) -> Dict:
        """Get current rate limit status."""
        try:
            # Clean old messages
            cutoff = datetime.utcnow() - timedelta(hours=1)
            self.sent_messages = [
                ts for ts in self.sent_messages
                if ts >= cutoff
            ]

            return {
                'sent_last_hour': len(self.sent_messages),
                'max_per_hour': self.max_per_hour,
                'remaining': max(0, self.max_per_hour - len(self.sent_messages))
            }

        except Exception as e:
            logger.error(f"Error getting rate limit status: {e}")
            return {}


def send_telegram_alert_sync(bot_token: str, chat_id: str, config: Dict, alert: Dict) -> bool:
    """
    Synchronous wrapper for sending Telegram alerts.

    Args:
        bot_token: Telegram bot token
        chat_id: Target chat ID
        config: Configuration dictionary
        alert: Alert to send

    Returns:
        True if sent successfully
    """
    try:
        notifier = TelegramNotifier(bot_token, chat_id, config)

        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(notifier.send_alert(alert))
        loop.close()

        return result

    except Exception as e:
        logger.error(f"Error in sync Telegram send: {e}")
        return False
