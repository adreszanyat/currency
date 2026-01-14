# deps.py
"""Получение зависимостей для handler'ов"""
from context import Context

def get_db():
    """Получить экземпляр базы данных"""
    db = Context.get_db()
    if db is None:
        # Попробуем получить из main
        try:
            from main import get_db as main_get_db
            return main_get_db()
        except ImportError:
            raise RuntimeError("База данных не инициализирована. Пожалуйста, сначала запустите бота.")
    return db