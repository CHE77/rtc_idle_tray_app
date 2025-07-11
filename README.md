
![Превью](https://github.com/CHE77/rtc_idle_tray_app/raw/main/preview.jpg)


Приложение устанавливает пробужение компьютера на нужное время. По пробуждению делает скриншот экрана и снимок камерой, отпрвляет их в Телеграм. Если нет активности то устнавливет пробуждение на следующий день и выключает компьютер. 

Работает с Gnome и lightdm.

Усанавливает возможность пробуждения по сети - WakeOnLan


Предварительные настройки:

Выключите режим экономии питания

Сделайте вход в систему без запроса пароля

Устаноивате AnyDesk и насторойте его автозапуск

Telegram: Создайте бот-токен в https://t.me/BotFather и узнайте свой сhat-id в https://t.me/myidbot





# 📦 Инструкция по установке `rtc_idle_tray_app`

## 🔧 Установка из архива (`.zip`)

1. **Скачайте архив:**

   Перейдите на страницу проекта:  
   https://github.com/CHE77/rtc_idle_tray_app

   Нажмите **"Code" → "Download ZIP"**  
   Или скачайте напрямую:  
   https://github.com/CHE77/rtc_idle_tray_app/archive/refs/heads/main.zip

2. **Распакуйте архив:**

   Откройте терминал и выполните:

   ```bash
   cd ~/Downloads
   unzip main.zip
   ```

3. **Скопируйте папку `rtc_idle_tray` в домашний каталог:**

   ```bash
   cp -r rtc_idle_tray_app-main/rtc_idle_tray ~/rtc_idle_tray
   ```

---

## 🔧 Установка через `git` (альтернатива)

Если установлен `git`, можно выполнить:

```bash
cd ~
git clone https://github.com/CHE77/rtc_idle_tray_app.git
cp -r rtc_idle_tray_app/rtc_idle_tray ~/rtc_idle_tray
```

---

## 📥 Установка зависимостей

Перейдите в папку:

```bash
cd ~/rtc_idle_tray
```

Запустите установку зависимостей:

```bash
./install_all_dependencies.py
```

> При необходимости будет запрошен пароль `sudo`.

---

## 🔁 Перезагрузка

После установки перезагрузите систему:

```bash
reboot
```

---

## ▶ Запуск приложения

После перезагрузки:

```bash
cd ~/rtc_idle_tray
./rtc_idle_tray.py
```

---

Готово. Программа запустится и появится в трее.
