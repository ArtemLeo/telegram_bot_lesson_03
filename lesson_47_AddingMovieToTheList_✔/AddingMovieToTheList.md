# ✅ Урок 43: Додавання фільму до списку TelegramBot

---
<img src="main_image.png" alt="pygame" width="1500">

## Зміст уроку:

1. [Сьогодні на уроці](#1-сьогодні-на-уроці)
2. [Реалізація команди `/create_film`](#2-реалізація-команди-create_film)
3. [Збереження інформації в `data.json`](#3-збереження-інформації-в-datajson)
4. [Підведення підсумків 🚀](#4-підведення-підсумків-)

> 🔗 Useful Links:

- [FSMContext](https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/)

---

## 1. Сьогодні на уроці

> 💡 На цьому уроці ми розглянемо наступні теми:

- Як створити команди, щоб додавати нові фільми до списку в **TelegramBot**.
- Як обробляти введені користувачем дані та зберігати інформацію у файлі.

На попередньому уроці ми вже навчилися створювати команди для перегляду списку фільмів та отримувати інформацію про
кожен з них.

> Сьогодні ми реалізуємо наступний крок - **додавання фільмів** до списку, що дозволить користувачам самостійно
> оновлювати бібліотеку з фільмами.

[Повернутися до змісту](#зміст-конспекту)

---

## 2. Реалізація команди `/create_film`

Необхідно створити нову команду `create_film` в модулі `commands.py`:

```python
# Old code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')

BOT_COMMANDS = [
    BotCommand(command='start', description="Почати розмову"),
    BotCommand(command='films', description="Перегляд списку фільмів")
]
```

```python
# New code
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
```

Також, необхідно змінити імпорти в модулі `bot.py`:

```python
# Old code
from commands import FILMS_COMMAND, START_COMMAND, BOT_COMMANDS

# New code
from commands import FILMS_COMMAND, START_COMMAND, FILM_CREATE_COMMAND, BOT_COMMANDS
```

Для створення нового фільму необхідно додати наступні імпорти в модуль `bot.py`:

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

💡 Клас `FSMContext` надає контекст для управління станом кінцевого автомата.

- Клас `FSMContext` використовується для зберігання та отримання даних, пов'язаних з поточним станом користувача.
- За допомогою `FSMContext` ви можете зберігати дані між різними обробниками повідомлень, що дозволяє вам створювати
  складні логічні ланцюжки взаємодії з користувачем.

💡 Клас `State` використовується для визначення окремих станів у кінцевому автоматі.

- Кожен стан представляє певний етап у взаємодії з користувачем.
- Наприклад, ви можете мати стани для очікування введення імені користувача, адреси електронної пошти тощо.

💡 Клас `StatesGroup` використовується для групування станів.

- Клас `StatesGroup` дозволяє вам організувати стани в логічні групи, що робить ваш код більш структурованим і
  зрозумілим.
- Наприклад, ви можете мати групу станів для процесу реєстрації користувача, яка включає стани для введення імені,
  адреси електронної пошти, паролю тощо.

💡 Клас `ReplyKeyboardRemove` використовується для видалення клавіатури, яка була відправлена користувачеві раніше.

- Коли ви хочете прибрати клавіатуру, щоб вона не заважала у чаті, ви можете використовувати цей клас.

Створимо `class FilmForm()` в модулі `bot.py` - форму для отримання інформації про фільми від користувача.

```python
# Форма для отримання інформації про фільми від користувача
class FilmForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()
```

💡 Всередині класу `FilmForm` визначаються різні стани, кожен з яких представляє певний етап у взаємодії з користувачем.

Кожен стан використовується для збору інформації про фільм:

- `name = State()`: Цей стан використовується для отримання назви фільму від користувача.
- `description = State()`: Цей стан використовується для отримання опису фільму від користувача.
- `rating = State()`: Цей стан використовується для отримання рейтингу фільму від користувача.
- `genre = State()`: Цей стан використовується для отримання жанру фільму від користувача.
- `actors = State()`: Цей стан використовується для отримання списку акторів фільму від користувача.
- `poster = State()`: Цей стан використовується для отримання постеру фільму від користувача.

Створимо наступні функції: `film_create()`, `film_name()`, `film_description()`, `film_rating()`, `film_genre()`,
`film_actors()` та `film_poster()` в модулі `bot.py`.

Кожна функція - це обробник окремого поля класу `FilmForm` команди `/create_film`:

```python
# Функції-обробники для кожного поля форми отримання інформації від користувача
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
        f"<b>Фільм {film.name} успішно додано ✅</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

💡 Попередній код визначає послідовність обробників повідомлень, які збирають інформацію про фільм від користувача.

> Розглянемо кожен обробник окремо:

### Обробник для початку процесу створення фільму:

```python
@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmForm.name)
    await message.answer(
        f"<b>Введіть назву фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

- `FILM_CREATE_COMMAND` - це команда, яка запускає процес створення фільму.
- `state.set_state(FilmForm.name)`: Встановлює початковий стан для збору інформації про назву фільму.
- `message.answer`: Відправляє повідомлення користувачеві з проханням ввести назву фільму.
- `ReplyKeyboardRemove()` використовується для видалення клавіатури, якщо вона була відправлена раніше.

### Обробник для отримання назви фільму:

```python
@dp.message(FilmForm.name)
async def film_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer(
        f"<b>Введіть опис фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

- `FilmForm.name`: Цей обробник викликається, коли користувач вводить назву фільму.
- `state.update_data(name=message.text)`: Зберігає назву фільму в контексті стану.
- `state.set_state(FilmForm.description)`: Встановлює наступний стан для збору опису фільму.

### Обробник для отримання опису фільму:

```python
@dp.message(FilmForm.description)
async def film_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer(
        f"<b>Вкажіть рейтинг фільму (від 0 до 10) ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

- `FilmForm.description`: Цей обробник викликається, коли користувач вводить опис фільму.
- `state.update_data(description=message.text)`: Зберігає опис фільму в контексті стану.
- `state.set_state(FilmForm.rating)`: Встановлює наступний стан для збору рейтингу фільму.

### Обробник для отримання рейтингу фільму:

```python
@dp.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=float(message.text))
    await state.set_state(FilmForm.genre)
    await message.answer(
        f"<b>Введіть жанр фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

- `FilmForm.rating`: Цей обробник викликається, коли користувач вводить рейтинг фільму.
- `state.update_data(rating=float(message.text))`: Зберігає рейтинг фільму в контексті стану.
- `state.set_state(FilmForm.genre)`: Встановлює наступний стан для збору жанру фільму.

### Обробник для отримання жанру фільму:

```python
@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer(
        text=f"<b>Введіть акторів фільму через `, ` \n⚠️ (Обов'язкова кома та відступ після неї)</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

- `FilmForm.genre`: Цей обробник викликається, коли користувач вводить жанр фільму.
- `state.update_data(genre=message.text)`: Зберігає жанр фільму в контексті стану.
- `state.set_state(FilmForm.actors)`: Встановлює наступний стан для збору списку акторів фільму.

### Обробник для отримання списку акторів фільму:

```python
@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
    await state.update_data(actors=[x for x in message.text.split(", ")])
    await state.set_state(FilmForm.poster)
    await message.answer(
        f"<b>Введіть посилання на постер фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

- `FilmForm.actors`: Цей обробник викликається, коли користувач вводить список акторів фільму.
- `state.update_data(actors=[x for x in message.text.split(", ")])`: Зберігає список акторів фільму в контексті стану.
- `state.set_state(FilmForm.poster)`: Встановлює наступний стан для збору посилання на постер фільму.

### Обробник для отримання посилання на постер фільму:

```python
@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
    data = await state.update_data(poster=message.text)
    film = Film(**data)
    add_film(film.model_dump())
    await state.clear()
    await message.answer(
        f"<b>Фільм {film.name} успішно додано ✅</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
```

- `FilmForm.poster`: Цей обробник викликається, коли користувач вводить посилання на постер фільму.
- `state.update_data(poster=message.text)`: Зберігає посилання на постер фільму в контексті стану.
- `Film(**data)`: Створює об'єкт фільму з використанням даних, зібраних у попередніх станах.
- `add_film(film.model_dump())`: Викликає функцію add_film для додавання фільму до бази даних або списку фільмів.
- `state.clear()`: Очищає стан, завершуючи процес збору інформації про фільм.
- `message.answer`: Відправляє повідомлення користувачеві про успішне додавання фільму.

Попередній код дозволяє боту крок за кроком збирати інформацію про фільм від користувача та зберігати її для подальшого
використання.

[Повернутися до змісту](#зміст-конспекту)

---

## 3. Збереження інформації в `data.json`

Необхідно додати функцію `add_film()` в модуль `data.py`, для того, щоб інформація про новий фільм потрапила в файл
`data.json`.

```python
# Old code
import json


#  Функція для отримання списку фільмів
def get_films(file_path: str = "data.json", film_id: int | None = None) -> list[dict] | dict:
    with open(file_path, 'r') as fp:
        films = json.load(fp)
        if film_id is not None and film_id < len(films):
            return films[film_id]
        return films
```

```python
# New code
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

💡 Функція `add_film()` додає новий фільм до списку фільмів у файлі `data.json`.

Функція `add_film()` використовує `get_films()` для отримання поточного списку фільмів, додає новий фільм до цього
списку і записує оновлений список назад у файл `data.json`.

Також, необхідно **додати імпорт** нової функції `add_film()` в модуль `bot.py`:

```python
# Old string
from data import get_films

# New string
from data import get_films, add_film
```

Запускаємо модуль `bot.py` та перевіряємо зміни в **TelegramBot**.

[Повернутися до змісту](#зміст-конспекту)

---

## 4. Підведення підсумків 🚀

> На цьому уроці ми вивчили наступні теми:

- Навчився створювати команду `/create_film` для додавання фільмів у **TelegramBot**.
- Розглянули, як отримувати інформацію від користувача через повідомлення та зберігати дані у файл.
- Вивчили основи взаємодії бота з користувачем та роботу з даними, що є важливим етапом у створенні інтерактивного та
  корисного **TelegramBot**.

> Тепер наш застосунок здатен не тільки демонструвати **список фільмів** та **детальну інформацію** по кожному з них,
> але й **оновлювати бібліотеку** за допомогою даних, які ввів користувач.

[Повернутися до змісту](#зміст-конспекту)


