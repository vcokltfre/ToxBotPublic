from aiohttp import ClientSession


class HTTPClient:
    def __init__(self, config: dict):
        self.headers = {"Authorization": config["token"]}
        self.url = config["api"]

        self.sess = ClientSession(headers=self.headers)

    async def ensure(self):
        if self.sess.closed:
            self.sess = ClientSession(headers=self.headers)

    async def request(self, text: str):
        async with self.sess.post(self.url, json={"text":text}) as resp:
            return await resp.json()
