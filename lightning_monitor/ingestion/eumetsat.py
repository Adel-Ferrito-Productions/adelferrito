"""
EUMETSAT Satellite Data Ingestion Module

Fetches satellite imagery and lightning mapper data from EUMETSAT.
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import base64

logger = logging.getLogger(__name__)


class EumetsatClient:
    """Client for fetching satellite data from EUMETSAT API."""

    def __init__(self, consumer_key: str, consumer_secret: str, config: Dict):
        """
        Initialize EUMETSAT client.

        Args:
            consumer_key: EUMETSAT API consumer key
            consumer_secret: EUMETSAT API consumer secret
            config: Configuration dictionary with EUMETSAT settings
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = config.get('base_url', 'https://api.eumetsat.int')
        self.products = config.get('products', [])
        self.session = requests.Session()
        self.access_token = None
        self.token_expiry = None

        logger.info("EUMETSAT client initialized")

    def _authenticate(self) -> bool:
        """Authenticate with EUMETSAT API and get access token."""
        try:
            # Check if we have a valid token
            if self.access_token and self.token_expiry:
                if datetime.utcnow() < self.token_expiry:
                    return True

            # Get new token
            url = f"{self.base_url}/token"

            # Create basic auth header
            credentials = f"{self.consumer_key}:{self.consumer_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()

            headers = {
                'Authorization': f'Basic {encoded}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            data = {'grant_type': 'client_credentials'}

            response = self.session.post(url, headers=headers, data=data, timeout=30)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data['access_token']

            # Token typically expires in 3600 seconds
            expires_in = token_data.get('expires_in', 3600)
            self.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in - 60)

            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })

            logger.info("EUMETSAT authentication successful")
            return True

        except Exception as e:
            logger.error(f"EUMETSAT authentication failed: {e}")
            return False

    def get_satellite_imagery(
        self,
        product: str,
        bbox: Dict[str, float],
        time_range: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Get satellite imagery for specified product and area.

        Args:
            product: Product identifier (e.g., 'MSG-IR', 'MSG-WV')
            bbox: Bounding box with keys: min_lat, max_lat, min_lon, max_lon
            time_range: Optional time range with 'start' and 'end' datetime objects

        Returns:
            Dictionary with imagery data and metadata
        """
        try:
            if not self._authenticate():
                return None

            # Default to last hour if no time range specified
            if time_range is None:
                end_time = datetime.utcnow()
                start_time = end_time - timedelta(hours=1)
                time_range = {'start': start_time, 'end': end_time}

            url = f"{self.base_url}/data/browse/1.0.0/collections/{product}/items"

            params = {
                'bbox': f"{bbox['min_lon']},{bbox['min_lat']},{bbox['max_lon']},{bbox['max_lat']}",
                'datetime': f"{time_range['start'].isoformat()}/{time_range['end'].isoformat()}",
                'limit': 10
            }

            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()

            data = response.json()

            # Parse and return the latest image
            if 'features' in data and data['features']:
                latest = data['features'][0]
                return self._parse_imagery(latest, product)

            logger.warning(f"No imagery found for product {product}")
            return None

        except Exception as e:
            logger.error(f"Error fetching EUMETSAT imagery: {e}")
            return None

    def get_lightning_data(self, bbox: Dict[str, float]) -> List[Dict]:
        """
        Get lightning detection data from MTG Lightning Imager.

        Note: Requires MTG (Meteosat Third Generation) satellites which
        include the Lightning Imager (LI) instrument.

        Args:
            bbox: Bounding box with keys: min_lat, max_lat, min_lon, max_lon

        Returns:
            List of lightning detections
        """
        try:
            if not self._authenticate():
                return []

            # MTG Lightning Imager product
            product = "MTG-LI-2-FD"

            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=30)

            url = f"{self.base_url}/data/browse/1.0.0/collections/{product}/items"

            params = {
                'bbox': f"{bbox['min_lon']},{bbox['min_lat']},{bbox['max_lon']},{bbox['max_lat']}",
                'datetime': f"{start_time.isoformat()}/{end_time.isoformat()}"
            }

            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()

            data = response.json()

            # Parse lightning detections
            detections = self._parse_lightning_data(data)

            logger.info(f"Fetched {len(detections)} lightning detections from EUMETSAT")
            return detections

        except Exception as e:
            logger.error(f"Error fetching EUMETSAT lightning data: {e}")
            return []

    def get_cloud_top_data(self, bbox: Dict[str, float]) -> Optional[Dict]:
        """
        Get cloud top height and temperature data.

        High cloud tops indicate strong convection and potential for severe weather.

        Args:
            bbox: Bounding box

        Returns:
            Dictionary with cloud top statistics
        """
        try:
            # Use infrared channel to estimate cloud top properties
            imagery = self.get_satellite_imagery('MSG-IR', bbox)

            if not imagery:
                return None

            # Extract cloud top information
            cloud_data = {
                'max_height': imagery.get('max_cloud_top_height', 0),
                'min_temperature': imagery.get('min_brightness_temp', 0),
                'timestamp': imagery.get('timestamp'),
                'image_url': imagery.get('image_url')
            }

            # Estimate convection strength
            if cloud_data['max_height'] > 12000:  # meters
                cloud_data['convection_strength'] = 'strong'
            elif cloud_data['max_height'] > 8000:
                cloud_data['convection_strength'] = 'moderate'
            else:
                cloud_data['convection_strength'] = 'weak'

            return cloud_data

        except Exception as e:
            logger.error(f"Error fetching cloud top data: {e}")
            return None

    def _parse_imagery(self, feature: Dict, product: str) -> Dict:
        """Parse imagery feature into standardized format."""
        try:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})

            parsed = {
                'product': product,
                'timestamp': properties.get('datetime'),
                'image_url': None,
                'preview_url': None,
                'bbox': geometry.get('coordinates', []),
                'metadata': properties
            }

            # Extract image URLs
            assets = feature.get('assets', {})
            if 'data' in assets:
                parsed['image_url'] = assets['data'].get('href')
            if 'thumbnail' in assets:
                parsed['preview_url'] = assets['thumbnail'].get('href')

            # Extract brightness temperature for IR products
            if 'MSG-IR' in product:
                # These values would come from actual image analysis
                # This is a simplified example
                parsed['min_brightness_temp'] = properties.get('brightness_temperature_min', -70)
                parsed['max_cloud_top_height'] = self._estimate_cloud_top_height(
                    parsed['min_brightness_temp']
                )

            return parsed

        except Exception as e:
            logger.error(f"Error parsing imagery: {e}")
            return {}

    def _parse_lightning_data(self, data: Dict) -> List[Dict]:
        """Parse lightning detection data."""
        detections = []

        try:
            features = data.get('features', [])

            for feature in features:
                properties = feature.get('properties', {})
                geometry = feature.get('geometry', {})

                detection = {
                    'timestamp': properties.get('datetime'),
                    'latitude': geometry.get('coordinates', [0, 0])[1],
                    'longitude': geometry.get('coordinates', [0, 0])[0],
                    'radiance': properties.get('radiance', 0),
                    'source': 'eumetsat',
                    'instrument': 'MTG-LI'
                }

                detections.append(detection)

        except Exception as e:
            logger.error(f"Error parsing lightning data: {e}")

        return detections

    def _estimate_cloud_top_height(self, brightness_temp: float) -> float:
        """
        Estimate cloud top height from infrared brightness temperature.

        Uses a simplified atmospheric temperature profile.

        Args:
            brightness_temp: Brightness temperature in Celsius

        Returns:
            Estimated height in meters
        """
        try:
            # Simplified estimation using standard atmosphere
            # Real implementation would use actual atmospheric profile

            if brightness_temp > 0:
                # Low clouds
                return 2000
            elif brightness_temp > -20:
                # Mid-level clouds
                return 5000
            elif brightness_temp > -40:
                # High clouds
                return 8000
            elif brightness_temp > -55:
                # Very high clouds (strong convection)
                return 12000
            else:
                # Overshooting tops (severe convection)
                return 15000

        except Exception as e:
            logger.error(f"Error estimating cloud top height: {e}")
            return 0

    def get_water_vapor_imagery(self, bbox: Dict[str, float]) -> Optional[Dict]:
        """
        Get water vapor channel imagery.

        Water vapor imagery shows moisture in the upper atmosphere,
        useful for identifying areas of potential storm development.

        Args:
            bbox: Bounding box

        Returns:
            Dictionary with water vapor imagery data
        """
        try:
            return self.get_satellite_imagery('MSG-WV', bbox)

        except Exception as e:
            logger.error(f"Error fetching water vapor imagery: {e}")
            return None
