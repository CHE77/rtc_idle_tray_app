#!/usr/bin/env python3

# Licensed under the Cooperative Non-Violent Public License (CNPL)
# See: https://github.com/CHE77/IoTManager-Modules/blob/main/LICENSE

import os
import sys
import subprocess
import importlib

def install_all_dependencies():
    print("🔍 Проверка зависимостей...")

    # APT-зависимости
    APT_PACKAGES = [
        "python3-pyqt5",
        "python3-opencv",
        "python3-tk",
        "python3-dev",
        "xprintidle",
        "util-linux",
        "gnome-screenshot",
        "x11-xkb-utils",
        "python3-pip"
    ]

    # pip-модули, которых нет в apt или нужны свежие версии
    REQUIRED_PIP_MODULES = {
        "pyautogui": "pyautogui",
        "telegram": "python-telegram-bot"
    }

    # === Шаг 1: установка APT-пакетов ===
    apt_to_install = []
    for pkg in APT_PACKAGES:
        result = subprocess.run(["dpkg-query", "-W", "-f=${Status}", pkg],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if "install ok installed" not in result.stdout:
            apt_to_install.append(pkg)

    if apt_to_install:
        print(f"🔧 Установка APT-пакетов: {' '.join(apt_to_install)}")
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', '--no-install-recommends'] + apt_to_install, check=True)
            print("✅ APT-зависимости установлены. Перезапускаем скрипт...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки APT-пакетов: {e}")
            sys.exit(1)

    # === Шаг 2: установка недостающих pip-модулей ===
    missing_pip = []
    for module, pip_name in REQUIRED_PIP_MODULES.items():
        try:
            importlib.import_module(module)
        except ImportError:
            print(f"📦 Модуль '{module}' не найден, будет установлен как '{pip_name}'")
            missing_pip.append(pip_name)

    if missing_pip:
        print(f"🔧 Установка pip-модулей: {' '.join(missing_pip)}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", *missing_pip], check=True)
            print("✅ pip-модули установлены. Перезапускаем скрипт...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки pip-модулей: {e}")
            sys.exit(1)

    print("✅ Все зависимости установлены и готовы к использованию.")

if __name__ == "__main__":
    install_all_dependencies()
