import os
import time
import logging
from selenium import webdriver
from PIL import Image
from telegram import Bot, Update, InputFile
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваш токен Telegram бота
API_TOKEN = 'BOT_TOKEN'

# Функция для захвата длинного скриншота
def capture_long_screenshot(url, output_path):
    options = Options()
    options.add_argument('--headless')  # Запуск браузера в фоновом режиме
    options.add_argument('--disable-gpu')  # Отключение GPU, если он не нужен
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(60)  # Ожидание полной загрузки страницы

    # Скролл до самого конца страницы, чтобы все элементы загрузились
    total_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(total_width, total_height)

    # Сделать скриншот всей страницы
    driver.save_screenshot(output_path)
    driver.quit()

# Хэндлер для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("User %s started the bot", user.username)
    await update.message.reply_text("Привет! Отправь мне ссылку, и я сделаю скриншот этой страницы.")

# Хэндлер для текстовых сообщений, содержащих URL
async def process_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    url = update.message.text
    logger.info("Received link from %s: %s", user.username, url)
    screenshot_path = 'screenshot.png'
    
    try:
        capture_long_screenshot(url, screenshot_path)
        # Отправка скриншота пользователю
        with open(screenshot_path, 'rb') as file:
            await update.message.reply_document(InputFile(file))
        os.remove(screenshot_path)  # Удаление файла после отправки
        logger.info("Screenshot taken and sent to %s", user.username)
    except Exception as e:
        logger.error("Error processing link from %s: %s", user.username, e)
        await update.message.reply_text(f"Произошла ошибка при обработке ссылки: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Хэндлер команды /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # Хэндлер текстовых сообщений, которые не являются командами
    link_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_link)
    application.add_handler(link_handler)

    logger.info("Bot is starting...")
    application.run_polling()
    logger.info("Bot has stopped.")
