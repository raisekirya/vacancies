import aiosqlite

from database.database import DB_PATH


async def get_user_by_tg_id(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,)) as cursor:
            return await cursor.fetchone()


async def create_user(tg_id: int, manager_id: int, city: str, age: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
                         INSERT INTO users (tg_id, manager_id, city, age)
                         VALUES (?, ?, ?, ?)''', (tg_id, manager_id, city, age))
        await db.commit()


async def get_all_managers():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT * FROM managers') as cursor:
            return await cursor.fetchall()


async def get_manager_by_id(manager_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM managers WHERE id = ?", (manager_id,)) as cursor:
            return await cursor.fetchone()


async def get_managers_count():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT COUNT(*) FROM managers') as cursor:
            count = await cursor.fetchone()

    return count[0]


async def create_manager(username: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('INSERT INTO managers (username) VALUES (?)', (username,))
        await db.commit()


async def delete_manager(manager_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('DELETE FROM managers WHERE id = ?', (manager_id,))
        await db.commit()
