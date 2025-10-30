"""
Alert Rules Engine

Evaluates alert conditions based on configured rules and generates
alerts with appropriate severity levels.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

logger = logging.getLogger(__name__)


class AlertRulesEngine:
    """Evaluates alert rules and generates alerts."""

    def __init__(self, config: Dict):
        """
        Initialize alert rules engine.

        Args:
            config: Configuration dictionary with alert rules
        """
        self.config = config
        self.alert_config = config.get('alerts', {})
        self.levels = self.alert_config.get('levels', {})

        # Track recent alerts to prevent duplicates
        self.recent_alerts = []

        logger.info("Alert rules engine initialized")

    def evaluate_conditions(
        self,
        lightning_analysis: Dict,
        atmospheric_analysis: Dict,
        storm_tracking: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Evaluate all alert conditions and generate alerts.

        Args:
            lightning_analysis: Lightning activity analysis
            atmospheric_analysis: Atmospheric instability analysis
            storm_tracking: Optional storm tracking data

        Returns:
            List of alert dictionaries
        """
        alerts = []

        try:
            # Create context with all available data
            context = self._build_context(
                lightning_analysis,
                atmospheric_analysis,
                storm_tracking
            )

            # Evaluate each severity level
            for level_name, level_config in self.levels.items():
                conditions = level_config.get('conditions', [])

                if self._evaluate_rule_set(conditions, context):
                    alert = self._create_alert(
                        level_name,
                        context,
                        conditions
                    )

                    # Check if this is a duplicate
                    if not self._is_duplicate(alert):
                        alerts.append(alert)
                        self._add_to_recent(alert)
                        logger.info(f"Alert generated: {level_name} - {alert['title']}")

            return alerts

        except Exception as e:
            logger.error(f"Error evaluating alert conditions: {e}")
            return []

    def _build_context(
        self,
        lightning_analysis: Dict,
        atmospheric_analysis: Dict,
        storm_tracking: Optional[Dict]
    ) -> Dict:
        """Build evaluation context from all data sources."""
        context = {
            # Lightning metrics
            'strikes_10min': lightning_analysis.get('strikes_10min', 0),
            'strikes_30min': lightning_analysis.get('strikes_30min', 0),
            'strike_rate': lightning_analysis.get('strike_rate', 0),
            'strike_distance': lightning_analysis.get('closest_strike_km', float('inf')),
            'strike_trend': lightning_analysis.get('trend', 'unknown'),
            'strike_rate_increasing': lightning_analysis.get('trend', '') in [
                'increasing', 'rapidly_increasing'
            ],

            # Atmospheric metrics
            'cape': atmospheric_analysis.get('cape', 0),
            'lifted_index': atmospheric_analysis.get('lifted_index', 0),
            'thunderstorm_potential': atmospheric_analysis.get('thunderstorm_potential', 0),
            'risk_level': atmospheric_analysis.get('risk_level', 'unknown'),

            # Storm tracking metrics
            'num_storm_cells': 0,
            'storm_approaching': False
        }

        # Add storm tracking data if available
        if storm_tracking:
            context['num_storm_cells'] = storm_tracking.get('num_cells', 0)

            # Check if any storms are predicted to approach
            predictions = storm_tracking.get('predictions', [])
            if predictions:
                # Check if any predicted position is closer than current
                for pred in predictions:
                    pred_lat = pred.get('predicted_lat', 0)
                    pred_lon = pred.get('predicted_lon', 0)
                    # Simplified check - in real implementation would calculate distance
                    # from monitoring center
                    if pred.get('prediction_time_minutes', 0) <= 60:
                        context['storm_approaching'] = True
                        break

        return context

    def _evaluate_rule_set(self, conditions: List[str], context: Dict) -> bool:
        """
        Evaluate a set of conditions.

        All conditions must be true for the rule set to trigger.

        Args:
            conditions: List of condition strings
            context: Evaluation context with variables

        Returns:
            True if all conditions are met
        """
        try:
            for condition in conditions:
                if not self._evaluate_condition(condition, context):
                    return False

            return True if conditions else False

        except Exception as e:
            logger.error(f"Error evaluating rule set: {e}")
            return False

    def _evaluate_condition(self, condition: str, context: Dict) -> bool:
        """
        Evaluate a single condition.

        Conditions are simple expressions like:
        - "cape > 1000"
        - "strikes_10min > 15"
        - "strike_distance < 30"
        - "strike_rate_increasing"

        Args:
            condition: Condition string
            context: Evaluation context

        Returns:
            True if condition is met
        """
        try:
            condition = condition.strip()

            # Handle boolean flags
            if condition in context:
                return bool(context[condition])

            # Parse comparison expressions
            match = re.match(r'(\w+)\s*([<>=!]+)\s*([0-9.-]+)', condition)

            if match:
                variable = match.group(1)
                operator = match.group(2)
                threshold = float(match.group(3))

                if variable not in context:
                    logger.warning(f"Unknown variable in condition: {variable}")
                    return False

                value = context[variable]

                # Evaluate comparison
                if operator == '>':
                    return value > threshold
                elif operator == '>=':
                    return value >= threshold
                elif operator == '<':
                    return value < threshold
                elif operator == '<=':
                    return value <= threshold
                elif operator == '==':
                    return value == threshold
                elif operator == '!=':
                    return value != threshold
                else:
                    logger.warning(f"Unknown operator: {operator}")
                    return False

            else:
                logger.warning(f"Unable to parse condition: {condition}")
                return False

        except Exception as e:
            logger.error(f"Error evaluating condition '{condition}': {e}")
            return False

    def _create_alert(
        self,
        level: str,
        context: Dict,
        conditions: List[str]
    ) -> Dict:
        """Create alert dictionary."""
        try:
            # Generate alert title and message
            title = self._generate_title(level, context)
            message = self._generate_message(level, context)

            alert = {
                'level': level,
                'title': title,
                'message': message,
                'timestamp': datetime.utcnow().isoformat(),
                'context': context,
                'triggered_conditions': conditions
            }

            return alert

        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return {}

    def _generate_title(self, level: str, context: Dict) -> str:
        """Generate alert title based on level and context."""
        level_titles = {
            'info': 'Weather Information',
            'watch': 'Thunderstorm Watch',
            'warning': 'Lightning Warning',
            'urgent': 'URGENT: Lightning Alert'
        }

        base_title = level_titles.get(level, 'Weather Alert')

        # Add specifics based on context
        strikes = context.get('strikes_10min', 0)
        distance = context.get('strike_distance', float('inf'))

        if strikes > 0 and distance < 50:
            return f"{base_title} - {strikes} strikes within {distance:.1f} km"

        return base_title

    def _generate_message(self, level: str, context: Dict) -> str:
        """Generate detailed alert message."""
        message_parts = []

        # Lightning information
        strikes_10 = context.get('strikes_10min', 0)
        strikes_30 = context.get('strikes_30min', 0)
        distance = context.get('strike_distance', float('inf'))
        trend = context.get('strike_trend', 'unknown')

        if strikes_10 > 0:
            message_parts.append(
                f"⚡ Lightning activity: {strikes_10} strikes in last 10 minutes "
                f"({strikes_30} in 30 min)"
            )

            if distance < float('inf'):
                message_parts.append(f"📍 Closest strike: {distance:.1f} km from Malta center")

            if trend in ['increasing', 'rapidly_increasing']:
                message_parts.append(f"📈 Activity is {trend.replace('_', ' ')}")

        # Atmospheric information
        cape = context.get('cape', 0)
        li = context.get('lifted_index', 0)
        ts_potential = context.get('thunderstorm_potential', 0)

        if cape > 0 or li < 0:
            message_parts.append(
                f"\n🌡️ Atmospheric conditions:\n"
                f"  • CAPE: {cape:.0f} J/kg\n"
                f"  • Lifted Index: {li:.1f}\n"
                f"  • Thunderstorm potential: {ts_potential:.0f}%"
            )

        # Storm tracking information
        num_cells = context.get('num_storm_cells', 0)
        if num_cells > 0:
            message_parts.append(f"\n🌩️ {num_cells} active storm cell(s) detected")

        if context.get('storm_approaching', False):
            message_parts.append("⚠️ Storm system may be approaching Malta")

        # Safety recommendations based on level
        if level in ['warning', 'urgent']:
            message_parts.append(
                "\n⚠️ Safety recommendations:\n"
                "  • Seek shelter indoors\n"
                "  • Avoid open areas and tall objects\n"
                "  • Stay away from water and metal objects"
            )

        return "\n".join(message_parts)

    def _is_duplicate(self, alert: Dict) -> bool:
        """Check if this alert is a duplicate of a recent alert."""
        try:
            suppress_minutes = self.alert_config.get('notifications', {}).get(
                'rate_limit', {}
            ).get('suppress_duplicates_minutes', 15)

            cutoff = datetime.utcnow() - timedelta(minutes=suppress_minutes)

            # Check recent alerts
            for recent in self.recent_alerts:
                if recent['timestamp'] >= cutoff.isoformat():
                    # Same level and similar context
                    if recent['level'] == alert['level']:
                        # Check if context is similar
                        if self._contexts_similar(recent['context'], alert['context']):
                            logger.debug(f"Suppressing duplicate {alert['level']} alert")
                            return True

            return False

        except Exception as e:
            logger.error(f"Error checking for duplicate: {e}")
            return False

    def _contexts_similar(self, context1: Dict, context2: Dict) -> bool:
        """Check if two contexts are similar enough to be considered duplicates."""
        try:
            # Check key metrics
            key_metrics = ['strikes_10min', 'strike_distance', 'cape', 'lifted_index']

            for metric in key_metrics:
                val1 = context1.get(metric, 0)
                val2 = context2.get(metric, 0)

                # Allow 20% variation
                if val1 > 0 and val2 > 0:
                    diff = abs(val1 - val2) / max(val1, val2)
                    if diff > 0.2:
                        return False

            return True

        except Exception as e:
            logger.error(f"Error comparing contexts: {e}")
            return False

    def _add_to_recent(self, alert: Dict):
        """Add alert to recent alerts list."""
        try:
            self.recent_alerts.append(alert)

            # Keep only last hour of alerts
            cutoff = datetime.utcnow() - timedelta(hours=1)
            self.recent_alerts = [
                a for a in self.recent_alerts
                if a['timestamp'] >= cutoff.isoformat()
            ]

        except Exception as e:
            logger.error(f"Error adding to recent alerts: {e}")

    def clear_recent_alerts(self):
        """Clear recent alerts history (useful for testing)."""
        self.recent_alerts = []
        logger.info("Recent alerts cleared")
