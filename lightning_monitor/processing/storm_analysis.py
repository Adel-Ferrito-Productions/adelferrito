"""
Storm Analysis Module

Analyzes storm development, tracks storm motion, and predicts
thunderstorm potential using atmospheric instability indices.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

logger = logging.getLogger(__name__)


class StormAnalyzer:
    """Analyzes storm activity and atmospheric conditions."""

    def __init__(self, config: Dict):
        """
        Initialize storm analyzer.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.processing_config = config.get('processing', {})
        self.lightning_config = self.processing_config.get('lightning', {})
        self.atmospheric_config = self.processing_config.get('atmospheric', {})
        self.tracking_config = self.processing_config.get('storm_tracking', {})

        # Historical data for tracking
        self.storm_history = []

        logger.info("Storm analyzer initialized")

    def analyze_lightning_activity(
        self,
        lightning_gdf: gpd.GeoDataFrame
    ) -> Dict:
        """
        Analyze lightning strike patterns and trends.

        Args:
            lightning_gdf: GeoDataFrame with lightning strikes

        Returns:
            Dictionary with lightning activity analysis
        """
        try:
            if lightning_gdf.empty:
                return {
                    'total_strikes': 0,
                    'strike_rate': 0.0,
                    'trend': 'none',
                    'severity': 'none'
                }

            now = datetime.utcnow()

            # Count strikes in different time windows
            strikes_10min = self._count_recent_strikes(lightning_gdf, now, minutes=10)
            strikes_30min = self._count_recent_strikes(lightning_gdf, now, minutes=30)
            strikes_60min = len(lightning_gdf)

            # Calculate strike rate (strikes per minute)
            strike_rate = strikes_10min / 10.0 if strikes_10min > 0 else 0.0

            # Determine trend
            trend = self._calculate_strike_trend(
                strikes_10min,
                strikes_30min,
                strikes_60min
            )

            # Calculate severity
            severity = self._calculate_lightning_severity(
                strikes_10min,
                strike_rate,
                lightning_gdf
            )

            # Get closest strike distance
            center_point = Point(
                self.config['location']['center']['longitude'],
                self.config['location']['center']['latitude']
            )

            if not lightning_gdf.empty:
                min_distance = lightning_gdf['distance_km'].min()
            else:
                min_distance = float('inf')

            analysis = {
                'total_strikes': strikes_60min,
                'strikes_10min': strikes_10min,
                'strikes_30min': strikes_30min,
                'strike_rate': round(strike_rate, 2),
                'trend': trend,
                'severity': severity,
                'closest_strike_km': round(min_distance, 1),
                'timestamp': now.isoformat()
            }

            logger.info(f"Lightning analysis: {strikes_10min} strikes (10min), "
                       f"rate: {strike_rate:.2f}/min, trend: {trend}")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing lightning activity: {e}")
            return {}

    def analyze_atmospheric_instability(
        self,
        weather_data: Dict
    ) -> Dict:
        """
        Analyze atmospheric instability indices.

        Args:
            weather_data: Weather model data with CAPE, Lifted Index, etc.

        Returns:
            Dictionary with instability analysis
        """
        try:
            # Extract key indices
            cape = weather_data.get('cape', {}).get('mean', 0)
            lifted_index = weather_data.get('lifted_index', {}).get('mean', 0)

            # Get thresholds from config
            cape_threshold = self.atmospheric_config.get('cape_threshold', 1000)
            li_threshold = self.atmospheric_config.get('lifted_index_threshold', -3)

            # Analyze CAPE
            cape_analysis = self._analyze_cape(cape, cape_threshold)

            # Analyze Lifted Index
            li_analysis = self._analyze_lifted_index(lifted_index, li_threshold)

            # Calculate combined thunderstorm potential
            ts_potential = self._calculate_thunderstorm_potential(
                cape,
                lifted_index,
                weather_data
            )

            analysis = {
                'cape': cape,
                'cape_category': cape_analysis['category'],
                'lifted_index': lifted_index,
                'li_category': li_analysis['category'],
                'thunderstorm_potential': ts_potential['potential'],
                'risk_level': ts_potential['risk_level'],
                'interpretation': self._generate_interpretation(
                    cape_analysis,
                    li_analysis,
                    ts_potential
                ),
                'timestamp': datetime.utcnow().isoformat()
            }

            logger.info(f"Atmospheric analysis: CAPE={cape:.0f}, LI={lifted_index:.1f}, "
                       f"TS potential={ts_potential['potential']}")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing atmospheric instability: {e}")
            return {}

    def track_storm_motion(
        self,
        current_cells: gpd.GeoDataFrame,
        previous_cells: Optional[gpd.GeoDataFrame] = None
    ) -> Dict:
        """
        Track storm cell motion and predict movement.

        Args:
            current_cells: Current storm cells
            previous_cells: Previous storm cells (from earlier time)

        Returns:
            Dictionary with storm motion vectors and predictions
        """
        try:
            if current_cells.empty:
                return {
                    'num_cells': 0,
                    'motion_vectors': [],
                    'predictions': []
                }

            motion_vectors = []
            predictions = []

            # If we have previous cells, calculate motion
            if previous_cells is not None and not previous_cells.empty:
                motion_vectors = self._calculate_motion_vectors(
                    previous_cells,
                    current_cells
                )

                # Predict future positions
                if motion_vectors:
                    predictions = self._predict_storm_positions(
                        current_cells,
                        motion_vectors
                    )

            # Store current cells in history
            self._update_storm_history(current_cells)

            tracking = {
                'num_cells': len(current_cells),
                'motion_vectors': motion_vectors,
                'predictions': predictions,
                'timestamp': datetime.utcnow().isoformat()
            }

            if motion_vectors:
                logger.info(f"Tracked {len(motion_vectors)} storm cells with motion")

            return tracking

        except Exception as e:
            logger.error(f"Error tracking storm motion: {e}")
            return {}

    def _count_recent_strikes(
        self,
        gdf: gpd.GeoDataFrame,
        reference_time: datetime,
        minutes: int
    ) -> int:
        """Count strikes within specified time window."""
        try:
            cutoff = reference_time - timedelta(minutes=minutes)
            recent = gdf[gdf['timestamp'] >= cutoff]
            return len(recent)
        except Exception as e:
            logger.error(f"Error counting recent strikes: {e}")
            return 0

    def _calculate_strike_trend(
        self,
        strikes_10min: int,
        strikes_30min: int,
        strikes_60min: int
    ) -> str:
        """Determine if strike activity is increasing, decreasing, or steady."""
        try:
            # Calculate rates for different windows
            rate_10 = strikes_10min / 10.0
            rate_30 = strikes_30min / 30.0
            rate_60 = strikes_60min / 60.0

            # Compare recent rate to longer-term rates
            if rate_10 > rate_30 * 1.5 and rate_30 > rate_60 * 1.2:
                return 'rapidly_increasing'
            elif rate_10 > rate_30 * 1.2:
                return 'increasing'
            elif rate_10 < rate_30 * 0.7 and rate_30 < rate_60 * 0.8:
                return 'rapidly_decreasing'
            elif rate_10 < rate_30 * 0.8:
                return 'decreasing'
            else:
                return 'steady'

        except Exception as e:
            logger.error(f"Error calculating strike trend: {e}")
            return 'unknown'

    def _calculate_lightning_severity(
        self,
        strikes_10min: int,
        strike_rate: float,
        gdf: gpd.GeoDataFrame
    ) -> str:
        """Calculate lightning severity level."""
        try:
            min_strikes = self.lightning_config.get('min_strikes_for_alert', 15)
            rate_threshold = self.lightning_config.get('rate_change_threshold', 2.0)

            if strikes_10min >= min_strikes * 2 or strike_rate >= rate_threshold * 2:
                return 'severe'
            elif strikes_10min >= min_strikes or strike_rate >= rate_threshold:
                return 'moderate'
            elif strikes_10min >= min_strikes / 2:
                return 'light'
            else:
                return 'minimal'

        except Exception as e:
            logger.error(f"Error calculating lightning severity: {e}")
            return 'unknown'

    def _analyze_cape(self, cape: float, threshold: float) -> Dict:
        """Analyze CAPE value and categorize."""
        categories = {
            'extreme': (2500, float('inf'), 'Extreme instability - severe storms likely'),
            'high': (1500, 2500, 'High instability - strong storms possible'),
            'moderate': (1000, 1500, 'Moderate instability - storms possible'),
            'weak': (500, 1000, 'Weak instability - isolated storms possible'),
            'minimal': (0, 500, 'Minimal instability - storms unlikely')
        }

        for category, (min_val, max_val, description) in categories.items():
            if min_val <= cape < max_val:
                return {
                    'category': category,
                    'description': description,
                    'exceeds_threshold': cape >= threshold
                }

        return {
            'category': 'unknown',
            'description': 'Unable to categorize',
            'exceeds_threshold': False
        }

    def _analyze_lifted_index(self, li: float, threshold: float) -> Dict:
        """Analyze Lifted Index value and categorize."""
        # Note: More negative LI = more unstable
        categories = {
            'extreme': (float('-inf'), -6, 'Extreme instability'),
            'high': (-6, -3, 'High instability'),
            'moderate': (-3, -1, 'Moderate instability'),
            'weak': (-1, 2, 'Weak instability'),
            'stable': (2, float('inf'), 'Stable atmosphere')
        }

        for category, (min_val, max_val, description) in categories.items():
            if min_val <= li < max_val:
                return {
                    'category': category,
                    'description': description,
                    'exceeds_threshold': li <= threshold
                }

        return {
            'category': 'unknown',
            'description': 'Unable to categorize',
            'exceeds_threshold': False
        }

    def _calculate_thunderstorm_potential(
        self,
        cape: float,
        lifted_index: float,
        weather_data: Dict
    ) -> Dict:
        """Calculate combined thunderstorm potential score."""
        try:
            # Base score from CAPE (0-50 points)
            cape_score = min(50, (cape / 2500) * 50)

            # Score from Lifted Index (0-30 points)
            if lifted_index < -6:
                li_score = 30
            elif lifted_index < -3:
                li_score = 25
            elif lifted_index < -1:
                li_score = 15
            elif lifted_index < 0:
                li_score = 10
            else:
                li_score = 0

            # Additional factors (0-20 points)
            extra_score = 0

            # Wind shear (if available)
            if 'wind' in weather_data:
                wind_data = weather_data['wind']
                if isinstance(wind_data, dict) and 'mean' in wind_data:
                    wind_speed = wind_data['mean']
                    if wind_speed > 15:  # m/s
                        extra_score += 10

            # Temperature (if available)
            if 'temp' in weather_data:
                temp_data = weather_data['temp']
                if isinstance(temp_data, dict) and 'mean' in temp_data:
                    temp = temp_data['mean']
                    if temp > 25:  # Celsius
                        extra_score += 5

            # Moisture (if available)
            if 'humidity' in weather_data:
                humidity_data = weather_data['humidity']
                if isinstance(humidity_data, dict) and 'mean' in humidity_data:
                    humidity = humidity_data['mean']
                    if humidity > 70:
                        extra_score += 5

            # Total potential score (0-100)
            total_score = cape_score + li_score + extra_score

            # Determine risk level
            if total_score >= 80:
                risk_level = 'extreme'
            elif total_score >= 60:
                risk_level = 'high'
            elif total_score >= 40:
                risk_level = 'moderate'
            elif total_score >= 20:
                risk_level = 'low'
            else:
                risk_level = 'minimal'

            return {
                'potential': round(total_score, 1),
                'risk_level': risk_level,
                'components': {
                    'cape_score': round(cape_score, 1),
                    'li_score': round(li_score, 1),
                    'extra_score': round(extra_score, 1)
                }
            }

        except Exception as e:
            logger.error(f"Error calculating thunderstorm potential: {e}")
            return {'potential': 0, 'risk_level': 'unknown'}

    def _generate_interpretation(
        self,
        cape_analysis: Dict,
        li_analysis: Dict,
        ts_potential: Dict
    ) -> str:
        """Generate human-readable interpretation of conditions."""
        interpretation_parts = []

        # CAPE interpretation
        interpretation_parts.append(cape_analysis.get('description', ''))

        # LI interpretation
        interpretation_parts.append(li_analysis.get('description', ''))

        # Overall risk
        risk = ts_potential.get('risk_level', 'unknown')
        if risk == 'extreme':
            interpretation_parts.append("Severe thunderstorms likely with potential for damaging weather.")
        elif risk == 'high':
            interpretation_parts.append("Strong thunderstorms possible.")
        elif risk == 'moderate':
            interpretation_parts.append("Thunderstorm development possible.")
        elif risk == 'low':
            interpretation_parts.append("Isolated thunderstorms may develop.")
        else:
            interpretation_parts.append("Thunderstorm development unlikely.")

        return " ".join(interpretation_parts)

    def _calculate_motion_vectors(
        self,
        previous_cells: gpd.GeoDataFrame,
        current_cells: gpd.GeoDataFrame
    ) -> List[Dict]:
        """Calculate motion vectors by matching cells between time steps."""
        vectors = []

        try:
            # Simple matching: nearest neighbor
            for i, current in current_cells.iterrows():
                # Find nearest previous cell
                distances = previous_cells.geometry.distance(current.geometry)
                if len(distances) > 0:
                    nearest_idx = distances.idxmin()
                    previous = previous_cells.loc[nearest_idx]

                    # Calculate motion
                    dx = current.geometry.centroid.x - previous.geometry.centroid.x
                    dy = current.geometry.centroid.y - previous.geometry.centroid.y

                    # Time difference (assume from timestamps)
                    time_diff = (current['last_strike'] - previous['last_strike']).total_seconds() / 3600.0

                    if time_diff > 0:
                        # Speed in degrees per hour (approximate)
                        speed_x = dx / time_diff
                        speed_y = dy / time_diff

                        vectors.append({
                            'cell_id': current.get('cell_id', i),
                            'dx': dx,
                            'dy': dy,
                            'speed_x': speed_x,
                            'speed_y': speed_y,
                            'time_diff_hours': time_diff
                        })

        except Exception as e:
            logger.error(f"Error calculating motion vectors: {e}")

        return vectors

    def _predict_storm_positions(
        self,
        current_cells: gpd.GeoDataFrame,
        motion_vectors: List[Dict]
    ) -> List[Dict]:
        """Predict future storm positions based on motion vectors."""
        predictions = []

        try:
            # Predict positions for next 30, 60, 90, 120 minutes
            prediction_times = [0.5, 1.0, 1.5, 2.0]  # hours

            for vector in motion_vectors:
                cell_id = vector['cell_id']
                cell = current_cells[current_cells['cell_id'] == cell_id].iloc[0]

                current_center = cell.geometry.centroid

                for pred_time in prediction_times:
                    pred_x = current_center.x + vector['speed_x'] * pred_time
                    pred_y = current_center.y + vector['speed_y'] * pred_time

                    predictions.append({
                        'cell_id': cell_id,
                        'prediction_time_minutes': int(pred_time * 60),
                        'predicted_lat': pred_y,
                        'predicted_lon': pred_x
                    })

        except Exception as e:
            logger.error(f"Error predicting storm positions: {e}")

        return predictions

    def _update_storm_history(self, cells: gpd.GeoDataFrame):
        """Update storm history with current cells."""
        try:
            self.storm_history.append({
                'timestamp': datetime.utcnow(),
                'cells': cells.copy()
            })

            # Keep only last hour of history
            cutoff = datetime.utcnow() - timedelta(hours=1)
            self.storm_history = [
                h for h in self.storm_history
                if h['timestamp'] >= cutoff
            ]

        except Exception as e:
            logger.error(f"Error updating storm history: {e}")
