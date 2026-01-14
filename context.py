# context.py
"""Хранилище глобальных зависимостей"""

class Context:
    _db = None
    
    @classmethod
    def set_db(cls, database):
        cls._db = database
    
    @classmethod
    def get_db(cls):
        return cls._db