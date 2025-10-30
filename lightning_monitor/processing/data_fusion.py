"""
Data Fusion Engine

Combines data from multiple sources (lightning, weather models, satellite)
into a unified GeoPandas-based dataset for analysis.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import numpy as np

logger = logging.getLogger(__name__)


class DataFusionEngine:
    """Fuses data from multiple weather sources into unified datasets."""

    def __init__(self, config: Dict):
        """
        Initialize data fusion engine.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.location = config.get('location', {})
        self.center = Point(
            self.location.get('center', {}).get('longitude', 14.3754),
            self.location.get('center', {}).get('latitude', 35.9375)
        )
        self.monitoring_radius = self.location.get('monitoring_radius_km', 100)

        logger.info("Data fusion engine initialized")

    def create_lightning_geodataframe(
        self,
        strikes: List[Dict]
    ) -> gpd.GeoDataFrame:
        """
        Convert lightning strikes to GeoDataFrame.

        Args:
            strikes: List of strike dictionaries

        Returns:
            GeoDataFrame with lightning strikes
        """
        try:
            if not strikes:
                # Return empty GeoDataFrame with correct schema
                return gpd.GeoDataFrame(
                    columns=['timestamp', 'intensity', 'source', 'geometry'],
                    crs='EPSG:4326'
                )

            # Create DataFrame
            df = pd.DataFrame(strikes)

            # Create Point geometries
            geometry = [
                Point(strike['longitude'], strike['latitude'])
                for strike in strikes
            ]

            # Create GeoDataFrame
            gdf = gpd.GeoDataFrame(
                df,
                geometry=geometry,
                crs='EPSG:4326'
            )

            # Calculate distance from monitoring center
            gdf['distance_km'] = gdf.geometry.apply(
                lambda x: self._calculate_distance(x, self.center)
            )

            # Filter to monitoring radius
            gdf = gdf[gdf['distance_km'] <= self.monitoring_radius]

            logger.info(f"Created lightning GeoDataFrame with {len(gdf)} strikes")
            return gdf

        except Exception as e:
            logger.error(f"Error creating lightning GeoDataFrame: {e}")
            return gpd.GeoDataFrame(crs='EPSG:4326')

    def fuse_weather_data(
        self,
        lightning_gdf: gpd.GeoDataFrame,
        weather_data: Dict,
        satellite_data: Optional[Dict] = None
    ) -> gpd.GeoDataFrame:
        """
        Fuse lightning data with weather model and satellite data.

        Args:
            lightning_gdf: GeoDataFrame with lightning strikes
            weather_data: Weather model data (CAPE, Lifted Index, etc.)
            satellite_data: Optional satellite data

        Returns:
            Enhanced GeoDataFrame with fused data
        """
        try:
            # Add weather attributes to lightning strikes
            if not lightning_gdf.empty:
                lightning_gdf = self._add_weather_attributes(
                    lightning_gdf,
                    weather_data
                )

            # Add satellite attributes if available
            if satellite_data and not lightning_gdf.empty:
                lightning_gdf = self._add_satellite_attributes(
                    lightning_gdf,
                    satellite_data
                )

            logger.info("Weather data fusion completed")
            return lightning_gdf

        except Exception as e:
            logger.error(f"Error fusing weather data: {e}")
            return lightning_gdf

    def create_storm_cells(
        self,
        lightning_gdf: gpd.GeoDataFrame,
        cluster_distance_km: float = 10.0
    ) -> gpd.GeoDataFrame:
        """
        Identify storm cells by clustering lightning strikes.

        Args:
            lightning_gdf: GeoDataFrame with lightning strikes
            cluster_distance_km: Distance threshold for clustering (km)

        Returns:
            GeoDataFrame with storm cell polygons
        """
        try:
            if lightning_gdf.empty or len(lightning_gdf) < 3:
                return gpd.GeoDataFrame(crs='EPSG:4326')

            # Convert to projected CRS for accurate distance calculations
            gdf_proj = lightning_gdf.to_crs('EPSG:3857')  # Web Mercator (meters)

            # Buffer strikes by cluster distance
            cluster_distance_m = cluster_distance_km * 1000
            buffered = gdf_proj.geometry.buffer(cluster_distance_m)

            # Dissolve overlapping buffers to create storm cells
            dissolved = buffered.unary_union

            # Convert back to individual polygons
            if dissolved.geom_type == 'Polygon':
                cells = [dissolved]
            elif dissolved.geom_type == 'MultiPolygon':
                cells = list(dissolved.geoms)
            else:
                cells = []

            # Create GeoDataFrame of storm cells
            cell_data = []
            for i, cell in enumerate(cells):
                # Find strikes within this cell
                cell_gdf = gpd.GeoDataFrame({'geometry': [cell]}, crs='EPSG:3857')
                strikes_in_cell = gpd.sjoin(
                    gdf_proj,
                    cell_gdf,
                    how='inner',
                    predicate='within'
                )

                if len(strikes_in_cell) > 0:
                    cell_data.append({
                        'cell_id': i,
                        'num_strikes': len(strikes_in_cell),
                        'avg_intensity': strikes_in_cell['intensity'].mean(),
                        'first_strike': strikes_in_cell['timestamp'].min(),
                        'last_strike': strikes_in_cell['timestamp'].max(),
                        'geometry': cell
                    })

            # Create GeoDataFrame
            if cell_data:
                cells_gdf = gpd.GeoDataFrame(cell_data, crs='EPSG:3857')
                # Convert back to WGS84
                cells_gdf = cells_gdf.to_crs('EPSG:4326')

                logger.info(f"Identified {len(cells_gdf)} storm cells")
                return cells_gdf
            else:
                return gpd.GeoDataFrame(crs='EPSG:4326')

        except Exception as e:
            logger.error(f"Error creating storm cells: {e}")
            return gpd.GeoDataFrame(crs='EPSG:4326')

    def calculate_strike_density(
        self,
        lightning_gdf: gpd.GeoDataFrame,
        grid_size_km: float = 5.0
    ) -> gpd.GeoDataFrame:
        """
        Calculate lightning strike density on a grid.

        Args:
            lightning_gdf: GeoDataFrame with lightning strikes
            grid_size_km: Grid cell size in kilometers

        Returns:
            GeoDataFrame with grid cells and strike counts
        """
        try:
            if lightning_gdf.empty:
                return gpd.GeoDataFrame(crs='EPSG:4326')

            # Get bounding box
            bbox = self.config.get('location', {}).get('bbox', {})
            min_lon = bbox.get('min_lon', 13.0)
            max_lon = bbox.get('max_lon', 15.5)
            min_lat = bbox.get('min_lat', 35.0)
            max_lat = bbox.get('max_lat', 37.0)

            # Calculate grid
            # Approximate: 1 degree latitude ≈ 111 km
            lat_step = grid_size_km / 111.0
            # 1 degree longitude varies with latitude, use average
            avg_lat = (min_lat + max_lat) / 2
            lon_step = grid_size_km / (111.0 * np.cos(np.radians(avg_lat)))

            # Create grid cells
            grid_cells = []
            lats = np.arange(min_lat, max_lat, lat_step)
            lons = np.arange(min_lon, max_lon, lon_step)

            for lat in lats:
                for lon in lons:
                    # Create polygon for grid cell
                    cell_polygon = Polygon([
                        (lon, lat),
                        (lon + lon_step, lat),
                        (lon + lon_step, lat + lat_step),
                        (lon, lat + lat_step),
                        (lon, lat)
                    ])

                    grid_cells.append({
                        'lat': lat + lat_step / 2,
                        'lon': lon + lon_step / 2,
                        'geometry': cell_polygon
                    })

            # Create GeoDataFrame
            grid_gdf = gpd.GeoDataFrame(grid_cells, crs='EPSG:4326')

            # Spatial join to count strikes in each cell
            joined = gpd.sjoin(
                lightning_gdf,
                grid_gdf,
                how='right',
                predicate='within'
            )

            # Count strikes per cell
            strike_counts = joined.groupby('index_right').size().reset_index(name='strike_count')

            # Merge back with grid
            grid_gdf = grid_gdf.reset_index().rename(columns={'index': 'index_right'})
            grid_gdf = grid_gdf.merge(strike_counts, on='index_right', how='left')
            grid_gdf['strike_count'] = grid_gdf['strike_count'].fillna(0)

            logger.info(f"Calculated strike density on {len(grid_gdf)} grid cells")
            return grid_gdf

        except Exception as e:
            logger.error(f"Error calculating strike density: {e}")
            return gpd.GeoDataFrame(crs='EPSG:4326')

    def _calculate_distance(self, point1: Point, point2: Point) -> float:
        """
        Calculate distance between two points in kilometers.

        Uses Haversine formula for accuracy over long distances.

        Args:
            point1: First point
            point2: Second point

        Returns:
            Distance in kilometers
        """
        try:
            # Convert to radians
            lat1 = np.radians(point1.y)
            lon1 = np.radians(point1.x)
            lat2 = np.radians(point2.y)
            lon2 = np.radians(point2.x)

            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
            c = 2 * np.arcsin(np.sqrt(a))

            # Earth radius in kilometers
            r = 6371

            return c * r

        except Exception as e:
            logger.error(f"Error calculating distance: {e}")
            return 0.0

    def _add_weather_attributes(
        self,
        gdf: gpd.GeoDataFrame,
        weather_data: Dict
    ) -> gpd.GeoDataFrame:
        """Add weather model attributes to GeoDataFrame."""
        try:
            # Add atmospheric parameters
            if 'cape' in weather_data:
                gdf['cape'] = weather_data['cape'].get('mean', 0)

            if 'lifted_index' in weather_data:
                gdf['lifted_index'] = weather_data['lifted_index'].get('mean', 0)

            if 'temp' in weather_data:
                gdf['temperature'] = weather_data['temp'].get('mean', 0)

            if 'pressure' in weather_data:
                gdf['pressure'] = weather_data['pressure'].get('mean', 0)

            return gdf

        except Exception as e:
            logger.error(f"Error adding weather attributes: {e}")
            return gdf

    def _add_satellite_attributes(
        self,
        gdf: gpd.GeoDataFrame,
        satellite_data: Dict
    ) -> gpd.GeoDataFrame:
        """Add satellite data attributes to GeoDataFrame."""
        try:
            # Add cloud top information
            if 'max_height' in satellite_data:
                gdf['cloud_top_height'] = satellite_data['max_height']

            if 'min_temperature' in satellite_data:
                gdf['cloud_top_temp'] = satellite_data['min_temperature']

            if 'convection_strength' in satellite_data:
                gdf['convection'] = satellite_data['convection_strength']

            return gdf

        except Exception as e:
            logger.error(f"Error adding satellite attributes: {e}")
            return gdf
