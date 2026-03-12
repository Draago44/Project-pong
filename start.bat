@echo off
chcp 65001 >nul
title Pong Game

REM Переход в папку со скриптом
cd /d "%~dp0"

REM Проверка наличия Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python не найден! Установите Python и добавьте его в PATH.
    echo Нажмите любую клавишу для выхода...
    pause
    exit /b 1
)

REM Проверка наличия pygame
python -c "import pygame" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Pygame не установлен. Установка...
    python -m pip install pygame
)

REM Запуск игры (pythonw скрывает консоль)
pythonw "pong.py"

exit /b