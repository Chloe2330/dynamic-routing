import asyncio
from main import main
from main import update_network_continuously

async def run_dvr():
    network, routers = main()

    print("Initial routing state")
    for router in routers.values():
        print(f"{router.id}: {router.vector}")

    tasks = []
    for router in routers.values():
        tasks.append(router.run_dvr(routers))

    await asyncio.gather(*tasks)

    print("Routing state after initial convergence")
    for router in routers.values():
        print(f"{router.id}: {router.vector}")

    while True: 
        print("Listening for changes in the config file...")
        await asyncio.sleep(10)
        updated, new_network = await asyncio.create_task(update_network_continuously(network, routers))
        network = new_network
        if updated:
            print("Change detected!")
            
            tasks = []
            for router in routers.values():
                tasks.append(router.run_dvr(routers))
            await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    asyncio.run(run_dvr())
    