# О проекте
Python 3.8.10

# Запуск
## настройки вирутального окружения

python3 -m venv venv 
venv/Scripts/activate - Windows
source venv/bin/activate - Mac/Linux
pip3 install -r requirements.txt

## создание бд
prisma db push

## запуск бота
python3 bot.py

## просмотр бд
prisma studio

# дполнительные команды
## вынести все зависмости в отдельный файл
pip3 freeze > requirements.txt

# проверить 
telebot - проверить, похоже есть методы для просомтра сообщений