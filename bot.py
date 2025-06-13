# Імпортуємо необхідні модулі
import asyncio  # Для асинхронного програмування
import logging  # Для логування подій
import sys  # Для доступу до деяких змінних та функцій, пов'язаних з інтерпретатором Python

# Імпортуємо токен бота з конфігураційного файлу
from config import BOT_TOKEN as TOKEN

# Імпортуємо необхідні класи та функції з бібліотеки aiogram
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Імпортуємо команди, які використовуються в боті
from commands import (FILMS_COMMAND, START_COMMAND, FILM_CREATE_COMMAND, BOT_COMMANDS)

# Імпортуємо функції для отримання та додавання даних про фільми
from data import get_films, add_film

# Імпортуємо функції для створення клавіатур та обробки зворотних викликів
from keyboards import films_keyboard_markup, FilmCallback

# Імпортуємо модель даних для фільму
from models import Film

# Ініціалізуємо диспетчер для обробки оновлень
dp = Dispatcher()


class FilmForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()


# Обробник для команди /start
@dp.message(Command("start"))
async def start(message: Message) -> None:
    # Відповідаємо на команду /start, вітаючи користувача
    await message.answer(
        f"Hello🖐, {html.bold(message.from_user.full_name)}!\n"
        "I'm your first Telegram Bot 🥳"
    )


# Обробник для команди /films
@dp.message(FILMS_COMMAND)
async def films(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        f"<b>Список фільмів: 🎞</b>\nОберіть фільм, щоб отримати інформацію про нього.",
        reply_markup=markup
    )


# Обробник зворотного виклику для фільмів
@dp.callback_query(FilmCallback.filter())
async def callback_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    # Отримуємо ID фільму з даних зворотного виклику
    film_id = callback_data.id
    # Отримуємо дані про конкретний фільм за його ID
    film_data = get_films(film_id=film_id)
    # Створюємо об'єкт фільму
    film = Film(**film_data)

    # Формуємо текст повідомлення з деталями про фільм
    text = f"<b>Фільм:</b> {film.name}\n" \
           f"<b>Опис:</b> {film.description}\n" \
           f"<b>Рейтинг:</b> {film.rating}\n" \
           f"<b>Жанр:</b> {film.genre}\n" \
           f"<b>Актори:</b> {', '.join(film.actors)}\n"

    # Відправляємо фото з постером фільму та текстом з деталями
    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            film.poster,
            filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
        )
    )


@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmForm.name)
    await message.answer(
        f"<b>Введіть назву фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.name)
async def film_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer(
        f"<b>Введіть опис фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.description)
async def film_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer(
        f"<b>Вкажіть рейтинг фільму (від 0 до 10) ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=float(message.text))
    await state.set_state(FilmForm.genre)
    await message.answer(
        f"<b>Введіть жанр фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer(
        text=f"<b>Введіть акторів фільму через `, ` \n⚠️ (Обов'язкова кома та відступ після неї)</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
    await state.update_data(actors=[x for x in message.text.split(", ")])
    await state.set_state(FilmForm.poster)
    await message.answer(
        f"<b>Введіть посилання на постер фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
    data = await state.update_data(poster=message.text)
    film = Film(**data)
    add_film(film.model_dump())
    await state.clear()
    await message.answer(
        f"Фільм {film.name} успішно додано ✅",
        reply_markup=ReplyKeyboardRemove(),
    )


# Головна асинхронна функція для запуску бота
async def main() -> None:
    # Ініціалізуємо екземпляр бота з токеном та властивостями за замовчуванням
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Встановлюємо команди бота
    await bot.set_my_commands(BOT_COMMANDS)
    # Запускаємо цикл опитування для отримання оновлень
    await dp.start_polling(bot)


# Перевіряємо, чи скрипт запускається напряму
if __name__ == "__main__":
    # Налаштовуємо базове логування для виведення інформаційних повідомлень у стандартний потік виведення
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Запускаємо головну асинхронну функцію
    asyncio.run(main())
