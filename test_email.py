import asyncio
from iris.collectors.email import EmailCollector

from iris.db import cache

async def main():
    cache.init_db()
    col = EmailCollector()
    res = await col.collect("subhadip.sec@gmail.com")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
