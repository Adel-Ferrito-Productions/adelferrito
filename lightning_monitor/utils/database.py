"""
Database Handler

Manages SQLite database for caching weather data and storing alert history.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Handles database operations for caching and storage."""

    def __init__(self, db_path: str):
        """
        Initialize database handler.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path

        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        logger.info(f"Database initialized at {db_path}")

    def _init_database(self):
        """Initialize database schema."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Lightning strikes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lightning_strikes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    intensity REAL,
                    source TEXT,
                    distance_km REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Weather data cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_type TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Alert history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alert_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    title TEXT,
                    message TEXT,
                    context_json TEXT,
                    timestamp TEXT NOT NULL,
                    sent_telegram INTEGER DEFAULT 0,
                    sent_email INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indices
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_strikes_timestamp
                ON lightning_strikes(timestamp)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_weather_type_timestamp
                ON weather_cache(data_type, timestamp)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_alert_timestamp
                ON alert_history(timestamp)
            """)

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    def store_lightning_strikes(self, strikes: List[Dict]) -> int:
        """
        Store lightning strikes in database.

        Args:
            strikes: List of strike dictionaries

        Returns:
            Number of strikes stored
        """
        try:
            if not strikes:
                return 0

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for strike in strikes:
                cursor.execute("""
                    INSERT INTO lightning_strikes
                    (timestamp, latitude, longitude, intensity, source, distance_km)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    strike.get('timestamp', datetime.utcnow()).isoformat(),
                    strike.get('latitude', 0),
                    strike.get('longitude', 0),
                    strike.get('intensity', 0),
                    strike.get('source', 'unknown'),
                    strike.get('distance_km', 0)
                ))

            conn.commit()
            count = cursor.rowcount
            conn.close()

            logger.debug(f"Stored {count} lightning strikes")
            return count

        except Exception as e:
            logger.error(f"Error storing lightning strikes: {e}")
            return 0

    def get_recent_strikes(self, hours: int = 1) -> List[Dict]:
        """
        Get recent lightning strikes.

        Args:
            hours: Number of hours to look back

        Returns:
            List of strike dictionaries
        """
        try:
            cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM lightning_strikes
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
            """, (cutoff,))

            rows = cursor.fetchall()
            conn.close()

            strikes = [dict(row) for row in rows]
            return strikes

        except Exception as e:
            logger.error(f"Error getting recent strikes: {e}")
            return []

    def store_weather_data(self, data_type: str, data: Dict) -> bool:
        """
        Store weather data in cache.

        Args:
            data_type: Type of data (e.g., 'windy_forecast', 'satellite')
            data: Data dictionary

        Returns:
            True if stored successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            data_json = json.dumps(data)
            timestamp = datetime.utcnow().isoformat()

            cursor.execute("""
                INSERT INTO weather_cache (data_type, data_json, timestamp)
                VALUES (?, ?, ?)
            """, (data_type, data_json, timestamp))

            conn.commit()
            conn.close()

            logger.debug(f"Stored weather data: {data_type}")
            return True

        except Exception as e:
            logger.error(f"Error storing weather data: {e}")
            return False

    def get_cached_weather_data(
        self,
        data_type: str,
        max_age_minutes: int = 30
    ) -> Optional[Dict]:
        """
        Get cached weather data.

        Args:
            data_type: Type of data to retrieve
            max_age_minutes: Maximum age of cached data in minutes

        Returns:
            Cached data dictionary or None
        """
        try:
            cutoff = (datetime.utcnow() - timedelta(minutes=max_age_minutes)).isoformat()

            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT data_json, timestamp FROM weather_cache
                WHERE data_type = ? AND timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (data_type, cutoff))

            row = cursor.fetchone()
            conn.close()

            if row:
                data = json.loads(row['data_json'])
                logger.debug(f"Retrieved cached weather data: {data_type}")
                return data

            return None

        except Exception as e:
            logger.error(f"Error getting cached weather data: {e}")
            return None

    def store_alert(self, alert: Dict, sent_telegram: bool = False, sent_email: bool = False) -> bool:
        """
        Store alert in history.

        Args:
            alert: Alert dictionary
            sent_telegram: Whether alert was sent via Telegram
            sent_email: Whether alert was sent via email

        Returns:
            True if stored successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            context_json = json.dumps(alert.get('context', {}))

            cursor.execute("""
                INSERT INTO alert_history
                (level, title, message, context_json, timestamp, sent_telegram, sent_email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.get('level', 'info'),
                alert.get('title', ''),
                alert.get('message', ''),
                context_json,
                alert.get('timestamp', datetime.utcnow().isoformat()),
                1 if sent_telegram else 0,
                1 if sent_email else 0
            ))

            conn.commit()
            conn.close()

            logger.debug(f"Stored alert: {alert.get('level', 'unknown')}")
            return True

        except Exception as e:
            logger.error(f"Error storing alert: {e}")
            return False

    def get_alert_history(self, hours: int = 24) -> List[Dict]:
        """
        Get alert history.

        Args:
            hours: Number of hours to look back

        Returns:
            List of alert dictionaries
        """
        try:
            cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM alert_history
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
            """, (cutoff,))

            rows = cursor.fetchall()
            conn.close()

            alerts = []
            for row in rows:
                alert = dict(row)
                # Parse context JSON
                if 'context_json' in alert:
                    alert['context'] = json.loads(alert['context_json'])
                alerts.append(alert)

            return alerts

        except Exception as e:
            logger.error(f"Error getting alert history: {e}")
            return []

    def cleanup_old_data(self, retention_days: int = 30) -> bool:
        """
        Clean up old data from database.

        Args:
            retention_days: Number of days to retain data

        Returns:
            True if cleanup successful
        """
        try:
            cutoff = (datetime.utcnow() - timedelta(days=retention_days)).isoformat()

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Clean lightning strikes
            cursor.execute("""
                DELETE FROM lightning_strikes WHERE timestamp < ?
            """, (cutoff,))
            strikes_deleted = cursor.rowcount

            # Clean weather cache
            cursor.execute("""
                DELETE FROM weather_cache WHERE timestamp < ?
            """, (cutoff,))
            cache_deleted = cursor.rowcount

            # Clean alert history
            cursor.execute("""
                DELETE FROM alert_history WHERE timestamp < ?
            """, (cutoff,))
            alerts_deleted = cursor.rowcount

            conn.commit()
            conn.close()

            logger.info(
                f"Cleanup: deleted {strikes_deleted} strikes, "
                f"{cache_deleted} cache entries, {alerts_deleted} alerts"
            )

            return True

        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return False

    def get_statistics(self, hours: int = 24) -> Dict:
        """
        Get database statistics.

        Args:
            hours: Number of hours for statistics

        Returns:
            Statistics dictionary
        """
        try:
            cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Count strikes
            cursor.execute("""
                SELECT COUNT(*) FROM lightning_strikes WHERE timestamp >= ?
            """, (cutoff,))
            total_strikes = cursor.fetchone()[0]

            # Count alerts
            cursor.execute("""
                SELECT COUNT(*) FROM alert_history WHERE timestamp >= ?
            """, (cutoff,))
            total_alerts = cursor.fetchone()[0]

            # Count by level
            cursor.execute("""
                SELECT level, COUNT(*) FROM alert_history
                WHERE timestamp >= ?
                GROUP BY level
            """, (cutoff,))
            alerts_by_level = dict(cursor.fetchall())

            conn.close()

            return {
                'total_strikes': total_strikes,
                'total_alerts': total_alerts,
                'alerts_by_level': alerts_by_level,
                'period_hours': hours
            }

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
