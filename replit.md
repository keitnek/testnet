# Emu8086 Web Bot - Betting Game

A Vietnamese-language web-based betting game built with Python Flask.

## Overview

A simple Tai/Xiu (Odd/Even) betting game where users place bets and a random number determines the outcome.

## Tech Stack

- **Backend**: Python 3.12 + Flask
- **Frontend**: Vanilla HTML/CSS/JS (served via Flask templates)
- **Storage**: CSV files (local filesystem)
- **Production Server**: Gunicorn

## Project Structure

- `main.py` - Flask app with routes for game logic
- `generator.py` - Random number generator (01-99)
- `wallet.py` - Manages user balance via `account.csv`
- `storage.py` - Saves game history and rounds to CSV files
- `templates/index.html` - Game UI

## Data Files (auto-created)

- `account.csv` - Current wallet balance (default: 1,000,000 VND)
- `data_bot.csv` - Current round result
- `history.csv` - Full game history log

## Game Logic

- A random 2-digit number is generated (01-99)
- Sum of digits mod 10 = `d`
- Tai (Tài) = d is 0-4, Xiu (Xỉu) = d is 5-9
- Chan (Chẵn) = d is even, Le (Lẻ) = d is odd

## Running

```bash
python main.py
```

Runs on `0.0.0.0:5000`.

## Deployment

Configured as a VM deployment using Gunicorn:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
```

VM target is used because the app stores state in local CSV files.
