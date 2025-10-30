"""
Windy API Weather Data Ingestion Module

Fetches meteorological data including CAPE, Lifted Index, and other
atmospheric parameters from Windy's weather models.
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np

logger = logging.getLogger(__name__)


class WindyClient:
    """Client for fetching weather data from Windy API."""

    def __init__(self, api_key: str, config: Dict):
        """
        Initialize Windy API client.

        Args:
            api_key: Windy API key
            config: Configuration dictionary with Windy settings
        """
        self.api_key = api_key
        self.base_url = config.get('base_url', 'https://api.windy.com/api')
        self.parameters = config.get('parameters', [])
        self.session = requests.Session()

        logger.info("Windy client initialized")

    def get_point_forecast(
        self,
        lat: float,
        lon: float,
        parameters: Optional[List[str]] = None
    ) -> Dict:
        """
        Get forecast data for a specific point.

        Args:
            lat: Latitude
            lon: Longitude
            parameters: List of parameters to fetch (uses config default if None)

        Returns:
            Dictionary with forecast data
        """
        try:
            if parameters is None:
                parameters = self.parameters

            url = f"{self.base_url}/point-forecast/v2"

            payload = {
                'lat': lat,
                'lon': lon,
                'model': 'gfs',  # Global Forecast System
                'parameters': parameters,
                'levels': ['surface', '850h', '700h', '500h'],
                'key': self.api_key
            }

            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Fetched Windy forecast for ({lat}, {lon})")

            return self._parse_forecast(data)

        except Exception as e:
            logger.error(f"Error fetching Windy point forecast: {e}")
            return {}

    def get_area_forecast(
        self,
        bbox: Dict[str, float],
        parameters: Optional[List[str]] = None
    ) -> Dict:
        """
        Get forecast data for an area (bounding box).

        Args:
            bbox: Bounding box with keys: min_lat, max_lat, min_lon, max_lon
            parameters: List of parameters to fetch

        Returns:
            Dictionary with area forecast data
        """
        try:
            # Sample multiple points within the bounding box
            sample_points = self._generate_sample_points(bbox, grid_size=3)

            forecasts = []
            for point in sample_points:
                forecast = self.get_point_forecast(
                    point['lat'],
                    point['lon'],
                    parameters
                )
                if forecast:
                    forecast['sample_lat'] = point['lat']
                    forecast['sample_lon'] = point['lon']
                    forecasts.append(forecast)

            # Aggregate forecasts
            aggregated = self._aggregate_forecasts(forecasts, bbox)

            logger.info(f"Fetched Windy area forecast with {len(forecasts)} sample points")
            return aggregated

        except Exception as e:
            logger.error(f"Error fetching Windy area forecast: {e}")
            return {}

    def get_thunder_probability(self, lat: float, lon: float) -> Dict:
        """
        Get thunder probability forecast.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with thunder probability data
        """
        try:
            forecast = self.get_point_forecast(lat, lon, parameters=['thunder'])

            if 'thunder' in forecast:
                return {
                    'current': forecast['thunder'].get('current', 0),
                    'max_24h': forecast['thunder'].get('max', 0),
                    'forecast': forecast['thunder'].get('forecast', [])
                }

            return {'current': 0, 'max_24h': 0, 'forecast': []}

        except Exception as e:
            logger.error(f"Error fetching thunder probability: {e}")
            return {}

    def get_instability_indices(self, lat: float, lon: float) -> Dict:
        """
        Get atmospheric instability indices (CAPE, Lifted Index).

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with instability indices
        """
        try:
            parameters = ['cape', 'lifted_index', 'temp', 'pressure']
            forecast = self.get_point_forecast(lat, lon, parameters)

            indices = {
                'cape': forecast.get('cape', {}).get('current', 0),
                'lifted_index': forecast.get('lifted_index', {}).get('current', 0),
                'temperature': forecast.get('temp', {}).get('current', 0),
                'pressure': forecast.get('pressure', {}).get('current', 0),
                'timestamp': datetime.utcnow().isoformat()
            }

            # Calculate derived indices
            indices['instability_score'] = self._calculate_instability_score(indices)

            return indices

        except Exception as e:
            logger.error(f"Error fetching instability indices: {e}")
            return {}

    def _generate_sample_points(
        self,
        bbox: Dict[str, float],
        grid_size: int = 3
    ) -> List[Dict]:
        """Generate sample points within bounding box."""
        points = []

        lat_step = (bbox['max_lat'] - bbox['min_lat']) / (grid_size + 1)
        lon_step = (bbox['max_lon'] - bbox['min_lon']) / (grid_size + 1)

        for i in range(1, grid_size + 1):
            for j in range(1, grid_size + 1):
                lat = bbox['min_lat'] + i * lat_step
                lon = bbox['min_lon'] + j * lon_step
                points.append({'lat': lat, 'lon': lon})

        return points

    def _parse_forecast(self, data: Dict) -> Dict:
        """Parse Windy API response into standardized format."""
        parsed = {}

        # Extract timestamp
        if 'ts' in data:
            timestamps = data['ts']
            parsed['timestamps'] = [
                datetime.fromtimestamp(ts / 1000) for ts in timestamps
            ]

        # Parse each parameter
        for param in self.parameters:
            if param in data:
                param_data = data[param]

                if isinstance(param_data, list):
                    # Time series data
                    parsed[param] = {
                        'forecast': param_data,
                        'current': param_data[0] if param_data else 0,
                        'max': max(param_data) if param_data else 0,
                        'min': min(param_data) if param_data else 0,
                        'avg': sum(param_data) / len(param_data) if param_data else 0
                    }
                elif isinstance(param_data, dict):
                    # Nested data (e.g., multiple levels)
                    parsed[param] = param_data
                else:
                    # Single value
                    parsed[param] = {
                        'current': param_data,
                        'forecast': [param_data]
                    }

        return parsed

    def _aggregate_forecasts(
        self,
        forecasts: List[Dict],
        bbox: Dict[str, float]
    ) -> Dict:
        """Aggregate multiple point forecasts into area statistics."""
        if not forecasts:
            return {}

        aggregated = {
            'bbox': bbox,
            'num_samples': len(forecasts),
            'timestamp': datetime.utcnow().isoformat()
        }

        # Aggregate each parameter
        for param in self.parameters:
            values = []

            for forecast in forecasts:
                if param in forecast:
                    current = forecast[param].get('current', 0)
                    if current is not None:
                        values.append(current)

            if values:
                aggregated[param] = {
                    'max': max(values),
                    'min': min(values),
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'samples': values
                }

        return aggregated

    def _calculate_instability_score(self, indices: Dict) -> float:
        """
        Calculate composite instability score.

        Combines CAPE and Lifted Index into a single score.
        Higher scores indicate greater instability and thunderstorm potential.

        Returns:
            Score from 0 (stable) to 100 (very unstable)
        """
        try:
            cape = indices.get('cape', 0)
            li = indices.get('lifted_index', 0)

            # CAPE component (0-50 points)
            # CAPE > 2500 = maximum points
            cape_score = min(50, (cape / 2500) * 50)

            # Lifted Index component (0-50 points)
            # LI < -6 = maximum points
            li_score = 0
            if li < -6:
                li_score = 50
            elif li < -3:
                li_score = 40
            elif li < -1:
                li_score = 25
            elif li < 0:
                li_score = 15
            elif li < 2:
                li_score = 5

            total_score = cape_score + li_score

            return round(total_score, 2)

        except Exception as e:
            logger.error(f"Error calculating instability score: {e}")
            return 0.0

    def get_radar_overlay(self, bbox: Dict[str, float]) -> Optional[str]:
        """
        Get radar overlay image URL for the area.

        Args:
            bbox: Bounding box

        Returns:
            URL to radar overlay image, or None if unavailable
        """
        try:
            # Windy provides map overlays via their tile service
            center_lat = (bbox['min_lat'] + bbox['max_lat']) / 2
            center_lon = (bbox['min_lon'] + bbox['max_lon']) / 2

            # Calculate appropriate zoom level
            lat_span = bbox['max_lat'] - bbox['min_lat']
            lon_span = bbox['max_lon'] - bbox['min_lon']
            zoom = self._calculate_zoom_level(max(lat_span, lon_span))

            # Windy map URL (requires API key parameter)
            url = (
                f"https://embed.windy.com/embed2.html"
                f"?lat={center_lat}&lon={center_lon}&zoom={zoom}"
                f"&level=surface&overlay=radar&product=ecmwf"
                f"&menu=&message=&marker=&calendar=now"
                f"&pressure=&type=map&location=coordinates"
                f"&detail=&metricWind=default&metricTemp=default"
                f"&radarRange=-1"
            )

            return url

        except Exception as e:
            logger.error(f"Error generating radar overlay URL: {e}")
            return None

    def _calculate_zoom_level(self, span_degrees: float) -> int:
        """Calculate appropriate zoom level for given span."""
        if span_degrees > 10:
            return 5
        elif span_degrees > 5:
            return 7
        elif span_degrees > 2:
            return 9
        else:
            return 11
