import aiosqlite
from datetime import datetime

class Database:
    def __init__(self, db_path='data/database.db'):
        self.db_path = db_path
        
    async def create_tables(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Пользователи
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    language TEXT DEFAULT 'ru',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Избранные валюты пользователя
            await db.execute('''
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    from_currency TEXT,
                    to_currency TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # История конвертаций
            await db.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    from_currency TEXT,
                    to_currency TEXT,
                    amount REAL,
                    result REAL,
                    rate REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            await db.commit()
    
    # Методы для работы с пользователями
    async def get_user(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
                return await cursor.fetchone()
    
    async def add_user(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
            await db.commit()
    
    async def update_language(self, user_id, language):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
            await db.commit()
    
    # Методы для избранных валют
    async def get_favorites(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT from_currency, to_currency FROM favorites WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                return await cursor.fetchall()
    
    async def add_favorite(self, user_id, from_currency, to_currency):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT INTO favorites (user_id, from_currency, to_currency) VALUES (?, ?, ?)',
                (user_id, from_currency, to_currency)
            )
            await db.commit()
    
    async def remove_favorite(self, user_id, from_currency, to_currency):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'DELETE FROM favorites WHERE user_id = ? AND from_currency = ? AND to_currency = ?',
                (user_id, from_currency, to_currency)
            )
            await db.commit()
    
    # Методы для истории
    async def add_to_history(self, user_id, from_currency, to_currency, amount, result, rate):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                '''INSERT INTO history 
                   (user_id, from_currency, to_currency, amount, result, rate) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (user_id, from_currency, to_currency, amount, result, rate)
            )
            await db.commit()
    
    async def get_history(self, user_id, limit=10):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                '''SELECT from_currency, to_currency, amount, result, rate, timestamp 
                   FROM history WHERE user_id = ? 
                   ORDER BY timestamp DESC LIMIT ?''',
                (user_id, limit)
            ) as cursor:
                return await cursor.fetchall()