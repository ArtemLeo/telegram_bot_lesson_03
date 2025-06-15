from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    name: str


# Функція для створення клавіатури з фільмами
def films_keyboard_markup(films_list: list[dict], offset: int | None = None, skip: int | None = None):
    # Створюємо об'єкт InlineKeyboardBuilder для побудови клавіатури
    builder = InlineKeyboardBuilder()

    # Установлюємо кількість кнопок у рядку та повторюємо цей шаблон
    builder.adjust(1, repeat=True)

    # Проходимо по списку фільмів та додаємо кнопки для кожного фільму
    for index, film_data in enumerate(films_list):
        # Створюємо об'єкт FilmCallback з даними фільму
        callback_data = FilmCallback(id=index, **film_data)
        # Додаємо кнопку з текстом назви фільму та callback даними
        builder.button(
            text=f"{callback_data.name}",  # Текст кнопки - назва фільму
            callback_data=callback_data.pack()  # Callback дані, які будуть повертатися при натисканні кнопки
        )

    # Повертаємо клавіатуру у вигляді розмітки
    builder.adjust(1, repeat=True)
    return builder.as_markup()
