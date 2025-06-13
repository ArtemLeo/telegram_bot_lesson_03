from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

FILMS_COMMAND = Command('films')
START_COMMAND = Command('start')
FILM_CREATE_COMMAND = Command("create_film")

BOT_COMMANDS = [
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="create_film", description="Додати новий фільм"),
]


