from asyncpg import create_pool
from asyncio import get_event_loop
from json import dumps, loads
from time import time

with open("./static/init.sql") as f:
    initscript = f.read()


class DatabaseInterface:
    def __init__(self, config: dict, default_guild_config: dict):
        self.creds = {
            "user": config.get("DB_USER", "root"),
            "password": config.get("DB_PASS", "password"),
            "database": config.get("DB_DATABASE", "toxbot"),
            "host": config.get("DB_HOST", "127.0.0.1"),
        }

        self.default = default_guild_config

        get_event_loop().create_task(self.init())

        self.confcache = {}
        self.guildreqs = {}

    async def hardreset(self):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DROP TABLE Infractions; DROP TABLE Guilds;"
            )
        self.pool = None
        self.confcache = {}
        await self.init()

    async def init(self):
        self.pool = await create_pool(**self.creds)

        async with self.pool.acquire() as conn:
            await conn.execute(initscript)

        await self.get_all_guild_requests()

    async def create_guild(self, guild: int, config: dict = None):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO Guilds (id, config, lastreset) VALUES ($1, $2, $3);", guild, dumps(config or self.default), round(time()))
            self.confcache[guild] = config
            return True
        except Exception as e:
            print(e)
            return False

    async def get_guild(self, guild: int):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM Guilds WHERE id = $1;", guild)

    async def delete_guild(self, guild: int):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM Guilds WHERE id = $1;", guild)

    async def get_guild_config(self, guild: int):
        if guild in self.confcache:
            return self.confcache[guild]

        data = await self.get_guild(guild)

        if not data:
            self.confcache[guild] = None
            return None

        d = loads(data[1])
        self.confcache[guild] = d
        return d

    async def set_guild_config(self, guild: int, config: dict):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE Guilds SET config = $1 WHERE id = $2", dumps(config), guild)

        self.confcache[guild] = config

    async def reset_guild_config(self, guild: int):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE Guilds SET config = $1 WHERE id = $2", dumps(self.default), guild)

        self.confcache[guild] = self.deafult

    async def get_all_guild_requests(self):
        async with self.pool.acquire() as conn:
            results = await conn.fetch("SELECT (id, daily, today, lastreset) FROM Guilds;")

        for result in results:
            result = result[0]
            self.guildreqs[result[0]] = {
                "limit": result[1],
                "today": result[2],
                "reset": result[3]
            }

    async def reset_requests(self):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE Guilds SET today = 0, lastreset = $1 WHERE lastreset < $1;", round(time() - 86400))

        await self.get_all_guild_requests()

    async def add_request(self, guild: int):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE Guilds SET today = today + 1 WHERE id = $1;", guild)

        self.guildreqs[guild]["today"] += 1
