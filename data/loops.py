import asyncio

from data.parser import parsing

loops = {}


class Loop:
    def __init__(self, user_id):
        self.user_id = user_id
        self._active = False
        self._stopped = True
        loops[self.user_id] = self

    @classmethod
    def get_loop(cls, user_id):
        return loops.get(user_id, cls(user_id))

    @property
    def is_running(self):
        return not self._stopped

    async def start(self):
        self._active = True
        asyncio.create_task(self._run_loop())

    async def _run_loop(self):
        while self._active:
            await parsing()
        self._stopped = True

    async def stop(self):
        self._active = False
        while not self._stopped:
            await asyncio.sleep(1)