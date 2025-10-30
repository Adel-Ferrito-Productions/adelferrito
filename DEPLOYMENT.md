# Deployment Guide - Malta Lightning Monitoring System

## Quick Start Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/Adel-Ferrito-Productions/adelferrito.git
cd adelferrito
git checkout claude/malta-lightning-automation-011CUe2ppkQ3RPFw1d5jpFew
```

### Step 2: Create .env File

Create a `.env` file in the project root with your API keys:

```bash
# Copy the example template
cp .env.example .env

# Or create it manually
```

**Edit `.env` and add your credentials:**

```env
# Windy API Key
WINDY_API_KEY=your_windy_api_key_here

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Email Configuration (optional)
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_TO=recipient@example.com

# Database Configuration (optional - defaults to SQLite)
DATABASE_URL=sqlite:///lightning_monitor/data/cache/weather_data.db

# System Flags
DEBUG_MODE=false
SILENT_MODE=false
```

### Step 3: Install Dependencies

**Option A: Minimal Installation (Recommended)**
```bash
pip install -r requirements-minimal.txt
```

**Option B: Full Installation (with all meteorological libraries)**
```bash
pip install -r requirements.txt
```

**Note:** If you encounter compilation errors with numpy/pandas on Python 3.13, use Option A (minimal) which works with pre-built wheels.

### Step 4: Verify Configuration

Check that `config/config.yaml` exists and is properly configured:

```bash
# Verify config file exists
ls config/config.yaml

# The config should already be set up for Malta monitoring
```

### Step 5: Test the Installation

```bash
# Test notifications (sends test message to Telegram)
python main.py --test
```

**Expected output:**
- ✅ System initializes successfully
- ✅ Test message sent to Telegram (if configured)
- ✅ No errors

### Step 6: Start Monitoring

```bash
# Run continuously
python main.py
```

**Expected behavior:**
- System starts and initializes all components
- Database created at `lightning_monitor/data/cache/weather_data.db`
- Logs written to `lightning_monitor/data/logs/monitor.log`
- Monitoring loop runs every 60 seconds (configurable)
- Checks for lightning strikes and weather conditions
- Sends alerts via Telegram when conditions are met

### Step 7: Run in Background (Linux/Mac)

**Using nohup:**
```bash
nohup python main.py > monitor.out 2>&1 &
```

**Using screen:**
```bash
screen -S lightning-monitor
python main.py
# Press Ctrl+A then D to detach
# Reattach with: screen -r lightning-monitor
```

**Using tmux:**
```bash
tmux new -s lightning-monitor
python main.py
# Press Ctrl+B then D to detach
# Reattach with: tmux attach -t lightning-monitor
```

## Windows Deployment

### Option 1: Run in PowerShell Background

```powershell
# Start in background
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden

# Or run in a separate PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python main.py"
```

### Option 2: Create Windows Service

Use NSSM (Non-Sucking Service Manager):
```powershell
# Download NSSM from https://nssm.cc/download
# Install service
nssm install LightningMonitor "C:\Python313\python.exe" "D:\path\to\adelferrito\main.py"
nssm set LightningMonitor AppDirectory "D:\path\to\adelferrito"
nssm start LightningMonitor
```

### Option 3: Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "When computer starts"
4. Action: Start a program
   - Program: `C:\Python313\python.exe`
   - Arguments: `main.py`
   - Start in: `D:\path\to\adelferrito`

## Docker Deployment

### Quick Start

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t malta-lightning-monitor .

# Run container
docker run -d \
  --name lightning-monitor \
  -v $(pwd)/lightning_monitor/data:/app/lightning_monitor/data \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  malta-lightning-monitor

# View logs
docker logs -f lightning-monitor
```

## Linux Systemd Service

### Install as System Service

```bash
# Copy service file
sudo cp deployment/malta-lightning-monitor.service /etc/systemd/system/

# Edit the service file to match your paths
sudo nano /etc/systemd/system/malta-lightning-monitor.service

# Update paths:
# ExecStart=/usr/bin/python3 /path/to/adelferrito/main.py
# WorkingDirectory=/path/to/adelferrito

# Reload systemd
sudo systemctl daemon-reload

# Enable service (starts on boot)
sudo systemctl enable malta-lightning-monitor

# Start service
sudo systemctl start malta-lightning-monitor

# Check status
sudo systemctl status malta-lightning-monitor

# View logs
sudo journalctl -u malta-lightning-monitor -f
```

## Verification Checklist

After deployment, verify:

- [ ] `.env` file created with correct API keys
- [ ] Dependencies installed (`pip list | grep apscheduler`)
- [ ] Test mode works (`python main.py --test`)
- [ ] Database created (`ls lightning_monitor/data/cache/weather_data.db`)
- [ ] Logs directory exists (`ls lightning_monitor/data/logs/`)
- [ ] Monitoring starts without errors
- [ ] Telegram notifications work (send test message)
- [ ] System runs continuously

## Monitoring & Logs

### View Logs

**Live log monitoring:**
```bash
# Linux/Mac
tail -f lightning_monitor/data/logs/monitor.log

# Windows PowerShell
Get-Content lightning_monitor\data\logs\monitor.log -Wait -Tail 50
```

### Check System Status

**Linux systemd:**
```bash
sudo systemctl status malta-lightning-monitor
```

**Docker:**
```bash
docker ps | grep lightning-monitor
docker logs lightning-monitor --tail 50
```

**Process check:**
```bash
# Linux/Mac
ps aux | grep "python main.py"

# Windows
Get-Process python | Where-Object {$_.Path -like "*adelferrito*"}
```

## Troubleshooting

### Issue: "Configuration file not found"
**Solution:** Ensure `config/config.yaml` exists in the project root

### Issue: "ModuleNotFoundError: No module named 'apscheduler'"
**Solution:** Install dependencies: `pip install -r requirements-minimal.txt`

### Issue: "no running event loop"
**Solution:** This should be fixed in the latest code. If it persists, ensure you're using the updated `main.py`

### Issue: Telegram notifications not working
**Solution:**
1. Verify bot token and chat ID in `.env`
2. Test with: `python main.py --test`
3. Check bot permissions with @BotFather

### Issue: Database locked errors
**Solution:** Ensure only one instance is running. Stop other instances before starting.

### Issue: API rate limits
**Solution:** Adjust fetch intervals in `config/config.yaml`:
```yaml
data_sources:
  windy:
    fetch_interval: 600  # Increase to 10 minutes
```

## Configuration Tuning

### Adjust Monitoring Frequency

Edit `config/config.yaml`:
```yaml
scheduler:
  monitoring_interval: 60  # seconds (default: 60)
```

### Change Alert Thresholds

```yaml
alerts:
  levels:
    watch:
      conditions:
        - "strikes_10min > 15"  # Adjust threshold
        - "cape > 1000"
```

### Set Notification Rate Limits

```yaml
alerts:
  notifications:
    rate_limit:
      max_per_hour: 10  # Maximum alerts per hour
      suppress_duplicates_minutes: 15  # Duplicate suppression window
```

## Performance Optimization

### For Low-Power Devices (Raspberry Pi)

```yaml
scheduler:
  monitoring_interval: 120  # Check every 2 minutes

location:
  monitoring_radius_km: 50  # Reduce area

storage:
  database:
    retention_days: 7  # Keep less history
```

### For Standard Servers

```yaml
scheduler:
  monitoring_interval: 60  # Check every minute

location:
  monitoring_radius_km: 100  # Full coverage

storage:
  database:
    retention_days: 30  # Keep full month
```

## Security Notes

- ✅ `.env` file is in `.gitignore` - never commit API keys
- ✅ Database files stored locally
- ✅ No external ports exposed (unless using web dashboard)
- ⚠️ Keep `.env` file permissions restricted: `chmod 600 .env` (Linux)

## Next Steps

1. **Monitor the logs** for the first few hours to ensure everything works
2. **Test notifications** by running `python main.py --test`
3. **Adjust thresholds** in `config/config.yaml` based on your needs
4. **Set up monitoring** to restart if the process crashes (systemd/supervisor)
5. **Review alerts** and fine-tune conditions based on real-world performance

## Support

- Check logs: `lightning_monitor/data/logs/monitor.log`
- Review configuration: `config/config.yaml`
- Test components: `python main.py --test`
- Check database: `sqlite3 lightning_monitor/data/cache/weather_data.db`

---

**Your system is now ready to monitor lightning activity around Malta! ⚡**

