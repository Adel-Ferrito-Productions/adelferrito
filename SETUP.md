# Malta Lightning Monitor - Setup Guide

## Step 1: Create .env File

Create a `.env` file in the project root with your API keys:

```env
WINDY_API_KEY=your_windy_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
DEBUG_MODE=false
SILENT_MODE=false
```

**Important:** Save the file (Cmd+S / Ctrl+S)

## Step 2: Install Python Dependencies

Open Terminal in Cursor:
- **Menu:** Terminal → New Terminal (or press `Ctrl+``)

Install dependencies:

```bash
pip install -r requirements-minimal.txt
```

*(This will take 1-2 minutes)*

## Step 3: Test the System

In the Cursor terminal, run:

```bash
python main.py --test
```

**You should see:**
- ✅ System initializes successfully
- ✅ Test message appears in your Telegram (from @MaltalightingBot)

## Step 4: Start Monitoring!

```bash
python main.py
```

**The system will:**
- ⚡ Monitor lightning strikes around Malta every 60 seconds
- 🌡️ Check weather conditions (CAPE, Lifted Index)
- 📱 Send Telegram alerts when storms are detected
- 📊 Store data in local database
- ✉️ Send daily summary at 8 AM (if you configure email)

## Running in Background

### Windows (PowerShell)
```powershell
# Run in background window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python main.py"
```

### Linux/Mac
```bash
# Using screen
screen -S lightning-monitor
python main.py
# Press Ctrl+A then D to detach

# Using nohup
nohup python main.py > monitor.out 2>&1 &
```

## Monitor Logs

View real-time logs:

```bash
# Windows PowerShell
Get-Content lightning_monitor\data\logs\monitor.log -Wait -Tail 50

# Linux/Mac
tail -f lightning_monitor/data/logs/monitor.log
```

## Stop the System

Press `Ctrl+C` in the terminal where it's running.

---

**That's it! Your lightning monitoring system is now running! ⚡**

