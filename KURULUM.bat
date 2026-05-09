@echo off
title TencenT Launcher - Kurulum
color 0B
echo.
echo ========================================
echo   TencenT Launcher - Kurulum Baslat
echo ========================================
echo.
echo Python ile kurulum baslatiliyor...
echo.

python test_installer.py

if errorlevel 1 (
    echo.
    echo HATA: Python bulunamadi veya kurulum basarisiz!
    echo.
    echo Python yuklu mu kontrol edin:
    echo   python --version
    echo.
    echo Python indirmek icin:
    echo   https://www.python.org/downloads/
    echo.
    pause
)
