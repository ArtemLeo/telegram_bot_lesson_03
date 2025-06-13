# ✅ Урок 43: Додавання фільму до списку TelegramBot

---
<img src="main_image.png" alt="pygame" width="1500">

## Зміст уроку:

1. [Сьогодні на уроці](#1-сьогодні-на-уроці)
2. [Реалізація команди `create_film`](#2-реалізація-команди-create_film)
3. [Збереження інформації в `data.json`](#3-збереження-інформації-в-datajson)
4. [Підведення підсумків 🚀](#4-підведення-підсумків-)

---

## 1. Сьогодні на уроці

> 💡 На цьому уроці ми розглянемо наступні теми:

- Як створювати команди, щоб додавати нові фільми до списку в **TelegramBot**.
- Як обробляти введені користувачем дані та зберігати інформацію у файлі.

На попередньому уроці ми навчилися створювати команди для перегляду списку фільмів та отримувати інформацію про кожен з
них.

Тепер ми перейдемо до наступного кроку - **додавання фільмів** до списку, що дозволить користувачам самостійно
оновлювати бібліотеку з фільмами.

[Повернутися до змісту](#зміст-конспекту)

---

## 2. Реалізація команди `create_film`

Необхідно створити нову команду `create_film` в модулі `commands.py`.

```python
# Old code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

FILMS_COMMAND = Command('films')
START_COMMAND = Command('start')

FILMS_BOT_COMMAND = BotCommand(command='films', description="Перегляд списку фільмів")
START_BOT_COMMAND = BotCommand(command='start', description="Почати розмову")
```

```python
# New code
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
```

Необхідно змінити імпорти в модулі `bot.py`.

```python
# Old code
from commands import (FILMS_COMMAND, START_COMMAND, FILMS_BOT_COMMAND, START_BOT_COMMAND)
```

```python
# New code
from commands import (FILMS_COMMAND, START_COMMAND, FILM_CREATE_COMMAND, BOT_COMMANDS)
```

Необхідно додати оновлені команди до головної функції `main()`.

```python
# Old code
async def main() -> None:
    # Ініціалізуємо екземпляр бота з токеном та властивостями за замовчуванням
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Встановлюємо команди бота
    await bot.set_my_commands([FILMS_BOT_COMMAND, START_BOT_COMMAND])

    # Запускаємо цикл опитування для отримання оновлень
    await dp.start_polling(bot)
```

```python
# New code
async def main() -> None:
    # Ініціалізуємо екземпляр бота з токеном та властивостями за замовчуванням
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Встановлюємо команди бота
    await bot.set_my_commands(BOT_COMMANDS)
    # Запускаємо цикл опитування для отримання оновлень
    await dp.start_polling(bot)
```

Для створення нового фільму необхідно додати наступні імпорти в модуль `bot.py`.

```python
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
```

```python
# Old code
from aiogram.types import Message, CallbackQuery, URLInputFile

# New code
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
```

Посилання на додатковий матеріал по
FSMContext [(Finite State Machine)](https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/)

Створимо форму для отримання інформації про фільми від користувача в модулі `bot.py`.

```python
class FilmForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()
```

Створимо функцію `film_create()` в модулі `bot.py`, як обробник команди `/create_film` та додамо обробники для кожного
поля форми.

```python
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
```

Коли ми створюємо бот, який збирає інформацію від користувача крок за кроком (наприклад, спочатку **назва** фільму,
потім **опис**, **рейтинг** і так далі), нам необхідно відстежувати, на якому етапі знаходиться користувач.

- Відстежування кожного етапу відбувається за допомогою **"машини станів"**.
- Кожен обробник, окрім останнього, встановлює наступний стан, по черзі.
- Наприклад, коли користувач вводить назву фільму, бот зберігає цю інформацію і переходить до очікування опису фільму.
- Це означає, що наступне повідомлення від користувача буде оброблятися функцією, яка відповідає за опис фільму.

Обробник `film_poster` є останнім кроком у зборі інформації про фільм.

- Коли користувач вводить посилання на постер фільму, бот зберігає всі дані, які були введені раніше (**назва, опис,
  рейтинг, жанр, актори, посилання на постер**) у змінну `data`.
- Після збереження даних, бот очищає контекст, тобто **"забуває"** поточний стан, щоб бути готовим до нової взаємодії з
  користувачем.
- Це означає, що бот завершив процес збору даних про фільм і готовий почати спочатку, якщо користувач захоче додати ще
  один фільм.

[Повернутися до змісту](#зміст-конспекту)

---

## 3. Збереження інформації в `data.json`

Необхідно змінити модуль `data.py`, для того, щоб інформація про новий фільм потрапила в файл `data.json`.

```python
# Імпорт бібліотеки json
import json


#  Функція для отримання списку фільмів
def get_films(file_path: str = "data.json", film_id: int | None = None) -> list[dict] | dict:
    with open(file_path, 'r') as fp:
        films = json.load(fp)
        if film_id is not None and film_id < len(films):
            return films[film_id]
        return films


#  Функція для додавання нового фільму у список
def add_film(film: dict, file_path: str = "data.json"):
    films = get_films(file_path=file_path, film_id=None)
    if films:
        films.append(film)
        with open(file_path, "w") as fp:
            json.dump(films, fp, indent=4, ensure_ascii=False)
```

Необхідно додати імпорт нової функції в модуль `bot.py`.

```python
# Old string
from data import get_films

# New string
from data import get_films, add_film
```

Запускаємо нашу програму та перевіряємо зміни в **TelegramBot**.

[Повернутися до змісту](#зміст-конспекту)

---

## 4. Підведення підсумків 🚀

> На цьому уроці ми вивчили наступні теми:

- Навчився створювати команду `/create_film` для додавання фільмів у **TelegramBot**.
- Розглянули, як отримувати інформацію від користувача через повідомлення та зберігати дані у файл.
- Вивчили основи взаємодії бота з користувачами та роботу з даними, що є важливим етапом у створенні інтерактивного та
  корисного **TelegramBot**.

> Тепер наш застосунок здатен не тільки демонструвати список фільмів та показувати детальну інформацію по кожному з них,
> але й оновлювати бібліотеку за допомогою введених користувачем даних.

[Повернутися до змісту](#зміст-конспекту)


