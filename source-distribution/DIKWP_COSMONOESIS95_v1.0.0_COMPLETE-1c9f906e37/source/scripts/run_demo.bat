@echo off
python run.py doctor || exit /b 1
python run.py demo --out outputs\cosmonoesis_demo || exit /b 1
python run.py verify outputs\cosmonoesis_demo || exit /b 1
