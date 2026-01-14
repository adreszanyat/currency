# handlers/favorites.py
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import get_favorites_keyboard, get_currency_keyboard
from utils import convert_currency
from states import FavoriteStates, ConvertStates  # Импортируем состояния
from deps import get_db  # Импортируем функцию для получения db

router = Router()

@router.message(Command("favorites"))
@router.message(F.text.contains("Избранное"))
@router.message(F.text.contains("Favorites"))
async def cmd_favorites(message: types.Message):
    db = get_db()  # Получаем базу данных
    
    favorites = await db.get_favorites(message.from_user.id)
    user = await db.get_user(message.from_user.id)
    lang = user[1] if user else 'ru'
    
    if not favorites:
        if lang == 'ru':
            text = "⭐ У вас нет избранных валютных пар\nНажмите 'Добавить пару' ниже"
        else:
            text = "⭐ You have no favorite currency pairs\nClick 'Add pair' below"
    else:
        if lang == 'ru':
            text = "⭐ *Ваши избранные валютные пары:*\n\nНажмите на пару для быстрой конвертации"
        else:
            text = "⭐ *Your favorite currency pairs:*\n\nClick on a pair for quick conversion"
    
    await message.answer(
        text,
        reply_markup=get_favorites_keyboard(favorites, lang),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "add_favorite")
async def add_favorite_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FavoriteStates.waiting_for_from)
    await callback.message.edit_text(
        "Выберите исходную валюту для добавления в избранное:",
        reply_markup=get_currency_keyboard(action="fav_from")
    )
    await callback.answer()

@router.callback_query(F.data.startswith("fav_from"))
async def process_fav_from(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split(":")[1]
    await state.update_data(from_currency=currency)
    await state.set_state(FavoriteStates.waiting_for_to)
    
    await callback.message.edit_text(
        f"Исходная валюта: {currency}\nТеперь выберите целевую валюту:",
        reply_markup=get_currency_keyboard(action="fav_to")
    )
    await callback.answer()

@router.callback_query(F.data.startswith("fav_to"))
async def process_fav_to(callback: types.CallbackQuery, state: FSMContext):
    db = get_db()  # Получаем базу данных
    
    to_currency = callback.data.split(":")[1]
    data = await state.get_data()
    from_currency = data.get('from_currency')
    
    # Добавляем в избранное
    await db.add_favorite(callback.from_user.id, from_currency, to_currency)
    
    await callback.message.edit_text(
        f"✅ Пара {from_currency} → {to_currency} добавлена в избранное!"
    )
    await state.clear()
    await callback.answer()

@router.callback_query(F.data.startswith("fav_convert"))
async def convert_from_favorite(callback: types.CallbackQuery, state: FSMContext):
    _, from_currency, to_currency = callback.data.split(":")
    await state.update_data(
        from_currency=from_currency,
        to_currency=to_currency
    )
    await state.set_state(ConvertStates.waiting_for_amount)
    
    await callback.message.edit_text(
        f"Быстрая конвертация: {from_currency} → {to_currency}\nВведите сумму:"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("fav_remove"))
async def remove_favorite(callback: types.CallbackQuery):
    db = get_db()  # Получаем базу данных
    
    _, from_currency, to_currency = callback.data.split(":")
    
    await db.remove_favorite(callback.from_user.id, from_currency, to_currency)
    
    await callback.message.edit_text(
        f"✅ Пара {from_currency} → {to_currency} удалена из избранного"
    )
    await callback.answer()