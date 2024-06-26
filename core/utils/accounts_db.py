import aiosqlite
import asyncio

class AccountsDB:
    def __init__(self, db_path):
        self.db_path = db_path

        self.cursor = None
        self.connection = None

        self.db_lock = asyncio.Lock()

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_path)
        self.cursor = await self.connection.cursor()
        await self.create_tables()

    async def create_tables(self):
        await self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL,
        proxies TEXT NOT NULL
        )
        ''')

        await self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProxyList (
        id INTEGER PRIMARY KEY,
        proxy TEXT NOT NULL
        )
        ''')

        await self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS PointStats (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL,
        points TEXT NOT NULL
        )
        ''')
        await self.connection.commit()

    async def add_account(self, email, new_proxy):
        async with self.db_lock:
            await self.cursor.execute("SELECT proxies FROM Accounts WHERE email=?", (email,))
            existing_proxies = await self.cursor.fetchone()
        if existing_proxies:
            existing_proxies = existing_proxies[0].split(",")
            if new_proxy not in existing_proxies:
                if new_proxy is None:
                    return False
                updated_proxies = ",".join(existing_proxies + [new_proxy])
                async with self.db_lock:
                    await self.cursor.execute("UPDATE Accounts SET proxies=? WHERE email=?", (updated_proxies, email))
                    await self.connection.commit()
        else:
            async with self.db_lock:
                # Email not found, create new entry
                await self.cursor.execute("INSERT INTO Accounts(email, proxies) VALUES(?, ?)", (email, new_proxy))
                await self.connection.commit()

    async def proxies_exist(self, proxy):
        async with self.db_lock:
            await self.cursor.execute("SELECT email, proxies FROM Accounts")
            rows = await self.cursor.fetchall()
        for row in rows:
            if len(row) > 1:
                email = row[0]
                existing_proxies = row[1].split(",")
                if proxy in existing_proxies:
                    return email
        return False

    async def update_or_create_point_stat(self, user_id, email, points):
        async with self.db_lock:
            await self.cursor.execute("SELECT * FROM PointStats WHERE id = ?", (user_id,))
            existing_user = await self.cursor.fetchone()

            if existing_user:
                await self.cursor.execute("UPDATE PointStats SET email = ?, points = ? WHERE id = ?",
                                          (email, points, user_id))
            else:
                await self.cursor.execute("INSERT INTO PointStats(id, email, points) VALUES (?, ?, ?)",
                                          (user_id, email, points))

            await self.connection.commit()

    async def get_total_points(self):
        async with self.db_lock:
            await self.cursor.execute(
                'SELECT SUM(CAST(points AS INTEGER)) '
                'FROM (SELECT email, MAX(CAST(points AS INTEGER)) as points '
                'FROM PointStats WHERE points NOT LIKE "%[^0-9]%" '
                'GROUP BY email)')
            result = await self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0

    async def get_proxies_by_email(self, email):
        async with self.db_lock:
            await self.cursor.execute("SELECT proxies FROM Accounts WHERE email=?", (email,))
            row = await self.cursor.fetchone()
        if row:
            proxies = row[0].split(",")
            return proxies
        return []

    async def get_new_from_extra_proxies(self, table="ProxyList"):
        # logger.info(f"Getting new proxy from {table}...")
        async with self.db_lock:
            await self.cursor.execute(f"SELECT proxy FROM {table} ORDER BY id DESC LIMIT 1")
            proxy = await self.cursor.fetchone()
        # logger.info(f"Extra proxy: {proxy}")
        if proxy and len(proxy) == 1:
            await self.cursor.execute(f"DELETE FROM {table} WHERE proxy=?", proxy)
            await self.connection.commit()
            return proxy[0]
        else:
            return None

    async def push_extra_proxies(self, proxies):
        async with self.db_lock:
            await self.cursor.executemany("INSERT INTO ProxyList(proxy) VALUES(?)", [(proxy,) for proxy in proxies])
            await self.connection.commit()

    async def delete_all_from_extra_proxies(self):
        async with self.db_lock:
            await self.cursor.execute("DELETE FROM ProxyList")
            await self.connection.commit()

    async def close_connection(self):
        await self.connection.close()
