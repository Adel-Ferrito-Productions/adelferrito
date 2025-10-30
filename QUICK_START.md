# Quick Start - 5 Minute Setup

## 1. Install Dependencies

```bash
pip install -r requirements-minimal.txt
```

## 2. Create .env File

Create `.env` in the project root:

```env
WINDY_API_KEY=D7kCVowVLNdloXm0SOnru4MnCCygPVQZ
TELEGRAM_BOT_TOKEN=8372458796:AAEPl-mEKdPrjfbDiMppa3YqDjt8KZ2zX_k
TELEGRAM_CHAT_ID=7621379285
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

