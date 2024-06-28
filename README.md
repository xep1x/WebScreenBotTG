# Telegram Bot для скриншотов web-страниц

Этот Telegram бот предназначен для создания скриншотов web-страниц и отправки их пользователю.

## Как использовать

1. **Команда /start**: Запускает бота и предоставляет инструкции.
2. **Отправка ссылки**: После запуска бота отправьте ему URL, чтобы получить скриншот этой страницы.

## Требования

- Python 3.6 и выше

## Установка

1. Клонируйте репозиторий:

    ```
    git clone https://github.com/xep1x/WebScreenBotTG.git
    cd WebScreenBotTG
    ```

2. Установите Chrome WebDriver (если не установлен) с помощью WebDriver Manager:

    ```
    webdriver-manager chrome --linkpath /usr/local/bin
    ```

## Конфигурация

- Замените `API_TOKEN` в `main.py` на свой токен Telegram бота.

## Запуск

