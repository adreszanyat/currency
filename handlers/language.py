from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import get_main_keyboard, get_language_keyboard
from database import Database

router = Router()

@router.message(Command("lang"))
@router.message(F.text.contains("Язык"))
@router.message(F.text.contains("Language"))
async def cmd_language(message: types.Message):
    text = "🌍 *Выберите язык / Choose language:*"
    await message.answer(text, reply_markup=get_language_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: types.CallbackQuery, db: Database):
    language = callback.data.split(":")[1]
    
    await db.update_language(callback.from_user.id, language)
    
    if language == 'ru':
        text = "✅ Язык изменен на Русский"
    else:
        text = "✅ Language changed to English"
    
    await callback.message.edit_text(text)
    
    # Обновляем клавиатуру
    await callback.message.answer(
        "Главное меню / Main menu:",
        reply_markup=get_main_keyboard(language)
    )
    await callback.answer()