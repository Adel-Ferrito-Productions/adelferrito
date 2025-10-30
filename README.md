# Malta Lightning Monitoring System ⚡

An automated real-time lightning monitoring and storm forecasting system specifically designed for Malta. Combines lightning strike detection, weather model analysis, and satellite data to provide timely alerts and forecast thunderstorm activity.

## Features

- **Real-time Lightning Detection**: Integrates with Blitzortung network for near real-time strike data
- **Weather Model Integration**: Fetches CAPE, Lifted Index, and other instability indices from Windy API
- **Satellite Data Analysis**: Optional EUMETSAT integration for cloud-top analysis
- **Storm Cell Tracking**: Identifies and tracks storm cells with motion prediction
- **Intelligent Alerting**: Configurable rules engine with multiple severity levels
- **Multi-channel Notifications**: Telegram bot and email alerts
- **Geographic Focus**: Optimized for Malta's central Mediterranean location
- **Data Persistence**: SQLite database for historical analysis
- **Automated Scheduling**: Continuous monitoring with configurable intervals
- **Docker Support**: Easy containerized deployment

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Data Ingestion Layer                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │  Blitzortung │ │   Windy API  │ │    EUMETSAT      │    │
│  │   Lightning  │ │   Weather    │ │    Satellite     │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                 Processing & Fusion Engine                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  GeoPandas Data Fusion | Storm Analysis | Tracking  │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Alert Rules Engine                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │   Configurable Thresholds | Severity Classification │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                  Notification Layer                         │
│  ┌────────────────────┐     ┌─────────────────────┐         │
│  │   Telegram Bot     │     │   Email (SMTP)      │         │
│  │   Push Alerts      │     │   Daily Summaries   │         │
│  └────────────────────┘     └─────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) Docker and Docker Compose

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd adelferrito
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

4. **Test the installation**
```bash
python main.py --test
```

5. **Start monitoring**
```bash
python main.py
```

## Configuration

### API Keys Required

1. **Windy API** (Essential)
   - Sign up at https://api.windy.com/keys
   - Free tier available
   - Provides CAPE, Lifted Index, and forecast data

2. **OpenWeatherMap** (Optional)
   - Free tier: https://openweathermap.org/api
   - Provides additional weather context

3. **Telegram Bot** (For notifications)
   - Create bot via @BotFather on Telegram
   - Get your chat ID by messaging @userinfobot

4. **EUMETSAT** (Optional, for satellite data)
   - Registration: https://eoportal.eumetsat.int/
   - Provides satellite imagery and cloud-top data

5. **Blitzortung** (Lightning data)
   - Public data available
   - Optional authentication for better access

### Configuration Files

#### `.env` - Credentials and Secrets
```bash
# API Keys
WINDY_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Email (for daily summaries)
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_TO=recipient@example.com
```

#### `config/config.yaml` - System Configuration
Key sections:
- **location**: Malta coordinates and monitoring radius
- **data_sources**: Enable/disable and configure data sources
- **processing**: Thresholds for lightning analysis and atmospheric instability
- **alerts**: Alert rules and notification settings
- **scheduler**: Monitoring intervals and timing

See `config/config.yaml` for full documentation of all options.

## Usage

### Running the Monitor

**Standard operation:**
```bash
python main.py
```

**With custom config:**
```bash
python main.py --config /path/to/config.yaml
```

**Test mode (send test notifications):**
```bash
python main.py --test
```

### Docker Deployment

**Build and start:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop:**
```bash
docker-compose down
```

### Systemd Service (Linux)

**Install service:**
```bash
sudo cp deployment/malta-lightning-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable malta-lightning-monitor
sudo systemctl start malta-lightning-monitor
```

**Check status:**
```bash
sudo systemctl status malta-lightning-monitor
```

## Alert Levels

The system generates alerts at four severity levels:

- **INFO** 🔵: Atmospheric conditions favorable for storms (CAPE > 500, LI < -1)
- **WATCH** 🟡: Storm development likely (CAPE > 1000, LI < -3, or 5+ strikes)
- **WARNING** 🟠: Active lightning nearby (15+ strikes in 10 min, within 30 km)
- **URGENT** 🔴: Intense lightning activity (30+ strikes, within 15 km)

## Data Sources

### Blitzortung Network
- Near real-time lightning strike detection
- Community-operated global network
- High accuracy for Europe/Mediterranean

### Windy API (ECMWF/GFS Models)
- CAPE (Convective Available Potential Energy)
- Lifted Index (atmospheric stability)
- Temperature, pressure, wind data
- 3-hour forecast resolution

### EUMETSAT (Optional)
- Meteosat satellite imagery
- Infrared and water vapor channels
- Cloud top heights
- Lightning Imager (MTG satellites)

## Database

SQLite database stores:
- **Lightning strikes**: Last 30 days (configurable)
- **Weather cache**: Recent forecasts
- **Alert history**: All triggered alerts

Location: `lightning_monitor/data/cache/weather_data.db`

## Logs

System logs are stored in:
- Main log: `lightning_monitor/data/logs/monitor.log`
- Alert log: `lightning_monitor/data/logs/alerts.log`

Log rotation is automatic (10 MB per file, 5 backups).

## Customization

### Adjusting Alert Thresholds

Edit `config/config.yaml`:
```yaml
processing:
  lightning:
    min_strikes_for_alert: 15  # Adjust sensitivity
    alert_radius_km: 30        # Alert distance

  atmospheric:
    cape_threshold: 1000       # J/kg
    lifted_index_threshold: -3
```

### Adding Custom Alert Rules

Alert rules use simple condition syntax:
```yaml
alerts:
  levels:
    custom_level:
      conditions:
        - "cape > 2000"
        - "strikes_10min > 20"
        - "strike_distance < 20"
```

### Notification Rate Limiting

```yaml
alerts:
  notifications:
    telegram:
      rate_limit:
        max_per_hour: 10
        suppress_duplicates_minutes: 15
```

## Troubleshooting

### No Lightning Data
- Check Blitzortung network status
- Verify internet connectivity
- Review logs for API errors

### Missing Weather Data
- Verify Windy API key in `.env`
- Check API quota/rate limits
- Test API key: `curl "https://api.windy.com/api/point-forecast/v2?key=YOUR_KEY"`

### Telegram Notifications Not Working
- Verify bot token and chat ID
- Test bot: `python main.py --test`
- Check bot has permission to send messages

### High Memory Usage
- Reduce `monitoring_radius_km` in config
- Decrease `retention_days` for database
- Lower `main_loop_interval` frequency

## Performance Considerations

### Recommended Settings

**Raspberry Pi / Low-power devices:**
```yaml
scheduler:
  main_loop_interval: 120  # 2 minutes
location:
  monitoring_radius_km: 50
storage:
  retention_days: 7
```

**Standard server:**
```yaml
scheduler:
  main_loop_interval: 60   # 1 minute
location:
  monitoring_radius_km: 100
storage:
  retention_days: 30
```

## Future Enhancements

Planned features:
- [ ] Web dashboard with live maps
- [ ] Machine learning storm prediction
- [ ] Local lightning sensor integration
- [ ] Mobile app notifications
- [ ] Historical storm analysis tools
- [ ] Photography recommendations engine
- [ ] Multi-location support

## Contributing

Contributions welcome! Areas of interest:
- Additional data sources
- Improved storm prediction algorithms
- Web dashboard development
- Documentation improvements
- Bug fixes and optimizations

## License

This project is created for educational and personal use. Please respect API terms of service for all integrated data sources.

## Acknowledgments

- **Blitzortung.org**: Lightning detection network
- **Windy/ECMWF**: Weather model data
- **EUMETSAT**: Satellite imagery
- **OpenWeatherMap**: Weather data

## Contact

For questions, issues, or contributions, please open an issue on the GitHub repository.

---

**Disclaimer**: This system is intended for informational purposes only. Always rely on official weather services for safety-critical decisions. Lightning is dangerous - stay safe and seek shelter during thunderstorms.
