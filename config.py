import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем .env файл из текущей директории
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Для отладки - посмотрим, что загрузилось
print(f"Токен загружен: {'ДА' if os.getenv('BOT_TOKEN') else 'НЕТ'}")
print(f"API ключ загружен: {'ДА' if os.getenv('EXCHANGE_API_KEY') else 'НЕТ'}")

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")  # exchangerate-api.com
    EXCHANGE_API_URL = "https://v6.exchangerate-api.com/v6/"
    
    # Если токен не загружен, выводим ошибку
    if not BOT_TOKEN:
        print("❌ ВНИМАНИЕ: BOT_TOKEN не загружен из .env файла!")
        print("   Убедитесь, что файл .env существует и содержит BOT_TOKEN=ваш_токен")
    
    if not EXCHANGE_API_KEY:
        print("⚠️  ВНИМАНИЕ: EXCHANGE_API_KEY не загружен из .env файла!")
    
    # Поддерживаемые языки
    LANGUAGES = {
        'ru': 'Русский',
        'en': 'English'
    }
    
    # Коды валют для информации
    CURRENCY_INFO = {
        'AED': {'name': 'Дирхам ОАЭ', 'symbol': 'د.إ', 'country': 'ОАЭ'},
        'ARS': {'name': 'Аргентинское песо', 'symbol': '$', 'country': 'Аргентина'},
        'AUD': {'name': 'Австралийский доллар', 'symbol': 'A$', 'country': 'Австралия'},
        'AZN': {'name': 'Азербайджанский манат', 'symbol': '₼', 'country': 'Азербайджан'},
        'BGN': {'name': 'Болгарский лев', 'symbol': 'лв', 'country': 'Болгария'},
        'BRL': {'name': 'Бразильский реал', 'symbol': 'R$', 'country': 'Бразилия'},
        'BYN': {'name': 'Белорусский рубль', 'symbol': 'Br', 'country': 'Беларусь'},
        'CAD': {'name': 'Канадский доллар', 'symbol': 'C$', 'country': 'Канада'},
        'CHF': {'name': 'Швейцарский франк', 'symbol': 'Fr', 'country': 'Швейцария'},
        'CLP': {'name': 'Чилийское песо', 'symbol': '$', 'country': 'Чили'},
        'CNY': {'name': 'Китайский юань', 'symbol': '¥', 'country': 'Китай'},
        'CZK': {'name': 'Чешская крона', 'symbol': 'Kč', 'country': 'Чехия'},
        'DKK': {'name': 'Датская крона', 'symbol': 'kr', 'country': 'Дания'},
        'EGP': {'name': 'Египетский фунт', 'symbol': '£', 'country': 'Египет'},
        'EUR': {'name': 'Евро', 'symbol': '€', 'country': 'Еврозона'},
        'GBP': {'name': 'Фунт стерлингов', 'symbol': '£', 'country': 'Великобритания'},
        'GEL': {'name': 'Грузинский лари', 'symbol': '₾', 'country': 'Грузия'},
        'HKD': {'name': 'Гонконгский доллар', 'symbol': 'HK$', 'country': 'Гонконг'},
        'HUF': {'name': 'Венгерский форинт', 'symbol': 'Ft', 'country': 'Венгрия'},
        'IDR': {'name': 'Индонезийская рупия', 'symbol': 'Rp', 'country': 'Индонезия'},
        'ILS': {'name': 'Новый израильский шекель', 'symbol': '₪', 'country': 'Израиль'},
        'INR': {'name': 'Индийская рупия', 'symbol': '₹', 'country': 'Индия'},
        'JPY': {'name': 'Японская иена', 'symbol': '¥', 'country': 'Япония'},
        'KGS': {'name': 'Киргизский сом', 'symbol': 'с', 'country': 'Киргизия'},
        'KRW': {'name': 'Южнокорейская вона', 'symbol': '₩', 'country': 'Южная Корея'},
        'KZT': {'name': 'Казахстанский тенге', 'symbol': '₸', 'country': 'Казахстан'},
        'MDL': {'name': 'Молдавский лей', 'symbol': 'L', 'country': 'Молдова'},
        'MXN': {'name': 'Мексиканское песо', 'symbol': '$', 'country': 'Мексика'},
        'MYR': {'name': 'Малайзийский ринггит', 'symbol': 'RM', 'country': 'Малайзия'},
        'NOK': {'name': 'Норвежская крона', 'symbol': 'kr', 'country': 'Норвегия'},
        'NZD': {'name': 'Новозеландский доллар', 'symbol': 'NZ$', 'country': 'Новая Зеландия'},
        'PLN': {'name': 'Польский злотый', 'symbol': 'zł', 'country': 'Польша'},
        'QAR': {'name': 'Катарский риал', 'symbol': 'ر.ق', 'country': 'Катар'},
        'RON': {'name': 'Румынский лей', 'symbol': 'lei', 'country': 'Румыния'},
        'RSD': {'name': 'Сербский динар', 'symbol': 'дин', 'country': 'Сербия'},
        'RUB': {'name': 'Российский рубль', 'symbol': '₽', 'country': 'Россия'},
        'SAR': {'name': 'Саудовский риял', 'symbol': 'ر.س', 'country': 'Саудовская Аравия'},
        'SEK': {'name': 'Шведская крона', 'symbol': 'kr', 'country': 'Швеция'},
        'SGD': {'name': 'Сингапурский доллар', 'symbol': 'S$', 'country': 'Сингапур'},
        'THB': {'name': 'Тайский бат', 'symbol': '฿', 'country': 'Таиланд'},
        'TRY': {'name': 'Турецкая лира', 'symbol': '₺', 'country': 'Турция'},
        'TJS': {'name': 'Таджикский сомони', 'symbol': 'смн', 'country': 'Таджикистан'},
        'TMT': {'name': 'Туркменский манат', 'symbol': 'T', 'country': 'Туркменистан'},
        'UAH': {'name': 'Украинская гривна', 'symbol': '₴', 'country': 'Украина'},
        'USD': {'name': 'Доллар США', 'symbol': '$', 'country': 'США'},
        'UZS': {'name': 'Узбекский сум', 'symbol': 'сўм', 'country': 'Узбекистан'},
        'VND': {'name': 'Вьетнамский донг', 'symbol': '₫', 'country': 'Вьетнам'},
        'XAU': {'name': 'Тройская унция золота', 'symbol': 'XAU', 'country': 'Международный'},
        'ZAR': {'name': 'Южноафриканский рэнд', 'symbol': 'R', 'country': 'ЮАР'},
    }