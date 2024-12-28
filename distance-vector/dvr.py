import asyncio
from main import main

async def run_dvr():
    routers = main()

    for router in routers.values():
        print(f"{router.id}: {router.vector}")

    tasks = []
    for router in routers.values():
        tasks.append(router.dvr(routers))

    await asyncio.gather(*tasks)

    for router in routers.values():
        print(f"{router.id}: {router.vector}")
    
if __name__ == "__main__":
    asyncio.run(run_dvr())
    