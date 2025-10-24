import aiosqlite

DB_PATH = "database.db"


async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS managers
                         (
                             id       INTEGER PRIMARY KEY AUTOINCREMENT,
                             username TEXT NOT NULL
                         )""")

        await db.execute("""
                         CREATE TABLE IF NOT EXISTS users
                         (
                             id         INTEGER PRIMARY KEY AUTOINCREMENT,
                             tg_id      BIGINT NOT NULL,
                             manager_id INTEGER,
                             city       TEXT,
                             age        INTEGER,
                             FOREIGN KEY (manager_id) REFERENCES managers (id)
                         )""")

        await db.commit()
