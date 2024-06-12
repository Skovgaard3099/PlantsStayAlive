@echo off
cd C:\KYH\Programs\WeatherForecast
call .venv\Scripts\activate
python main.py > C:\KYH\Programs\WeatherForecast\run_log.txt 2>&1