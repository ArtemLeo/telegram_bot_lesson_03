# Імпортуємо необхідні модулі
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


# Створимо клас для реалізації `CallbackData`
class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    name: str


def films_keyboard_markup(films_list: list[dict], offset: int | None = None, skip: int | None = None):
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    for index, film_data in enumerate(films_list):
        callback_data = FilmCallback(id=index, **film_data)
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()
