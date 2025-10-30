"""
Email Notification Module

Sends daily summaries and alerts via email.
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Sends notifications via email."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        from_email: str,
        password: str,
        to_email: str,
        config: Dict
    ):
        """
        Initialize email notifier.

        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            from_email: Sender email address
            password: Email password (app-specific password for Gmail)
            to_email: Recipient email address
            config: Configuration dictionary
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.from_email = from_email
        self.password = password
        self.to_email = to_email
        self.config = config

        email_config = config.get('alerts', {}).get('notifications', {}).get('email', {})
        self.enabled = email_config.get('enabled', True)
        self.include_forecast = email_config.get('include_forecast', True)

        logger.info("Email notifier initialized")

    def send_daily_summary(self, summary: Dict) -> bool:
        """
        Send daily summary email.

        Args:
            summary: Summary dictionary with statistics and forecast

        Returns:
            True if sent successfully
        """
        try:
            if not self.enabled:
                logger.debug("Email notifications disabled")
                return False

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Malta Lightning Monitor - Daily Summary {summary.get('date', '')}"
            msg['From'] = self.from_email
            msg['To'] = self.to_email

            # Create plain text and HTML versions
            text_content = self._format_summary_text(summary)
            html_content = self._format_summary_html(summary)

            # Attach both versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.send_message(msg)

            logger.info("Daily summary email sent")
            return True

        except Exception as e:
            logger.error(f"Error sending daily summary email: {e}")
            return False

    def send_alert_email(self, alert: Dict) -> bool:
        """
        Send alert email for urgent notifications.

        Args:
            alert: Alert dictionary

        Returns:
            True if sent successfully
        """
        try:
            if not self.enabled:
                return False

            # Only send emails for warning and urgent levels
            if alert.get('level', '') not in ['warning', 'urgent']:
                return False

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"⚠️ {alert.get('title', 'Weather Alert')}"
            msg['From'] = self.from_email
            msg['To'] = self.to_email

            text_content = self._format_alert_text(alert)
            html_content = self._format_alert_html(alert)

            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.send_message(msg)

            logger.info(f"Alert email sent: {alert['level']}")
            return True

        except Exception as e:
            logger.error(f"Error sending alert email: {e}")
            return False

    def _format_summary_text(self, summary: Dict) -> str:
        """Format summary as plain text."""
        lines = [
            "Malta Lightning Monitor - Daily Summary",
            "=" * 50,
            f"Date: {summary.get('date', datetime.utcnow().strftime('%Y-%m-%d'))}",
            ""
        ]

        # Statistics
        if 'statistics' in summary:
            stats = summary['statistics']
            lines.extend([
                "Yesterday's Activity:",
                f"  • Total lightning strikes: {stats.get('total_strikes', 0)}",
                f"  • Active storm cells: {stats.get('storm_cells', 0)}",
                f"  • Closest strike: {stats.get('closest_strike_km', 'N/A')} km",
                ""
            ])

        # Forecast
        if 'forecast' in summary and self.include_forecast:
            forecast = summary['forecast']
            lines.extend([
                "Today's Forecast:",
                f"  • CAPE: {forecast.get('cape', 0):.0f} J/kg",
                f"  • Lifted Index: {forecast.get('lifted_index', 0):.1f}",
                f"  • Thunderstorm Risk: {forecast.get('risk_level', 'unknown').title()}",
                ""
            ])

        # Shooting windows
        if 'shooting_windows' in summary:
            windows = summary['shooting_windows']
            if windows:
                lines.append("Best Lightning Photography Windows:")
                for window in windows[:3]:
                    lines.append(
                        f"  • {window.get('time_range', 'TBD')}: "
                        f"{window.get('probability', 'unknown')} probability"
                    )
                lines.append("")

        # Recommendations
        if 'recommendations' in summary:
            lines.extend([
                "Recommendations:",
                f"  {summary['recommendations']}",
                ""
            ])

        lines.extend([
            "-" * 50,
            "Malta Lightning Monitor",
            "Automated weather monitoring system"
        ])

        return "\n".join(lines)

    def _format_summary_html(self, summary: Dict) -> str:
        """Format summary as HTML."""
        html = f"""
        <html>
          <head>
            <style>
              body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
              .header {{ background-color: #1e3a8a; color: white; padding: 20px; text-align: center; }}
              .content {{ padding: 20px; }}
              .section {{ margin-bottom: 25px; }}
              .section-title {{ color: #1e3a8a; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
              .stat-item {{ margin: 8px 0; padding-left: 20px; }}
              .footer {{ background-color: #f3f4f6; padding: 15px; text-align: center; color: #6b7280; font-size: 12px; }}
              .emoji {{ font-size: 20px; }}
            </style>
          </head>
          <body>
            <div class="header">
              <h1>⚡ Malta Lightning Monitor</h1>
              <p>Daily Summary - {summary.get('date', datetime.utcnow().strftime('%Y-%m-%d'))}</p>
            </div>

            <div class="content">
        """

        # Statistics
        if 'statistics' in summary:
            stats = summary['statistics']
            html += f"""
              <div class="section">
                <div class="section-title">📊 Yesterday's Activity</div>
                <div class="stat-item">⚡ Total strikes: <strong>{stats.get('total_strikes', 0)}</strong></div>
                <div class="stat-item">🌩️ Storm cells: <strong>{stats.get('storm_cells', 0)}</strong></div>
                <div class="stat-item">📍 Closest strike: <strong>{stats.get('closest_strike_km', 'N/A')} km</strong></div>
              </div>
            """

        # Forecast
        if 'forecast' in summary and self.include_forecast:
            forecast = summary['forecast']
            risk_colors = {
                'extreme': '#dc2626',
                'high': '#ea580c',
                'moderate': '#f59e0b',
                'low': '#84cc16',
                'minimal': '#22c55e'
            }
            risk_level = forecast.get('risk_level', 'unknown')
            risk_color = risk_colors.get(risk_level, '#6b7280')

            html += f"""
              <div class="section">
                <div class="section-title">🌡️ Today's Forecast</div>
                <div class="stat-item">CAPE: <strong>{forecast.get('cape', 0):.0f} J/kg</strong></div>
                <div class="stat-item">Lifted Index: <strong>{forecast.get('lifted_index', 0):.1f}</strong></div>
                <div class="stat-item">Thunderstorm Risk: <strong style="color: {risk_color};">{risk_level.title()}</strong></div>
              </div>
            """

        # Shooting windows
        if 'shooting_windows' in summary:
            windows = summary['shooting_windows']
            if windows:
                html += """
                  <div class="section">
                    <div class="section-title">📸 Best Lightning Photography Windows</div>
                """
                for window in windows[:3]:
                    html += f"""
                    <div class="stat-item">
                      {window.get('time_range', 'TBD')}:
                      <strong>{window.get('probability', 'unknown')}</strong> probability
                    </div>
                    """
                html += "</div>"

        # Recommendations
        if 'recommendations' in summary:
            html += f"""
              <div class="section">
                <div class="section-title">💡 Recommendations</div>
                <div class="stat-item">{summary['recommendations']}</div>
              </div>
            """

        html += """
            </div>

            <div class="footer">
              <p>Malta Lightning Monitor - Automated Weather Monitoring System</p>
              <p>This is an automated email. Please do not reply.</p>
            </div>
          </body>
        </html>
        """

        return html

    def _format_alert_text(self, alert: Dict) -> str:
        """Format alert as plain text."""
        lines = [
            f"⚠️ {alert.get('title', 'Weather Alert')}",
            "=" * 50,
            "",
            alert.get('message', ''),
            "",
            f"Alert Level: {alert.get('level', 'unknown').upper()}",
            f"Timestamp: {alert.get('timestamp', 'unknown')}",
            "",
            "-" * 50,
            "Malta Lightning Monitor"
        ]

        return "\n".join(lines)

    def _format_alert_html(self, alert: Dict) -> str:
        """Format alert as HTML."""
        level_colors = {
            'info': '#3b82f6',
            'watch': '#f59e0b',
            'warning': '#ea580c',
            'urgent': '#dc2626'
        }

        level = alert.get('level', 'info')
        color = level_colors.get(level, '#6b7280')

        # Convert newlines to <br> for HTML
        message = alert.get('message', '').replace('\n', '<br>')

        html = f"""
        <html>
          <head>
            <style>
              body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
              .header {{ background-color: {color}; color: white; padding: 20px; text-align: center; }}
              .content {{ padding: 20px; }}
              .message {{ background-color: #f9fafb; padding: 15px; border-left: 4px solid {color}; margin: 20px 0; }}
              .footer {{ background-color: #f3f4f6; padding: 15px; text-align: center; color: #6b7280; font-size: 12px; }}
              .level-badge {{ background-color: {color}; color: white; padding: 5px 15px; border-radius: 5px; display: inline-block; }}
            </style>
          </head>
          <body>
            <div class="header">
              <h1>⚠️ {alert.get('title', 'Weather Alert')}</h1>
            </div>

            <div class="content">
              <div class="message">
                {message}
              </div>

              <p><span class="level-badge">{level.upper()}</span></p>
              <p><strong>Timestamp:</strong> {alert.get('timestamp', 'unknown')}</p>
            </div>

            <div class="footer">
              <p>Malta Lightning Monitor - Automated Weather Monitoring System</p>
            </div>
          </body>
        </html>
        """

        return html
