from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')
FILM_CREATE_COMMAND = Command("create_film")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="create_film", description="Додати новий фільм"),
]
