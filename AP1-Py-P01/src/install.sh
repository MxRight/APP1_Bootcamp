#!/usr/bin/env bash
# ===============================================================
#  install.sh — автоматическая установка зависимостей проекта
# ===============================================================

set -e  # прерываем выполнение при любой ошибке

echo ""
echo "==============================="
echo "  Настройка окружения Python"
echo "==============================="
echo ""

if ! command -v python3 &>/dev/null; then
  echo "Python3 не найден. Установите Python3 и повторите попытку."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Создаём виртуальное окружение (.venv)..."
  python3 -m venv .venv
else
  echo "Окружение .venv уже существует."
fi

source .venv/bin/activate

echo "Обновляем pip..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
  echo "Устанавливаем зависимости..."
  pip install -r requirements.txt
else
  echo "Файл requirements.txt не найден, пропускаем установку зависимостей."
fi

echo ""
echo "Установка завершена! Окружение активировано."
echo "Чтобы активировать его позже вручную:"
echo ""
echo "   source .venv/bin/activate"
echo ""
echo "После активации проект можно запустить командой:"
echo "   python3 main.py"
echo ""
