import sys
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from database import Database
from context import Context  # Импортируем Context

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальная переменная для базы данных
db_instance = None

async def main():
    global db_instance
    
    # Инициализация базы данных
    db_instance = Database()
    await db_instance.create_tables()
    
    # Сохраняем базу данных в контекст
    Context.set_db(db_instance)
    
    # Инициализация бота и диспетчера
    bot = Bot(token=Config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Ручной импорт handler'ов
    from handlers.start import router as start_router
    from handlers.convert import router as convert_router
    from handlers.history import router as history_router
    from handlers.favorites import router as favorites_router
    from handlers.calc import router as calc_router
    from handlers.info import router as info_router
    from handlers.tips import router as tips_router
    from handlers.language import router as language_router
    
    # Подключение всех роутеров
    dp.include_router(start_router)
    dp.include_router(convert_router)
    dp.include_router(history_router)
    dp.include_router(favorites_router)
    dp.include_router(calc_router)
    dp.include_router(info_router)
    dp.include_router(tips_router)
    dp.include_router(language_router)
    
    # Запуск бота
    await dp.start_polling(bot)

def get_db():
    """Функция для получения экземпляра базы данных из других модулей"""
    global db_instance
    return db_instance

if __name__ == '__main__':
    asyncio.run(main())