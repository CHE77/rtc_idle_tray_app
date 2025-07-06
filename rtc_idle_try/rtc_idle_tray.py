#!/usr/bin/env python3

# Licensed under the Cooperative Non-Violent Public License (CNPL)
# See: https://github.com/CHE77/IoTManager-Modules/blob/main/LICENSE
import os
import sys
import subprocess
import shutil
import importlib

APP_NAME = "rtc_idle_tray"


def ensure_pip_installed():
    # Проверка наличия pip
    try:
        import pip
    except ImportError:
        print("❌ pip не найден.")
        answer = input("Хотите установить pip через apt? [Y/n] ").strip().lower()
        if answer in ("", "y", "yes"):
            try:
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(
                    ["sudo", "apt", "install", "-y", "python3-pip"], check=True
                )
                print("✅ pip успешно установлен.")
            except Exception as e:
                print(f"❌ Не удалось установить pip через apt: {e}")
                sys.exit(1)
        else:
            print("⛔ Без pip невозможно продолжить.")
            sys.exit(1)

    REQUIRED_PYTHON_MODULES = {
        "PyQt5": "PyQt5",
        "cv2": "opencv-python-headless",
        "telegram": "python-telegram-bot",
        "pyautogui": "pyautogui",
    }

    missing_pip = []
    for module_name, pip_name in REQUIRED_PYTHON_MODULES.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(
                f"📦 Модуль '{module_name}' не найден, будет установлен как '{pip_name}'"
            )
            missing_pip.append(pip_name)

    if missing_pip:
        print(f"🔧 Установка Python-пакетов: {' '.join(missing_pip)}")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--break-system-packages",
                    *missing_pip,
                ],
                check=True,
            )
            print("✅ Python-пакеты установлены. Перезапускаем скрипт...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки: {e}")
            sys.exit(1)


# ensure_pip_installed()


# === ШАГ 2. Устанавливаем недостающие модули ===
def install_missing_modules():
    REQUIRED_PYTHON_MODULES = {
        "PyQt5": "PyQt5",
        "cv2": "opencv-python-headless",
        "telegram": "python-telegram-bot",
        "pyautogui": "pyautogui",
    }

    REQUIRED_BINARIES = {
        "rtcwake": "util-linux",
        "xprintidle": "xprintidle",
        "gnome-screenshot": "gnome-screenshot",
        "setxkbmap": "x11-xkb-utils",
    }

    missing_pip = []
    for module_name, pip_name in REQUIRED_PYTHON_MODULES.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(
                f"📦 Модуль '{module_name}' не найден, будет установлен как '{pip_name}'"
            )
            missing_pip.append(pip_name)

    apt_packages = []
    for bin, pkg in REQUIRED_BINARIES.items():
        if shutil.which(bin) is None:
            apt_packages.append(pkg)

    try:
        import tkinter
    except ImportError:
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        apt_packages += [f"python{py_version}-tk", "python3-dev"]

    if apt_packages:
        print(f"🔧 Установка APT-пакетов: {' '.join(apt_packages)}")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(
                ["sudo", "apt", "install", "-y", "--no-install-recommends"]
                + apt_packages,
                check=True,
            )
            print("✅ Системные пакеты установлены")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки APT: {e}")
            sys.exit(1)

    if missing_pip:
        print(f"🔧 Установка Python-пакетов: {' '.join(missing_pip)}")
        try:

            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True
            )
            # subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', *missing_pip], check=True)
            subprocess.run(
                [sys.executable, "-m", "pip", "install", *missing_pip], check=True
            )
            print("✅ Python-пакеты установлены. Перезапускаем скрипт...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки pip-пакетов: {e}")
            sys.exit(1)

    print("✅ Все зависимости удовлетворены")


# install_missing_modules()


# Импорты после установки
from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
import pyautogui
from telegram import Bot

#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
import getpass
from datetime import datetime, timezone, timedelta
import shutil

import json
import uuid

import asyncio


APP_NAME = "rtc_idle_tray"
global next_wakeup_dt
next_wakeup_dt = None
debug = False


# === Настройки времени пробуждения ===
# WAKE_HOUR = 10     # Часы LT
# WAKE_MINUTE = 20  # Минуты LT
# WAKE_OFFSET_DAYS = 0  # Через сколько дней сработает (0 — сегодня, 1 — завтра и т.д.)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WAKE_FLAG_PATH = os.path.join(SCRIPT_DIR, ".wake_set")

DEFAULT_WAKE_DATA = {
    "enabled": False,  # Автозапуск включён
    "time": "07:00",  # Время пробуждения
    "auto_shutdown": False,  # Перезагрузка при простое
    "idle_timeout": 120,  # Время бездействия в секундах
    "terminal": True,
    "telegram_enabled": True,
    "telegram_token": "",
    "telegram_chat_id": "",
}
# 499079294

import importlib


def install_missing_modules1():
    """Установка недостающих зависимостей (оптимизированная версия)"""
    # 1. Проверка Python-модулей
    REQUIRED_PYTHON_MODULES = {
        "PyQt5": "PyQt5",
        "cv2": "opencv-python-headless",  # Более лёгкая версия OpenCV
        "telegram": "python-telegram-bot",
        "pyautogui": "pyautogui",  # Обычно работает без python3-xlib
    }

    missing_pip = []
    for module_name, pip_name in REQUIRED_PYTHON_MODULES.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(
                f"📦 Модуль '{module_name}' не найден, будет установлен как '{pip_name}'"
            )
            missing_pip.append(pip_name)

    # 2. Проверка системных утилит
    REQUIRED_BINARIES = {
        "rtcwake": "util-linux",
        "xprintidle": "xprintidle",
        "gnome-screenshot": "gnome-screenshot",
        "setxkbmap": "x11-xkb-utils",
    }

    apt_packages = []
    for bin, pkg in REQUIRED_BINARIES.items():
        if shutil.which(bin) is None:
            apt_packages.append(pkg)

    # 3. Проверка tkinter (особый случай)
    try:
        import tkinter
    except ImportError:
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        apt_packages.extend([f"python{py_version}-tk", "python3-dev"])

    # 4. Установка системных пакетов
    if apt_packages:
        print(f"🔧 Установка APT-пакетов: {' '.join(apt_packages)}")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(
                ["sudo", "apt", "install", "-y", "--no-install-recommends"]
                + apt_packages,
                check=True,
            )
            print("✅ Системные пакеты установлены")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки: {e}")
            return False

    # 5. Установка Python-пакетов
    if missing_pip:
        print(f"🔧 Установка Python-пакетов: {' '.join(missing_pip)}")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True
            )
            subprocess.run(
                [sys.executable, "-m", "pip", "install", *missing_pip], check=True
            )
            print("✅ Python-пакеты установлены. Перезапустите скрипт.")
            return True  # Требует перезапуска
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки: {e}")
            return False

    print("✅ Все зависимости удовлетворены")
    return True


def load_wake_data():
    """Загружает данные из файла или создаёт с данными по умолчанию"""
    if not os.path.exists(WAKE_FLAG_PATH):
        print(f"[wake_config] Файл {WAKE_FLAG_PATH} не найден. Создаю по умолчанию.")
        save_wake_data(DEFAULT_WAKE_DATA)
        return DEFAULT_WAKE_DATA.copy()
    try:
        with open(WAKE_FLAG_PATH, "r") as f:
            data = json.load(f)
            if debug:
                print(f"[wake_config] Загружены данные из файла: {data}")
            return {**DEFAULT_WAKE_DATA, **data}
    except Exception as e:
        print(f"[wake_config] Ошибка чтения файла: {e}. Переинициализация.")
        save_wake_data(DEFAULT_WAKE_DATA)
        return DEFAULT_WAKE_DATA.copy()


def save_wake_data(data):
    """Сохраняет данные в файл"""
    try:
        with open(WAKE_FLAG_PATH, "w") as f:
            json.dump(data, f, indent=2)
        if debug:
            print(f"[wake_config] Сохранены данные: {data}")
    except Exception as e:
        print(f"[wake_config] Ошибка записи в файл: {e}")


def set_wake_enabled(enabled: bool):
    data = load_wake_data()
    data["enabled"] = enabled
    save_wake_data(data)
    print(f"[wake_config] Автозапуск установлен в: {enabled}")


def set_wake_time(time_str: str):
    data = load_wake_data()
    data["time"] = time_str.strip()
    save_wake_data(data)
    print(f"[wake_config] Время автозапуска установлено в: {time_str}")


def set_auto_shutdown(enabled: bool):
    data = load_wake_data()
    data["auto_shutdown"] = enabled
    save_wake_data(data)
    print(f"[wake_config] Автоотключение по простою: {enabled}")


def set_telegram_enabled(enabled: bool):
    data = load_wake_data()
    data["telegram_enabled"] = enabled
    save_wake_data(data)
    print(f"[wake_config] Телеграм установлен в: {enabled}")
    ensure_telegram_config()


def set_terminal_enabled(enabled: bool):
    data = load_wake_data()
    data["terminal"] = enabled
    save_wake_data(data)
    print(f"[wake_config] Терминал установлен в: {enabled}")


def set_idle_timeout(seconds: int):
    data = load_wake_data()
    data["idle_timeout"] = int(seconds)
    save_wake_data(data)
    print(f"[wake_config] Таймаут бездействия: {seconds} секунд")


def get_wake_time():
    return load_wake_data()["time"]


def get_idle_timeout():
    return load_wake_data()["idle_timeout"]


def is_wake_enabled():
    return load_wake_data()["enabled"]


def is_auto_shutdown_enabled():
    return load_wake_data()["auto_shutdown"]


def is_terminal_enabled():
    return load_wake_data()["terminal"]


def is_telegram_enabled():
    return load_wake_data().get("telegram_enabled", False)


def get_telegram_token():
    return load_wake_data().get("telegram_token", "")


def get_telegram_chat_id():
    return load_wake_data().get("telegram_chat_id", "")


def ensure_telegram_config():
    """Запрашивает у пользователя token и chat_id, если включена отправка, но данных нет"""
    data = load_wake_data()

    if not data.get("telegram_enabled"):
        return

    updated = False
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    if not data.get("telegram_token"):
        token, ok = QtWidgets.QInputDialog.getText(
            None, "Telegram Token", "Введите Telegram Bot Token:"
        )
        if ok and token.strip():
            data["telegram_token"] = token.strip()
            updated = True
        else:
            print("❌ Token не введён. Отключаем Telegram.")
            data["telegram_enabled"] = False
            save_wake_data(data)
            return

    if not data.get("telegram_chat_id"):
        chat_id, ok = QtWidgets.QInputDialog.getText(
            None, "Telegram Chat ID", "Введите Telegram Chat ID:"
        )
        if ok and chat_id.strip():
            data["telegram_chat_id"] = chat_id.strip()
            updated = True
        else:
            print("❌ Chat ID не введён. Отключаем Telegram.")
            data["telegram_enabled"] = False
            save_wake_data(data)
            return

    if updated:
        save_wake_data(data)
        print("✅ Данные Telegram сохранены.")


import uuid

from datetime import datetime

import uuid
import os
import subprocess
import asyncio
from datetime import datetime

def _telegram_params():
    """
    Возвращает (token, chat_id, snapshots_dir) или None,
    если Telegram отключён или не сконфигурирован.
    """
    data = load_wake_data()
    if not data.get("telegram_enabled"):
        return None

    token, chat_id = data.get("telegram_token"), data.get("telegram_chat_id")
    if not token or not chat_id:
        print("❌ Не указаны token или chat_id")
        return None

    snapshots_dir = os.path.join(SCRIPT_DIR, "snapshots")
    os.makedirs(snapshots_dir, exist_ok=True)
    return token, chat_id, snapshots_dir


async def _send_photo(token: str, chat_id: str, file_path: str, caption: str = ""):
    """Асинхронно отправляет фото в Telegram (если файл существует)."""
    if not os.path.exists(file_path):
        return

    try:
        bot = Bot(token=token)
        with open(file_path, "rb") as f:
            await bot.send_photo(chat_id=chat_id, photo=f, caption=caption)
        print(f"✅ Отправлено в Telegram: {file_path}")
    except TimedOut:
        print("⏱️ Время ожидания при отправке в Telegram истекло.")
    except TelegramError as e:
        print(f"❌ Ошибка Telegram API: {e}")
    except Exception as e:
        print(f"❌ Неизвестная ошибка при отправке в Telegram: {e}")


def capture_camera_and_send(caption: str = ""):
    """
    Делает снимок с первой доступной камеры и отправляет его в Telegram.
    """
    try:
        params = _telegram_params()
        if params is None:
            return
        token, chat_id, snapshots_dir = params

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        cam_path = os.path.join(snapshots_dir, f"camera_{ts}.jpg")

        # 📸 Снимок с камеры
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                cv2.imwrite(cam_path, frame)
                print(f"📸 Снимок с камеры сохранён: {cam_path}")
            else:
                print("❌ Не удалось сделать снимок с камеры")
                return
        except Exception as e:
            print(f"❌ Ошибка камеры: {e}")
            return

        # 📤 Отправка
        asyncio.run(_send_photo(token, chat_id, cam_path, caption))

    except Exception as e:
        print(f"❌ Ошибка capture_camera_and_send: {e}")

def capture_screen_and_send(caption: str = ""):
    """
    Делает скриншот текущего экрана при помощи gnome-screenshot
    и отправляет его в Telegram.
    """
    try:
        params = _telegram_params()
        if params is None:
            return
        token, chat_id, snapshots_dir = params

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screen_path = os.path.join(snapshots_dir, f"screen_{ts}.png")

        # 🖥 Скриншот через gnome-screenshot
        try:
            subprocess.run(["gnome-screenshot", "-f", screen_path], check=True)
            print(f"🖥 Скриншот сохранён: {screen_path}")
        except Exception as e:
            print(f"❌ Ошибка при создании скриншота: {e}")
            return

        # 📤 Отправка
        asyncio.run(_send_photo(token, chat_id, screen_path, caption))

    except Exception as e:
        print(f"❌ Ошибка capture_screen_and_send: {e}")



def show_startup_notification():
    try:
        # Получаем имя скрипта
        script_name = os.path.basename(sys.argv[0])
        app_name = os.path.splitext(script_name)[0]

        subprocess.Popen(
            [
                "notify-send",
                "--icon=system-run",
                "--app-name",
                app_name,
                "Автозапуск",
                f"{app_name} запущен в фоновом режиме",
            ]
        )
    except Exception as e:
        print(f"Не удалось показать уведомление: {e}")


def detect_display_manager():
    try:
        # Попробуем узнать через systemctl
        result = subprocess.run(
            ["systemctl", "show", "display-manager.service", "--property=ExecStart"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        line = result.stdout.strip()
        if "gdm" in line.lower():
            return "gdm"
        elif "lightdm" in line.lower():
            return "lightdm"
        elif "sddm" in line.lower():
            return "sddm"
    except Exception as e:
        print(f"⚠️ Не удалось определить дисплей-менеджер: {e}")
    return "unknown"


def ensure_autostart():
    if debug:
        print("✅ ensure_autostart() run")

    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)

    script_path = os.path.realpath(sys.argv[0])
    script_name = os.path.basename(script_path)
    app_name = os.path.splitext(script_name)[0]
    desktop_path = os.path.join(autostart_dir, f"{app_name}.desktop")

    # Определяем дисплей-менеджер
    dm = detect_display_manager().lower()
    print(f"🖥️ Дисплей-менеджер: {dm}")

    # Подбираем Exec-команду в зависимости от terminal-настройки и DM
    if is_terminal_enabled():
        if dm.startswith("gdm"):
            dm = "gdm"

        print(f"[DEBUG] detect_display_manager() вернул: {dm!r}")

        if dm == "gdm":
            #exec_cmd = f'gnome-terminal -- bash -c "{script_path}; exec bash"'
            exec_cmd = f'gnome-terminal --window --maximize -- bash -c "{script_path}; exec bash"'
        elif dm == "lightdm":
            #exec_cmd = f'xfce4-terminal --hold --command="{script_path}"'
            exec_cmd = f'xfce4-terminal --maximize --hold --command="{script_path}"'
        else:
            exec_cmd = f'xterm -hold -e "{script_path}"'
    else:
        exec_cmd = f"{sys.executable} {script_path}"

    # Содержимое .desktop-файла
    desktop_content = f"""[Desktop Entry]
Type=Application
Exec={exec_cmd}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name={app_name}
Comment=Autозапуск для {app_name}
"""

    # Проверка: пересоздаём, если файл не существует или отличается по Exec
    recreate = True
    if os.path.exists(desktop_path):
        with open(desktop_path, "r") as f:
            existing = f.read()
        if existing.strip() == desktop_content.strip():
            print(f"✅ Автозапуск УЖЕ настроен корректно: {desktop_path}")
            recreate = False
        else:
            print(f"🔁 Обновляется .desktop-файл: {desktop_path}")

    if recreate:
        with open(desktop_path, "w") as f:
            f.write(desktop_content)
        print(f"✅ Файл автозапуска создан/обновлён: {desktop_path}")


def ensure_rtc_access():
    print("⚙️ Проверка доступа к /dev/rtc0...")
    if not os.path.exists("/dev/rtc0"):
        print("❌ /dev/rtc0 не найден")
        sys.exit(1)

    st = os.stat("/dev/rtc0")
    if not (st.st_mode & 0o660):
        print("⚠️ Недостаточно прав для /dev/rtc0, пытаемся исправить...")
        # Добавляем группу rtc, создаём правило udev и добавляем пользователя в группу rtc
        # Группа rtc может отсутствовать - создаём её если нужно
        try:
            subprocess.run(["sudo", "groupadd", "-f", "rtc"], check=True)
            # Правило udev
            udev_rule = 'KERNEL=="rtc0", GROUP="rtc", MODE="0660"\n'
            udev_path = "/etc/udev/rules.d/99-rtc0.rules"
            with open("rtc0.rules.tmp", "w") as f:
                f.write(udev_rule)
            subprocess.run(["sudo", "mv", "rtc0.rules.tmp", udev_path], check=True)
            subprocess.run(["sudo", "udevadm", "control", "--reload-rules"], check=True)
            subprocess.run(["sudo", "udevadm", "trigger", "/dev/rtc0"], check=True)
            # Добавляем пользователя в группу rtc, если нет
            user = getpass.getuser()
            groups = subprocess.check_output(["groups", user]).decode()
            if "rtc" not in groups:
                print(f"👥 Добавляем пользователя {user} в группу rtc...")
                subprocess.run(["sudo", "usermod", "-aG", "rtc", user], check=True)
                print("⚠️ Перезайдите в сессию, чтобы изменения групп применились")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при попытке настроить доступ к /dev/rtc0: {e}")
            sys.exit(1)


def add_cap_sys_time():
    path = "/usr/sbin/rtcwake"
    print("⏱ Проверка наличия cap_sys_time для rtcwake...")

    # Получаем реальный путь, если это симлинк
    try:
        real_path = os.path.realpath(path)
    except Exception as e:
        print(f"⚠️ Ошибка определения реального пути: {e}")
        return

    try:
        result = subprocess.run(
            ["getcap", real_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = result.stdout.strip()
        if "cap_sys_time" in output:
            print(f"✅ cap_sys_time уже установлен для {real_path}: {output}")
            return

        print(f"➕ Добавляется cap_sys_time для {real_path}...")
        subprocess.run(["sudo", "setcap", "cap_sys_time+ep", real_path], check=True)
        print("✅ cap_sys_time успешно добавлен.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки cap_sys_time: {e}")
    except Exception as e:
        print(f"⚠️ Ошибка при проверке cap_sys_time: {e}")


def detect_display_manager():
    try:
        out = subprocess.check_output(
            [
                "loginctl",
                "show-session",
                os.environ.get("XDG_SESSION_ID", ""),
                "-p",
                "Type",
            ],
            text=True,
        )
        # Иногда XDG_SESSION_ID не задан — fallback
    except Exception:
        out = ""
    # Попытка через systemctl
    try:
        out2 = subprocess.check_output(
            ["systemctl", "status", "display-manager"], text=True
        )
        if "lightdm" in out2:
            return "lightdm"
        if "gdm3" in out2:
            return "gdm3"
    except Exception:
        pass
    # fallback по процессам
    procs = subprocess.check_output(["ps", "axo", "comm"], text=True).splitlines()
    if "lightdm" in procs:
        return "lightdm"
    if "gdm3" in procs or "gdm" in procs:
        return "gdm3"
    return "unknown"


def ensure_gdm_autologin_enabled():
    conf_path = "/etc/gdm3/custom.conf"
    user = os.getenv("USER")
    changed = False

    print(f"🖥️ Проверка GDM конфигурации в {conf_path}...")

    # Читаем оригинальный файл
    with open(conf_path, "r") as f:
        lines = f.readlines()

    in_daemon = False
    found_autologin_enable = False
    found_autologin = False
    found_wayland = False

    new_lines = []
    for line in lines:
        stripped = line.strip()

        if stripped.startswith("[") and "daemon" in stripped.lower():
            in_daemon = True
            new_lines.append(line)
            continue
        elif stripped.startswith("[") and not "daemon" in stripped.lower():
            in_daemon = False

        if in_daemon:
            if stripped.startswith("AutomaticLoginEnable"):
                found_autologin_enable = True
                if stripped.lower() != "automaticloginenable=true":
                    print("🔁 Заменяется AutomaticLoginEnable → true")
                    new_lines.append("AutomaticLoginEnable=true\n")
                    changed = True
                else:
                    print("✅ AutomaticLoginEnable уже установлен в true")
                    new_lines.append(line)
                continue

            elif stripped.startswith("AutomaticLogin"):
                found_autologin = True
                if stripped != f"AutomaticLogin={user}":
                    print(f"🔁 Заменяется AutomaticLogin → {user}")
                    new_lines.append(f"AutomaticLogin={user}\n")
                    changed = True
                else:
                    print("✅ AutomaticLogin уже установлен верно")
                    new_lines.append(line)
                continue

            elif stripped.startswith("WaylandEnable"):
                found_wayland = True
                if stripped.lower() != "waylandenable=false":
                    print("🔁 Заменяется WaylandEnable → false")
                    new_lines.append("WaylandEnable=false\n")
                    changed = True
                else:
                    print("✅ WaylandEnable уже установлен в false (X11 включён)")
                    new_lines.append(line)
                continue

        new_lines.append(line)

    # Добавление недостающих параметров в секцию [daemon]
    if not found_autologin_enable or not found_autologin or not found_wayland:
        print("➕ Добавление недостающих параметров в секцию [daemon]...")
        updated_lines = []
        inserted = False
        for line in new_lines:
            updated_lines.append(line)
            if line.strip().startswith("[daemon]") and not inserted:
                if not found_autologin_enable:
                    print("➕ Добавляется AutomaticLoginEnable=true")
                    updated_lines.append("AutomaticLoginEnable=true\n")
                if not found_autologin:
                    print(f"➕ Добавляется AutomaticLogin={user}")
                    updated_lines.append(f"AutomaticLogin={user}\n")
                if not found_wayland:
                    print("➕ Добавляется WaylandEnable=false")
                    updated_lines.append("WaylandEnable=false\n")
                inserted = True
        new_lines = updated_lines
        changed = True

    if changed:
        print("💾 Сохраняются изменения конфигурации GDM...")
        backup_path = conf_path + ".bak"
        print(f"📂 Создаётся резервная копия: {backup_path}")
        subprocess.run(["sudo", "cp", conf_path, backup_path])
        with open("/tmp/custom.conf.new", "w") as f:
            f.writelines(new_lines)
        subprocess.run(["sudo", "cp", "/tmp/custom.conf.new", conf_path])
        print("✅ GDM конфигурация обновлена.")
    else:
        print("✅ Автологин и X11 уже правильно настроены для GDM.")


def ensure_lightdm_autologin_enabled():
    conf_dir = "/etc/lightdm/lightdm.conf.d"
    conf_file = "50-autologin.conf"
    conf_path = os.path.join(conf_dir, conf_file)
    user = os.getenv("USER")
    changed = False

    print(f"🖥️ Проверка конфигурации LightDM в {conf_path}...")

    if not os.path.exists(conf_path):
        print("⚠️ Файл конфигурации не найден. Создаётся новый файл автологина...")
        lines = ["[Seat:*]\n", f"autologin-user={user}\n", "autologin-user-timeout=0\n"]
        with open("/tmp/autologin_lightdm.conf", "w") as f:
            f.writelines(lines)
        subprocess.run(["sudo", "cp", "/tmp/autologin_lightdm.conf", conf_path])
        print("✅ Файл автологина создан для LightDM.")
        return

    # Чтение текущего файла
    with open(conf_path, "r") as f:
        lines = f.readlines()

    in_seat = False
    found_autologin_user = False
    found_autologin_timeout = False
    new_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("[") and "seat" in stripped.lower():
            in_seat = True
            new_lines.append(line)
            continue
        elif stripped.startswith("["):
            in_seat = False
            new_lines.append(line)
            continue

        if in_seat:
            if stripped.startswith("autologin-user="):
                found_autologin_user = True
                if stripped != f"autologin-user={user}":
                    print(f"🔁 Заменяется autologin-user → {user}")
                    new_lines.append(f"autologin-user={user}\n")
                    changed = True
                else:
                    print("✅ autologin-user уже установлен верно")
                    new_lines.append(line)
                continue
            elif stripped.startswith("autologin-user-timeout="):
                found_autologin_timeout = True
                if stripped != "autologin-user-timeout=0":
                    print("🔁 Заменяется autologin-user-timeout → 0")
                    new_lines.append("autologin-user-timeout=0\n")
                    changed = True
                else:
                    print("✅ autologin-user-timeout уже установлен в 0")
                    new_lines.append(line)
                continue

        new_lines.append(line)

    # Добавление недостающих параметров
    if not found_autologin_user or not found_autologin_timeout:
        print("➕ Добавление недостающих параметров в секцию [Seat:*]...")
        updated_lines = []
        inserted = False
        for line in new_lines:
            updated_lines.append(line)
            if line.strip().startswith("[Seat:") and not inserted:
                if not found_autologin_user:
                    print(f"➕ Добавляется autologin-user={user}")
                    updated_lines.append(f"autologin-user={user}\n")
                if not found_autologin_timeout:
                    print("➕ Добавляется autologin-user-timeout=0")
                    updated_lines.append("autologin-user-timeout=0\n")
                inserted = True
        new_lines = updated_lines
        changed = True

    if changed:
        print("💾 Сохраняются изменения конфигурации LightDM...")
        backup_path = conf_path + ".bak"
        print(f"📂 Создаётся резервная копия: {backup_path}")
        subprocess.run(["sudo", "cp", conf_path, backup_path])
        with open("/tmp/50-autologin.conf.new", "w") as f:
            f.writelines(new_lines)
        subprocess.run(["sudo", "cp", "/tmp/50-autologin.conf.new", conf_path])
        print("✅ LightDM конфигурация обновлена.")
    else:
        print("✅ Автологин уже правильно настроен в LightDM.")


import shutil


def check_xprintidle():
    if shutil.which("xprintidle") is None:
        print(
            "❌ Требуется пакет xprintidle. Установите через: sudo apt install xprintidle"
        )
        return False
    return True


def set_rtcwake_wakeup(wakeup_dt):
    global next_wakeup_dt
    # Преобразуем локальное время в UTC
    local_tz = datetime.now().astimezone().tzinfo
    wakeup_dt_utc = wakeup_dt.astimezone(timezone.utc)
    epoch = int(wakeup_dt_utc.timestamp())

    print(
        f"Установка rtcwake на {wakeup_dt.strftime('%Y-%m-%d %H:%M:%S')} (локальное) -> {wakeup_dt_utc.strftime('%Y-%m-%d %H:%M:%S')} (UTC) -> {epoch}"
    )
    try:
        # -m no — не переходить в режим сна, только установка времени пробуждения
        subprocess.run(["rtcwake", "-m", "no", "-t", str(epoch)], check=True)
        if debug:
            print(f"rtcwake: wakeup using /dev/rtc0 at {wakeup_dt_utc} (локальное)")
        set_wake_enabled(True)
        next_wakeup_dt = wakeup_dt
    except subprocess.CalledProcessError as e:
        print(f"Ошибка rtcwake: {e}")


def set_wakeup_from_config():
    """Устанавливает rtcwake на основании времени из конфигурации"""
    now = datetime.now()
    time_str = get_wake_time()  # формат HH:MM

    try:
        hour, minute = map(int, time_str.split(":"))
    except ValueError:
        print("❌ Неверный формат времени в конфиге, ожидалось HH:MM")
        return

    # Создаем datetime в локальном времени
    wakeup_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if wakeup_dt <= now:
        wakeup_dt += timedelta(days=1)
        if debug:
            print(
                f"⏱ Время прошло, переносим на следующий день: {wakeup_dt.isoformat()} (локальное)"
            )

    if debug:
        print(
            f"⏱ Установка пробуждения (из конфига) на {wakeup_dt.isoformat()} (локальное время)"
        )
    set_rtcwake_wakeup(wakeup_dt)
    notify_wakeup_set(wakeup_dt)


def notify_wakeup_set(wakeup_dt):
    subprocess.Popen(
        [
            "notify-send",
            "--icon=alarm",
            "Пробуждение установлено",
            wakeup_dt.strftime("на %Y-%m-%d %H:%M:%S (локальное время)"),
        ]
    )


def cancel_rtcwake():
    """Отменяет запланированное пробуждение"""
    try:
        subprocess.run(["rtcwake", "-m", "disable"], check=True)
        print("🗑 rtcwake: пробуждение отменено")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка отмены rtcwake: {e}")


# 2. Добавить логгирование в файл
import logging


def setup_logging():
    log_dir = os.path.join(SCRIPT_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{APP_NAME}.log")
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


# 3. Улучшенная проверка зависимостей
def check_dependencies():
    """Проверка наличия всех необходимых системных зависимостей"""
    required_binaries = [
        "rtcwake",
        "xprintidle",
        "gnome-screenshot",
        "setxkbmap",  # Основной способ переключения раскладки
    ]

    missing = []
    for bin in required_binaries:
        if shutil.which(bin) is None:
            missing.append(bin)

    if missing:
        logging.error(f"Отсутствуют необходимые бинарные файлы: {', '.join(missing)}")
        return False
    return True


# 4. Защита от множественного запуска
def check_already_running():
    lock_file = os.path.join(SCRIPT_DIR, f"{APP_NAME}.lock")
    try:
        fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        with os.fdopen(fd, "w") as f:
            f.write(str(os.getpid()))
        return True
    except OSError:
        logging.error("Программа уже запущена")
        return False


def set_english_layout():
    """Переключение на английскую раскладку с подробной отладкой"""
    methods = [
        {"cmd": ["setxkbmap", "us"], "name": "setxkbmap (основной метод)"},
        {
            "cmd": [
                "gsettings",
                "set",
                "org.gnome.desktop.input-sources",
                "current",
                "0",
            ],
            "name": "gsettings (для GNOME)",
        },
        {
            "cmd": ["localectl", "set-x11-keymap", "us"],
            "name": "localectl (системный метод)",
        },
    ]

    print("\n=== Попытка переключения на английскую раскладку ===")

    for method in methods:
        print(f"\nПробуем метод: {method['name']}")
        print(f"Команда: {' '.join(method['cmd'])}")

        try:
            result = subprocess.run(
                method["cmd"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            print("✅ Успешно выполнено")
            print(f"Вывод: {result.stdout.strip() or 'нет вывода'}")
            return True

        except subprocess.CalledProcessError as e:
            print("❌ Ошибка выполнения:")
            print(f"Код возврата: {e.returncode}")
            print(f"Ошибка: {e.stderr.strip() or 'нет сообщения об ошибке'}")
            continue

        except Exception as e:
            print(f"⚠️ Неожиданная ошибка: {str(e)}")
            continue

    print("\n=== Все методы переключения раскладки не сработали ===")

    # Дополнительная диагностика
    try:
        print("\nПроверяем текущую раскладку:")
        current_layout = subprocess.run(
            ["setxkbmap", "-query"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(current_layout.stdout.strip() or "Не удалось определить раскладку")
    except Exception as e:
        print(f"Ошибка проверки раскладки: {str(e)}")

    return False


class TrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.app = QtWidgets.QApplication.instance()
        self.setToolTip(APP_NAME)

        self.idle_shutdown_enabled = is_auto_shutdown_enabled()

        # Инициализация меню
        self.init_menu()

        self.idle_check_timer = QtCore.QTimer()
        self.idle_check_timer.timeout.connect(self.check_user_idle)
        self.idle_check_timer.start(30 * 1000)

        self.update_menu()
        self.show()

    def init_menu(self):
        """Инициализация пунктов меню"""
        self.menu = QtWidgets.QMenu()
        self.setContextMenu(self.menu)

        # Информационный пункт
        self.info_action = QtWidgets.QAction("", self)
        self.info_action.setEnabled(False)

        # Основные действия
        self.wakeup_action = QtWidgets.QAction("", self)
        self.wakeup_action.triggered.connect(self.toggle_wakeup)

        self.change_time_action = QtWidgets.QAction(
            "Изменить время пробуждения...", self
        )
        self.change_time_action.triggered.connect(self.change_wake_time)

        self.terminal_action = QtWidgets.QAction("", self)
        self.terminal_action.triggered.connect(self.toggle_terminal)

        # Настройки
        self.idle_action = QtWidgets.QAction("Выключать при простое", self)
        self.idle_action.setCheckable(True)
        self.idle_action.setChecked(is_auto_shutdown_enabled())
        self.idle_action.toggled.connect(self.toggle_idle_shutdown)

        self.telegram_action = QtWidgets.QAction("Отправлять снимок в ТГ", self)
        self.telegram_action.setCheckable(True)
        self.telegram_action.setChecked(is_telegram_enabled())
        self.telegram_action.toggled.connect(self.toggle_telegram)

        self.change_idle_timeout_action = QtWidgets.QAction(
            "Изменить время простоя...", self
        )
        self.change_idle_timeout_action.triggered.connect(self.change_idle_timeout)

        # Выход
        self.exit_action = QtWidgets.QAction("Выход", self)
        self.exit_action.triggered.connect(self.clean_exit)  # Исправленная строка

    def update_menu(self):
        """Обновляет пункты меню в зависимости от состояния автопробуждения"""
        self.menu.clear()

        # Информационный пункт меню
        time_str = get_wake_time()
        if is_wake_enabled():
            info_text = f"Пробуждение установлено на: {time_str}"
        else:
            info_text = f"Пробуждение возможно на: {time_str}"
        self.info_action.setText(info_text)
        self.menu.addAction(self.info_action)

        # Кнопка автопробуждения
        if is_wake_enabled():
            self.wakeup_action.setText("Отменить автопробуждение")
        else:
            self.wakeup_action.setText("Установить автопробуждение")
        self.menu.addAction(self.wakeup_action)

        # Смена времени
        self.menu.addAction(self.change_time_action)

        # Чекбокс "Выключать при простое"
        self.idle_action = QtWidgets.QAction(
            f"Выключать при простое {get_idle_timeout()} сек. ", self
        )
        self.idle_action.setCheckable(True)
        self.idle_action.setChecked(is_auto_shutdown_enabled())
        self.idle_action.toggled.connect(self.toggle_idle_shutdown)
        self.menu.addAction(self.idle_action)

        # Смена времени простоя
        self.menu.addAction(self.change_idle_timeout_action)

        # Чекбокс "Выключать при простое"
        self.telegram_action = QtWidgets.QAction(f"Отправлять снимок в ТГ", self)
        self.telegram_action.setCheckable(True)
        self.telegram_action.setChecked(is_telegram_enabled())
        self.telegram_action.toggled.connect(self.toggle_telegram)
        self.menu.addAction(self.telegram_action)

        # Отображение/скрытие терминала
        if is_terminal_enabled():
            self.terminal_action.setText("Скрывать Терминал")
        else:
            self.terminal_action.setText("Отображать Терминал")
        self.menu.addAction(self.terminal_action)

        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)

    def clean_exit(self):
        """Корректное завершение работы"""
        try:
            print("Завершение работы приложения...")

            # Остановка таймеров
            self.idle_check_timer.stop()

            # Сохранение данных
            if hasattr(self, "idle_shutdown_enabled"):
                data = load_wake_data()
                data["auto_shutdown"] = self.idle_shutdown_enabled
                save_wake_data(data)

            # Закрытие GUI
            self.hide()
            self.app.quit()

        except Exception as e:
            print(f"Ошибка при завершении: {e}")
            sys.exit(1)

    # Остальные методы класса остаются без изменений
    # ...

    def toggle_wakeup(self):
        """Переключает режим автопробуждения"""
        if is_wake_enabled():
            print("❎ Отключаем автопробуждение")
            cancel_rtcwake()
            set_wake_enabled(False)
        else:
            print("✅ Включаем автопробуждение")
            self.set_wakeup()  # устанавливаем rtcwake
            # set_wake_enabled(True)
        self.update_menu()

    def prompt_telegram_config(self):
        token, ok1 = QtWidgets.QInputDialog.getText(
            None, "Telegram Token", "Введите Telegram Bot Token:"
        )
        if not ok1 or not token.strip():
            return

        chat_id, ok2 = QtWidgets.QInputDialog.getText(
            None, "Telegram Chat ID", "Введите Telegram Chat ID:"
        )
        if not ok2 or not chat_id.strip():
            return

        data = load_wake_data()
        data["telegram_token"] = token.strip()
        data["telegram_chat_id"] = chat_id.strip()
        save_wake_data(data)
        print("✅ Данные Telegram сохранены.")

    def toggle_terminal(self):
        """Переключает режим вывода в Териминал"""
        if is_terminal_enabled():
            print("❎ Отключаем Терминал")
            set_terminal_enabled(False)
        else:
            print("✅ Включаем Терминал")
            set_terminal_enabled(True)
        ensure_autostart()
        self.update_menu()

    def set_wakeup(self):
        global next_wakeup_dt
        now = datetime.now()
        # now = datetime.now(timezone.utc)
        print(f"⏱ now = {now.isoformat()} local time")

        time_str = get_wake_time()  # формат HH:MM
        try:
            hour, minute = map(int, time_str.split(":"))
        except ValueError:
            print("❌ Неверный формат времени в конфиге, ожидалось HH:MM")
            return

        wakeup_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if wakeup_dt <= now:
            wakeup_dt += timedelta(days=1)
            if debug:
                print(
                    f"⏱ Время прошло, переносим на следующий день: {wakeup_dt.isoformat()} local time"
                )
        if debug:
            print(f"⏱ Установка пробуждения на {wakeup_dt.isoformat()} local time")
        set_rtcwake_wakeup(wakeup_dt)
        next_wakeup_dt = wakeup_dt  # <-- сохраняем для дальнейшего сравнения

    def change_wake_time(self):
        """Открывает диалог выбора времени пробуждения"""
        current = get_wake_time()
        try:
            hour, minute = map(int, current.split(":"))
        except:
            hour, minute = 7, 0

        time_dialog = QtWidgets.QTimeEdit()
        time_dialog.setTime(QtCore.QTime(hour, minute))
        time_dialog.setDisplayFormat("HH:mm")
        time_dialog.setWindowTitle("Выберите время пробуждения")
        time_dialog.setFixedWidth(100)

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Изменить время пробуждения")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Время (часы:минуты):"))
        layout.addWidget(time_dialog)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_time = time_dialog.time().toString("HH:mm")
            set_wake_time(new_time)

            print(f"⏱ Новое время пробуждения: {new_time}")
            if is_wake_enabled():
                self.set_wakeup()  # пересчёт rtcwake
            self.update_menu()

    ###############################
    def change_idle_timeout(self):
        """Открывает диалог выбора времени простоя (в секундах)"""
        current = get_idle_timeout()

        spin_box = QtWidgets.QSpinBox()
        spin_box.setRange(10, 86400)  # от 10 секунд до 24 часов
        spin_box.setValue(current)
        # spin_box.setSuffix(" сек.")
        spin_box.setSingleStep(10)

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Изменить таймаут простоя")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Введите время простоя в секундах:"))
        layout.addWidget(spin_box)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_timeout = spin_box.value()
            set_idle_timeout(new_timeout)
            print(f"⏱ Новый таймаут простоя: {new_timeout} сек.")
            self.update_menu()

    def toggle_idle_shutdown(self, checked):
        print(f"🌓 Переключение автоотключения: {checked}")
        set_auto_shutdown(checked)
        self.idle_shutdown_enabled = checked

    def toggle_telegram(self, checked):
        print(f" Переключение отправки снимка в Телеграм: {checked}")
        set_telegram_enabled(checked)
        self.telegram_enabled = checked

        if checked:
            data = load_wake_data()
            if not data.get("telegram_token") or not data.get("telegram_chat_id"):
                self.prompt_telegram_config()

    def check_user_idle(self):
        try:
            if not self.idle_shutdown_enabled:
                return

            idle_ms = int(subprocess.check_output(["xprintidle"]).decode().strip())
            idle_sec = idle_ms / 1000

            if idle_sec >= get_idle_timeout():
                if (
                    is_wake_enabled()
                    and isinstance(next_wakeup_dt, datetime)
                    and next_wakeup_dt > datetime.now()
                ):
                    print(
                        f"💤 Нет активности. Автовыключение... Будет пробуждение в {next_wakeup_dt}"
                    )
                    print(f" сейчас datetime.now() = {datetime.now()}")
                    self.show_shutdown_warning()
                else:
                    print(
                        "⚠️ Автовыключение отменено — не задано пробуждение в будущем."
                    )
                    set_wakeup_from_config()
        except Exception as e:
            print(f"⚠️ Ошибка при проверке простоя: {e}")

    def show_shutdown_warning(self):
        print("📤 Отправка снимка и выключение...")
        if is_telegram_enabled():
            capture_camera_and_send("Before power off")
            capture_screen_and_send("Before power off")
        dialog = QtWidgets.QMessageBox()
        dialog.setIcon(QtWidgets.QMessageBox.Warning)
        dialog.setWindowTitle("Автовыключение")
        dialog.setText("Система будет выключена через 30 секунд из-за бездействия.")
        dialog.setInformativeText("Нажмите 'Отмена', чтобы отменить выключение.")
        dialog.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )
        dialog.setDefaultButton(QtWidgets.QMessageBox.Cancel)

        cancelled = {"value": False}

        def proceed_shutdown():
            if not cancelled["value"]:

                # subprocess.run(["systemctl", "poweroff"])
                # Новый вариант — с игнорированием блокировок
                subprocess.run(["systemctl", "poweroff", "-i"])

            # Закрываем диалог, если он ещё не закрыт
            dialog.done(0)

        # Автоматическое выполнение через 30 секунд
        QtCore.QTimer.singleShot(30_000, proceed_shutdown)

        result = dialog.exec_()
        if result == QtWidgets.QMessageBox.Cancel:
            cancelled["value"] = True
            print("⏹️ Пользователь отменил выключение.")
        else:
            print("✅ Пользователь подтвердил выключение.")


tray = None  # глобальная переменная для хранения TrayApp


def main():
    global tray

    # Выполняем установку pip и модулей при старте
    # if not check_already_running():
    # sys.exit(1)

    setup_logging()
    logging.info("Запуск приложения")

    # Установка английской раскладки при старте
    set_english_layout()

    try:
        # if not check_dependencies():
        # sys.exit(1)
        # install_missing_modules()
        # if not install_missing_modules():
        # sys.exit(1)

        load_wake_data()
        ensure_telegram_config()
        if is_telegram_enabled():
            try:
                capture_camera_and_send("On boot")
            except Exception as e:
                logging.error(f"Ошибка при отправке Telegram: {e}")

        show_startup_notification()
        ensure_autostart()
        ensure_rtc_access()
        add_cap_sys_time()
        dm = detect_display_manager()
        if dm == "gdm3":
            ensure_gdm_autologin_enabled()
        elif dm == "lightdm":
            ensure_lightdm_autologin_enabled()

        if not check_xprintidle():
            logging.warning("xprintidle не найден, некоторые функции будут недоступны")

        app = QtWidgets.QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        # Настройка обработки Ctrl+C в терминале
        # signal.signal(signal.SIGINT, lambda *args: app.quit())

        if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            QtWidgets.QMessageBox.critical(None, "Ошибка", "Системный трей недоступен.")
            capture_screen_and_send("On boot. Error")
            sys.exit(1)

        dummy_window = QtWidgets.QWidget()
        dummy_window.setAttribute(QtCore.Qt.WA_DontShowOnScreen)
        dummy_window.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        dummy_window.setVisible(True)
        QtGui.QIcon.setThemeName("Yaru")
        icon = QtGui.QIcon.fromTheme("system-shutdown")
        #capture_screen_and_send("On boot1")

        def delayed_start():
            global tray
            try:
                tray = TrayApp(icon, parent=dummy_window)
                if is_wake_enabled():
                    set_wakeup_from_config()
                    capture_screen_and_send("On boot")
            except Exception as e:
                logging.error(f"Ошибка при создании трея: {e}")
                capture_screen_and_send("On boot. Error")
                sys.exit(1)

        QtCore.QTimer.singleShot(2000, delayed_start)
        #capture_screen_and_send("On boot2")
        sys.exit(app.exec_())
        
        
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}")
        capture_screen_and_send("On boot. Error")
        sys.exit(1)


if __name__ == "__main__":
    main()
