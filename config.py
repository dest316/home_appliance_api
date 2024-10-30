from dotenv import load_dotenv
import os


# Получение данных о подключении к базе данных из файла .env
load_dotenv()

# Создание переменных с полученными из .env данными для подключения
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")