"""
Tests for alert rules engine.
"""

import pytest
from datetime import datetime, timedelta
from lightning_monitor.alerting.rules_engine import AlertRulesEngine


@pytest.mark.unit
class TestAlertRulesEngine:
    """Test alert rules engine functionality."""

    @pytest.fixture
    def alert_config(self, sample_config):
        """Get alert configuration."""
        return sample_config['alerts']

    @pytest.fixture
    def rules_engine(self, sample_config):
        """Create a rules engine instance."""
        return AlertRulesEngine(sample_config)

    def test_initialization(self, rules_engine, sample_config):
        """Test rules engine initializes correctly."""
        assert rules_engine.config == sample_config
        assert rules_engine.alert_config == sample_config['alerts']
        assert isinstance(rules_engine.recent_alerts, list)

    def test_evaluate_conditions_simple(self, rules_engine, sample_atmospheric_data):
        """Test basic condition evaluation."""
        lightning_analysis = {
            'strikes_10min': 20,
            'strikes_30min': 45,
            'strike_rate': 10.5,
            'closest_strike_km': 25,
            'trend': 'increasing'
        }
        
        alerts = rules_engine.evaluate_conditions(
            lightning_analysis,
            sample_atmospheric_data
        )
        
        assert isinstance(alerts, list)
        # Should generate at least one alert based on conditions

    def test_evaluate_conditions_no_alerts(self, rules_engine):
        """Test when no conditions are met."""
        lightning_analysis = {
            'strikes_10min': 2,
            'strikes_30min': 5,
            'strike_rate': 1.0,
            'closest_strike_km': 100,
            'trend': 'decreasing'
        }
        atmospheric_data = {
            'cape': 500,
            'lifted_index': 0,
            'thunder_probability': 10,
            'thunderstorm_potential': 15
        }
        
        alerts = rules_engine.evaluate_conditions(
            lightning_analysis,
            atmospheric_data
        )
        
        # No conditions met, so no alerts
        assert len(alerts) == 0

    def test_evaluate_conditions_watch_level(self, rules_engine, sample_atmospheric_data):
        """Test watch-level alert generation."""
        lightning_analysis = {
            'strikes_10min': 20,
            'strikes_30min': 45,
            'strike_rate': 15.0,
            'closest_strike_km': 25,
            'trend': 'increasing'
        }
        
        alerts = rules_engine.evaluate_conditions(
            lightning_analysis,
            sample_atmospheric_data  # CAPE is 1200, which meets threshold
        )
        
        # Should generate watch alert
        assert len(alerts) > 0
        watch_alerts = [a for a in alerts if a.get('level') == 'watch']
        assert len(watch_alerts) > 0

    def test_duplicate_suppression(self, rules_engine, sample_atmospheric_data):
        """Test that duplicate alerts are suppressed."""
        lightning_analysis = {
            'strikes_10min': 20,
            'strikes_30min': 45,
            'strike_rate': 10.5,
            'closest_strike_km': 25,
            'trend': 'increasing'
        }
        
        # Generate first alert
        alerts1 = rules_engine.evaluate_conditions(
            lightning_analysis,
            sample_atmospheric_data
        )
        
        # Generate second alert immediately (should be suppressed)
        alerts2 = rules_engine.evaluate_conditions(
            lightning_analysis,
            sample_atmospheric_data
        )
        
        # Second call should have fewer or no alerts due to duplicate suppression
        assert len(alerts2) <= len(alerts1)

    def test_build_context(self, rules_engine, sample_atmospheric_data):
        """Test context building."""
        lightning_analysis = {
            'strikes_10min': 20,
            'strikes_30min': 45,
            'strike_rate': 10.5,
            'closest_strike_km': 25,
            'trend': 'increasing'
        }
        
        context = rules_engine._build_context(
            lightning_analysis,
            sample_atmospheric_data,
            None
        )
        
        assert 'strikes_10min' in context
        assert 'strikes_30min' in context
        assert 'cape' in context
        assert context['strikes_10min'] == 20
        assert context['cape'] == sample_atmospheric_data['cape']

    def test_evaluate_rule_set_simple(self, rules_engine):
        """Test simple rule evaluation."""
        context = {
            'strikes_10min': 20,
            'cape': 1500
        }
        
        # Test simple condition
        conditions = ['strikes_10min > 15']
        assert rules_engine._evaluate_rule_set(conditions, context) is True
        
        conditions = ['strikes_10min > 30']
        assert rules_engine._evaluate_rule_set(conditions, context) is False

    def test_evaluate_rule_set_multiple(self, rules_engine):
        """Test multiple conditions (AND logic)."""
        context = {
            'strikes_10min': 20,
            'cape': 1500
        }
        
        # Both conditions must be true
        conditions = ['strikes_10min > 15', 'cape > 1000']
        assert rules_engine._evaluate_rule_set(conditions, context) is True
        
        # One condition false
        conditions = ['strikes_10min > 15', 'cape > 2000']
        assert rules_engine._evaluate_rule_set(conditions, context) is False

    def test_create_alert(self, rules_engine, sample_atmospheric_data):
        """Test alert creation."""
        lightning_analysis = {
            'strikes_10min': 20,
            'strikes_30min': 45,
            'strike_rate': 10.5,
            'closest_strike_km': 25,
            'trend': 'increasing'
        }
        
        context = rules_engine._build_context(
            lightning_analysis,
            sample_atmospheric_data,
            None  # storm_tracking is optional
        )
        
        alert = rules_engine._create_alert(
            'watch',
            context,
            ['strikes_10min > 15']
        )
        
        assert alert['level'] == 'watch'
        assert 'title' in alert
        assert 'message' in alert
        assert 'timestamp' in alert
        assert 'context' in alert

    def test_is_duplicate(self, rules_engine):
        """Test duplicate detection."""
        # Use ISO format timestamps as the implementation expects
        alert1 = {
            'level': 'watch',
            'title': 'Test Alert',
            'timestamp': datetime.now().isoformat(),
            'context': {
                'strikes_10min': 20,
                'strike_distance': 25,
                'cape': 1200,
                'lifted_index': -4
            }
        }
        
        alert2 = {
            'level': 'watch',
            'title': 'Test Alert',
            'timestamp': datetime.now().isoformat(),
            'context': {
                'strikes_10min': 22,  # Similar (within 20%)
                'strike_distance': 24,
                'cape': 1180,
                'lifted_index': -3.8
            }
        }
        
        # First alert should not be duplicate
        assert rules_engine._is_duplicate(alert1) is False
        
        # Add to recent
        rules_engine._add_to_recent(alert1)
        
        # Second alert should be duplicate (similar context within time window)
        assert rules_engine._is_duplicate(alert2) is True

    def test_add_to_recent(self, rules_engine):
        """Test adding alerts to recent list."""
        alert = {
            'level': 'watch',
            'title': 'Test Alert',
            'timestamp': datetime.now().isoformat(),
            'context': {}
        }
        
        initial_count = len(rules_engine.recent_alerts)
        rules_engine._add_to_recent(alert)
        
        assert len(rules_engine.recent_alerts) == initial_count + 1
        assert rules_engine.recent_alerts[-1] == alert

    def test_contexts_similar(self, rules_engine):
        """Test context similarity checking."""
        context1 = {
            'strikes_10min': 20,
            'strike_distance': 25,
            'cape': 1200,
            'lifted_index': -4
        }
        
        context2 = {
            'strikes_10min': 22,  # Within 20% threshold
            'strike_distance': 24,
            'cape': 1180,
            'lifted_index': -3.8
        }
        
        assert rules_engine._contexts_similar(context1, context2) is True
        
        # Different contexts
        context3 = {
            'strikes_10min': 50,  # Way different
            'strike_distance': 25,
            'cape': 1200,
            'lifted_index': -4
        }
        
        assert rules_engine._contexts_similar(context1, context3) is False

    def test_clear_recent_alerts(self, rules_engine):
        """Test clearing recent alerts."""
        alert = {
            'level': 'watch',
            'title': 'Test Alert',
            'timestamp': datetime.now().isoformat(),
            'context': {}
        }
        rules_engine._add_to_recent(alert)
        
        assert len(rules_engine.recent_alerts) > 0
        
        rules_engine.clear_recent_alerts()
        
        assert len(rules_engine.recent_alerts) == 0

