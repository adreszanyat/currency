from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from deps import get_db  # Импортируем из deps.py

router = Router()

@router.message(Command("history"))
@router.message(F.text.contains("История"))
@router.message(F.text.contains("History"))
async def cmd_history(message: types.Message):
    db = get_db()  # Получаем базу данных
    
    user = await db.get_user(message.from_user.id)
    lang = user[1] if user else 'ru'
    
    history = await db.get_history(message.from_user.id, limit=5)
    
    if not history:
        if lang == 'ru':
            text = "📭 Ваша история конвертаций пуста"
        else:
            text = "📭 Your conversion history is empty"
        await message.answer(text)
        return
    
    if lang == 'ru':
        text = "📈 *Последние 5 операций:*\n\n"
    else:
        text = "📈 *Last 5 operations:*\n\n"
    
    for record in history:
        from_curr, to_curr, amount, result, rate, timestamp = record
        
        if lang == 'ru':
            text += (
                f"🕐 {timestamp}\n"
                f"💰 {amount:.2f} {from_curr} → {result:.2f} {to_curr}\n"
                f"📊 Курс: 1 {from_curr} = {rate:.4f} {to_curr}\n"
                f"━━━━━━━━━━━━━━━\n\n"
            )
        else:
            text += (
                f"🕐 {timestamp}\n"
                f"💰 {amount:.2f} {from_curr} → {result:.2f} {to_curr}\n"
                f"📊 Rate: 1 {from_curr} = {rate:.4f} {to_curr}\n"
                f"━━━━━━━━━━━━━━━\n\n"
            )
    
    await message.answer(text, parse_mode="Markdown")