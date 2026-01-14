import aiohttp
from config import Config

async def get_exchange_rate(from_currency, to_currency):
    """Получение курса валюты с exchangerate-api.com"""
    try:
        url = f"{Config.EXCHANGE_API_URL}{Config.EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('conversion_rate')
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

async def convert_currency(amount, from_currency, to_currency):
    """Конвертация суммы"""
    rate = await get_exchange_rate(from_currency, to_currency)
    if rate:
        result = amount * rate
        return result, rate
    return None, None

def format_currency_info(currency_code, lang='ru'):
    """Форматирование информации о валюте"""
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

def format_history_record(record, lang='ru'):
    """Форматирование записи истории"""
    from_curr, to_curr, amount, result, rate, timestamp = record
    
    if lang == 'ru':
        return (
            f"🕐 {timestamp}\n"
            f"💰 {amount:.2f} {from_curr} → {result:.2f} {to_curr}\n"
            f"📊 Курс: 1 {from_curr} = {rate:.4f} {to_curr}\n"
            f"━━━━━━━━━━━━━━━"
        )
    else:
        return (
            f"🕐 {timestamp}\n"
            f"💰 {amount:.2f} {from_curr} → {result:.2f} {to_curr}\n"
            f"📊 Rate: 1 {from_curr} = {rate:.4f} {to_curr}\n"
            f"━━━━━━━━━━━━━━━"
        )