"""
Blitzortung Lightning Data Ingestion Module

Fetches real-time and historical lightning strike data from the Blitzortung network.
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

logger = logging.getLogger(__name__)


class BlitzortungClient:
    """Client for fetching lightning data from Blitzortung API."""

    def __init__(self, config: Dict, api_key: Optional[str] = None):
        """
        Initialize Blitzortung client.

        Args:
            config: Configuration dictionary with Blitzortung settings
            api_key: Optional API key for authenticated access
        """
        self.base_url = config.get('base_url', 'https://data.blitzortung.org')
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})

        logger.info("Blitzortung client initialized")

    def get_strikes(
        self,
        bbox: Dict[str, float],
        time_window_minutes: int = 60
    ) -> List[Dict]:
        """
        Fetch lightning strikes within a bounding box and time window.

        Args:
            bbox: Bounding box with keys: min_lat, max_lat, min_lon, max_lon
            time_window_minutes: Historical window in minutes

        Returns:
            List of strike dictionaries with timestamp, lat, lon, intensity
        """
        try:
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=time_window_minutes)

            # Blitzortung uses regional data endpoints
            # This is a simplified example - actual implementation may vary
            region = self._determine_region(bbox)

            # Try multiple data sources
            strikes = []

            # Method 1: Direct API (if available)
            try:
                strikes = self._fetch_from_api(bbox, start_time, end_time)
            except Exception as e:
                logger.debug(f"Direct API failed: {e}, trying alternative sources")

            # Method 2: Live data feed
            if not strikes:
                try:
                    strikes = self._fetch_from_live_feed(bbox, time_window_minutes)
                except Exception as e:
                    logger.debug(f"Live feed failed: {e}")

            # Method 3: Third-party relay (lightningmaps.org)
            if not strikes:
                try:
                    strikes = self._fetch_from_relay(bbox, time_window_minutes)
                except Exception as e:
                    logger.debug(f"Relay failed: {e}")

            logger.info(f"Fetched {len(strikes)} strikes from Blitzortung")
            return strikes

        except Exception as e:
            logger.error(f"Error fetching Blitzortung data: {e}")
            return []

    def _determine_region(self, bbox: Dict[str, float]) -> str:
        """Determine Blitzortung region code from bounding box."""
        # Malta is in region 1 (Europe)
        return "1"

    def _fetch_from_api(
        self,
        bbox: Dict[str, float],
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict]:
        """Fetch from official Blitzortung API (requires authentication)."""
        url = f"{self.base_url}/strikes"

        params = {
            'min_lat': bbox['min_lat'],
            'max_lat': bbox['max_lat'],
            'min_lon': bbox['min_lon'],
            'max_lon': bbox['max_lon'],
            'start': start_time.isoformat(),
            'end': end_time.isoformat()
        }

        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        return self._parse_strikes(data)

    def _fetch_from_live_feed(
        self,
        bbox: Dict[str, float],
        time_window_minutes: int
    ) -> List[Dict]:
        """Fetch from Blitzortung live data feed."""
        # Blitzortung provides regional live data
        region = self._determine_region(bbox)
        url = f"https://www.blitzortung.org/en/live_lightning_maps.php?map=30"

        # Note: This would need to parse the actual data format
        # which may be JSON, binary, or other format
        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        # Parse response (format depends on actual API)
        strikes = self._parse_live_feed(response.content, bbox)
        return strikes

    def _fetch_from_relay(
        self,
        bbox: Dict[str, float],
        time_window_minutes: int
    ) -> List[Dict]:
        """Fetch from third-party relay service (e.g., lightningmaps.org)."""
        # lightningmaps.org provides Blitzortung data
        url = "https://api.lightningmaps.org/strikes"

        params = {
            'bbox': f"{bbox['min_lon']},{bbox['min_lat']},{bbox['max_lon']},{bbox['max_lat']}",
            'minutes': time_window_minutes
        }

        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        return self._parse_strikes(data)

    def _parse_strikes(self, data: any) -> List[Dict]:
        """Parse strike data into standardized format."""
        strikes = []

        # Handle different data formats
        if isinstance(data, dict):
            if 'strikes' in data:
                raw_strikes = data['strikes']
            elif 'data' in data:
                raw_strikes = data['data']
            else:
                raw_strikes = [data]
        elif isinstance(data, list):
            raw_strikes = data
        else:
            logger.warning(f"Unexpected data format: {type(data)}")
            return []

        for strike in raw_strikes:
            try:
                # Parse common fields
                parsed = {
                    'timestamp': self._parse_timestamp(strike),
                    'latitude': float(strike.get('lat', strike.get('latitude', 0))),
                    'longitude': float(strike.get('lon', strike.get('longitude', 0))),
                    'intensity': strike.get('intensity', strike.get('amplitude', 1)),
                    'source': 'blitzortung'
                }
                strikes.append(parsed)
            except Exception as e:
                logger.debug(f"Error parsing strike: {e}")
                continue

        return strikes

    def _parse_live_feed(self, content: bytes, bbox: Dict[str, float]) -> List[Dict]:
        """Parse live feed data format."""
        # This is a placeholder - actual implementation depends on data format
        try:
            data = json.loads(content)
            strikes = self._parse_strikes(data)

            # Filter by bounding box
            filtered = [
                s for s in strikes
                if bbox['min_lat'] <= s['latitude'] <= bbox['max_lat']
                and bbox['min_lon'] <= s['longitude'] <= bbox['max_lon']
            ]
            return filtered
        except Exception as e:
            logger.error(f"Error parsing live feed: {e}")
            return []

    def _parse_timestamp(self, strike: Dict) -> datetime:
        """Parse timestamp from various formats."""
        # Try different timestamp fields
        ts_fields = ['timestamp', 'time', 'datetime', 'ts']

        for field in ts_fields:
            if field in strike:
                ts = strike[field]

                # Handle different formats
                if isinstance(ts, (int, float)):
                    # Unix timestamp (seconds or milliseconds)
                    if ts > 1e10:  # Milliseconds
                        return datetime.fromtimestamp(ts / 1000)
                    else:  # Seconds
                        return datetime.fromtimestamp(ts)
                elif isinstance(ts, str):
                    # ISO format string
                    try:
                        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    except:
                        pass

        # Default to current time if parsing fails
        return datetime.utcnow()

    def get_statistics(self, bbox: Dict[str, float]) -> Dict:
        """Get statistics about recent lightning activity."""
        try:
            strikes = self.get_strikes(bbox, time_window_minutes=60)

            if not strikes:
                return {
                    'total_strikes': 0,
                    'strikes_last_10min': 0,
                    'strikes_last_30min': 0,
                    'average_intensity': 0
                }

            now = datetime.utcnow()

            strikes_10min = len([
                s for s in strikes
                if (now - s['timestamp']).total_seconds() < 600
            ])

            strikes_30min = len([
                s for s in strikes
                if (now - s['timestamp']).total_seconds() < 1800
            ])

            avg_intensity = sum(s['intensity'] for s in strikes) / len(strikes)

            return {
                'total_strikes': len(strikes),
                'strikes_last_10min': strikes_10min,
                'strikes_last_30min': strikes_30min,
                'average_intensity': avg_intensity
            }

        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}
