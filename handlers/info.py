from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from config import Config

router = Router()

def format_currency_info(currency_code, lang='ru'):
    if currency_code not in Config.CURRENCY_INFO:
        return None
    
    info = Config.CURRENCY_INFO[currency_code]
    
    if lang == 'ru':
        return (
            f"💱 **{currency_code}** - {info['name']}\n"
            f"📌 **Символ:** {info['symbol']}\n"
            f"🌍 **Страна:** {info['country']}\n"
            f"🔢 **Код ISO:** {currency_code}"
        )
    else:
        return (
            f"💱 **{currency_code}** - {info['name']}\n"
            f"📌 **Symbol:** {info['symbol']}\n"
            f"🌍 **Country:** {info['country']}\n"
            f"🔢 **ISO Code:** {currency_code}"
        )

@router.message(Command("info"))
@router.message(F.text.contains("Информация о валютах"))
@router.message(F.text.contains("Currency Info"))
async def cmd_info(message: types.Message):
    from deps import get_db
    
    user = await get_db.get_user(message.from_user.id)
    lang = user[1] if user else 'ru'
    
    if lang == 'ru':
        text = "ℹ️ *Информация о валютах*\n\nДоступные валюты:\n"
    else:
        text = "ℹ️ *Currency Information*\n\nAvailable currencies:\n"
    
    for currency_code in Config.CURRENCY_INFO.keys():
        text += f"• {currency_code}\n"
    
    if lang == 'ru':
        text += "\nИспользуйте: /info [код валюты]\nНапример: /info USD"
    else:
        text += "\nUse: /info [currency code]\nExample: /info USD"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("info"))
async def cmd_currency_info(message: types.Message):
    from deps import get_db
    
    parts = message.text.split()
    if len(parts) == 2:
        currency_code = parts[1].upper()
        user = await get_db.get_user(message.from_user.id)
        lang = user[1] if user else 'ru'
        
        info = format_currency_info(currency_code, lang)
        
        if info:
            await message.answer(info, parse_mode="Markdown")
        else:
            if lang == 'ru':
                await message.answer(f"Валюта {currency_code} не найдена. Используйте код из списка: /info")
            else:
                await message.answer(f"Currency {currency_code} not found. Use a code from the list: /info")