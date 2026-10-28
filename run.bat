@echo off
title Fraud Detection System for Transactions
cd /d "%~dp0"

echo ============================================================
echo   Fraud Detection System for Transactions
echo   Starting Banking and AML Compliance Dashboard...
echo ============================================================
echo.
echo Opening browser at http://127.0.0.1:5000 ...
start "" http://127.0.0.1:5000
echo.
python app.py
pause
