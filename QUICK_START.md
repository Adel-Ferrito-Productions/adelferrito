# Quick Start - 5 Minute Setup

## 1. Install Dependencies

```bash
pip install -r requirements-minimal.txt
```

## 2. Create .env File

Create `.env` in the project root:

```env
WINDY_API_KEY=your_windy_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
DEBUG_MODE=false
SILENT_MODE=false
```

## 3. Test

```bash
python main.py --test
```

## 4. Run

```bash
python main.py
```

**Done!** The system is now monitoring lightning activity around Malta.

---

See `DEPLOYMENT.md` for detailed deployment options (Docker, systemd, etc.)

