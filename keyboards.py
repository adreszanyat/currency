from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

# Основная клавиатура
def get_main_keyboard(lang='ru'):
    if lang == 'ru':
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💰 Конвертировать"), KeyboardButton(text="📊 Курсы")],
                [KeyboardButton(text="⭐ Избранное"), KeyboardButton(text="📈 История")],
                [KeyboardButton(text="🧮 Калькулятор комиссий"), KeyboardButton(text="💸 Чаевые")],
                [KeyboardButton(text="ℹ️ Информация о валютах"), KeyboardButton(text="🌍 Язык")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💰 Convert"), KeyboardButton(text="📊 Rates")],
                [KeyboardButton(text="⭐ Favorites"), KeyboardButton(text="📈 History")],
                [KeyboardButton(text="🧮 Fee Calculator"), KeyboardButton(text="💸 Tips")],
                [KeyboardButton(text="ℹ️ Currency Info"), KeyboardButton(text="🌍 Language")]
            ],
            resize_keyboard=True
        )

# Клавиатура для выбора валют (inline)
def get_currency_keyboard(selected_currencies=None, action="convert_from"):
    if selected_currencies is None:
        selected_currencies = []
    
    currencies = ['USD', 'EUR', 'RUB', 'KZT', 'UAH', 'CNY', 'GBP', 'JPY']
    buttons = []
    
    for i in range(0, len(currencies), 4):
        row = []
        for currency in currencies[i:i+4]:
            prefix = "✅ " if currency in selected_currencies else ""
            row.append(InlineKeyboardButton(
                text=f"{prefix}{currency}", 
                callback_data=f"{action}:{currency}"
            ))
        buttons.append(row)
    
    if action == "convert_from":
        buttons.append([InlineKeyboardButton(text="Далее ▶️", callback_data="next_step")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура для управления избранным
def get_favorites_keyboard(favorites, lang='ru'):
    buttons = []
    
    for fav in favorites:
        from_curr, to_curr = fav
        text = f"{from_curr} → {to_curr}"
        if lang == 'ru':
            callback = f"fav_convert:{from_curr}:{to_curr}"
            buttons.append([InlineKeyboardButton(text=text, callback_data=callback)])
            buttons.append([
                InlineKeyboardButton(text="❌ Удалить", callback_data=f"fav_remove:{from_curr}:{to_curr}")
            ])
        else:
            callback = f"fav_convert:{from_curr}:{to_curr}"
            buttons.append([InlineKeyboardButton(text=text, callback_data=callback)])
            buttons.append([
                InlineKeyboardButton(text="❌ Remove", callback_data=f"fav_remove:{from_curr}:{to_curr}")
            ])
    
    if lang == 'ru':
        buttons.append([InlineKeyboardButton(text="➕ Добавить пару", callback_data="add_favorite")])
    else:
        buttons.append([InlineKeyboardButton(text="➕ Add pair", callback_data="add_favorite")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура выбора языка
def get_language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")]
        ]
    )