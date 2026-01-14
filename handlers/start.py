from aiogram import Router, types
from aiogram.filters import Command
from keyboards import get_main_keyboard
from deps import get_db  # Импортируем из deps.py

router = Router()

@router.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    # Получаем db через deps
    db = get_db()
    
    user_id = message.from_user.id
    
    # Добавляем пользователя в БД
    await db.add_user(user_id)
    
    # Получаем язык пользователя
    user = await db.get_user(user_id)
    lang = user[1] if user else 'ru'
    
    if lang == 'ru':
        welcome_text = (
            "👋 *Добро пожаловать в Currency Bot!*\n\n"
            "Я помогу вам с конвертацией валют и не только!\n\n"
            "*Основные функции:*\n"
            "💰 Конвертировать валюту\n"
            "⭐ Избранные курсы\n"
            "📈 История операций\n"
            "🧮 Калькулятор комиссий\n"
            "💸 Калькулятор чаевых\n"
            "ℹ️ Информация о валютах\n"
            "🌍 Смена языка\n\n"
            "Используйте кнопки ниже или команды!"
        )
    else:
        welcome_text = (
            "👋 *Welcome to Currency Bot!*\n\n"
            "I'll help you with currency conversion and more!\n\n"
            "*Main features:*\n"
            "💰 Convert currency\n"
            "⭐ Favorite rates\n"
            "📈 Operation history\n"
            "🧮 Commission calculator\n"
            "💸 Tips calculator\n"
            "ℹ️ Currency information\n"
            "🌍 Language switch\n\n"
            "Use the buttons below or commands!"
        )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )