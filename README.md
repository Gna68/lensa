# Lensa

Lensa is a Python tool built with Playwright for interacting with WorldGuessr.

## Requirements

- Python 3.10+
- Git
- Playwright

## Installation

1. Clone this repository

```bash
git clone https://github.com/Gna68/lensa.git
```

2. Go to the project directory

```bash
cd lensa
```

3. Create a virtual environment (recommended)

### Linux / macOS

```bash
python3 -m venv venv
```

### Windows

```powershell
python -m venv venv
```

4. Activate the virtual environment

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Install Playwright Chromium

```bash
playwright install chromium
```

## Usage

Run the script:

```bash
python lensa.py
```

A Chromium browser will open automatically.

## License

MIT License
