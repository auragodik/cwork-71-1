import os

from dotenv import load_dotenv

load_dotenv()  # читаем переменные из файла .env

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE = 'bot.db'
