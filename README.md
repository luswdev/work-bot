# Work Bot

Fetch outlook clock in mail, send to telegram bot and show countdown in screen.

## Contribute

First, create a telegram bot (if not has one).

Filled config.yml (for example, see config.yml.example)

```powershell
python -m venv work_env
. .\workenv\Scripts\activate
pip install -r .\requirements.txt
```

### Local Testing
```powershell
. .\workenv\Scripts\activate
.\\main.py
```

### Pack Distribution
```powershell
. .\workenv\Scripts\activate
pyinstaller .\main.spec
```

## Dependencies
- python-telegram-bot
- PySide6
