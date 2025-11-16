import asyncio
import aiohttp
import time

URL = "https://dbdata4life.genomas.cl"
CONCURRENCIA = 200   # número de peticiones simultáneas

async def request(session):
    async with session.get(URL) as response:
        return await response.text()

async def run_test():
    async with aiohttp.ClientSession() as session:
        tasks = [request(session) for _ in range(CONCURRENCIA)]
        start = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end = time.time()

        ex = sum(1 for r in results if isinstance(r, Exception))
        ok = CONCURRENCIA - ex

        print(f"✔ OK: {ok} | ❌ Errores: {ex}")
        print(f"⏱ Tiempo total: {end - start:.2f}s")
        print(f"🚀 RPS aproximado: {ok / (end - start):.2f}")

asyncio.run(run_test())
