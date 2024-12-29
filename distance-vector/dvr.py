import asyncio
from main import main

async def run_dvr():
    routers = main()

    print("Initial routing state")
    for router in routers.values():
        print(f"{router.id}: {router.vector}")

    tasks = []
    for router in routers.values():
        tasks.append(router.run_dvr(routers))

    await asyncio.gather(*tasks)

    print("Final routing state")
    for router in routers.values():
        print(f"{router.id}: {router.vector}")
    
if __name__ == "__main__":
    asyncio.run(run_dvr())
    