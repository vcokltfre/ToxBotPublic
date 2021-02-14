from asyncpg import create_pool
from asyncio import get_event_loop
from json import dumps, loads

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

    async def create_guild(self, guild: int, config: dict = None):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO Guilds (id, config) VALUES ($1, $2);", guild, dumps(config or self.default))
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