import aiosqlite


class AccountsDB:
    def __init__(self, db_path):
        self.db_path = db_path

        self.cursor = None
        self.connection = None

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
        await self.connection.commit()

    async def add_account(self, email, new_proxy):
        await self.cursor.execute("SELECT proxies FROM Accounts WHERE email=?", (email,))
        existing_proxies = await self.cursor.fetchone()
        if existing_proxies:
            existing_proxies = existing_proxies[0].split(",")
            if new_proxy not in existing_proxies:
                if new_proxy is None:
                    return False
                updated_proxies = ",".join(existing_proxies + [new_proxy])
                await self.cursor.execute("UPDATE Accounts SET proxies=? WHERE email=?", (updated_proxies, email))
        else:
            # Email not found, create new entry
            await self.cursor.execute("INSERT INTO Accounts(email, proxies) VALUES(?, ?)", (email, new_proxy))
        await self.connection.commit()

    async def proxies_exist(self, proxy):
        await self.cursor.execute("SELECT email, proxies FROM Accounts")
        rows = await self.cursor.fetchall()
        for row in rows:
            email = row[0]
            existing_proxies = row[1].split(",")
            if proxy in existing_proxies:
                return email
        return False

    async def get_proxies_by_email(self, email):
        await self.cursor.execute("SELECT proxies FROM Accounts WHERE email=?", (email,))
        row = await self.cursor.fetchone()
        if row:
            proxies = row[0].split(",")
            return proxies
        return []

    async def get_new_from_extra_proxies(self, table="ProxyList"):
        await self.cursor.execute(f"SELECT proxy FROM {table} ORDER BY id DESC LIMIT 1")
        proxy = await self.cursor.fetchone()
        if proxy:
            await self.cursor.execute(f"DELETE FROM {table} WHERE proxy=?", proxy)
            await self.connection.commit()
            return proxy[0]
        else:
            return None

    async def push_extra_proxies(self, proxies):
        await self.cursor.executemany("INSERT INTO ProxyList(proxy) VALUES(?)", [(proxy,) for proxy in proxies])
        await self.connection.commit()

    async def delete_all_from_extra_proxies(self):
        await self.cursor.execute("DELETE FROM ProxyList")
        await self.connection.commit()

    async def close_connection(self):
        await self.connection.close()
