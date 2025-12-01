# Weather CLI (OpenWeatherMap)

Simple command-line Python app that fetches current weather for a city using the OpenWeatherMap API.

## Files
- `Task6_(Weather_App).py` — main script

## Requirements
- Python 3.7+
- requests

## Setup (Windows)
1. Open PowerShell or VS Code integrated terminal.
2. Verify Python:
   ```powershell
   python --version
   ```
3. Install dependency:
   ```powershell
   python -m pip install --upgrade pip
   pip install requests
   ```

## Configure API key
The script currently reads the API key from the `API_KEY` variable inside `Task6_(Weather_App).py`. Replace the value of `API_KEY` with your OpenWeatherMap key.

Alternative (safer): set an environment variable and modify the script to read it (recommended for production).

Warning: Do not commit your API key to public repos.

## Run
```powershell
cd "d:\Devanshu_Pote\The_Developers_Arena_Internship\Task6_(Weather_App_With_API)"
python Task6_(Weather_App).py
```
Enter a city name when prompted (e.g., Mumbai).

## Example output
```
------------------------------
🌤  Weather in Mumbai, IN
------------------------------
Temperature : 29.5°C
Feels Like  : 31.0°C
Humidity    : 78%
Condition   : Light Rain
------------------------------
```

##
