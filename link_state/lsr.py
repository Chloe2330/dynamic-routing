import asyncio 
from main import main
from main import update_network_continuously
from utils.signal_handler import setup_signal_handler, get_stop_event

async def run_lsr(network, routers):

    print("Initial routing state")
    for router in routers.values():
        print(f"{router.id}: {router.vector}")

    tasks = []
    for router in routers.values():
        tasks.append(router.run_lsr(network, routers))

    await asyncio.gather(*tasks)

    print("Routing state after initial convergence")
    for router in routers.values():
        print(f"{router.id}: {router.vector}")

    print("Listening for changes in the config file...")

    stop_event = get_stop_event()
    while not stop_event.is_set(): 
        await asyncio.sleep(1)
        updated, new_network = await asyncio.create_task(update_network_continuously(network, routers, False))
        network = new_network
        if updated:
            print("Change detected!")
            for router in routers.values():
                print(f"{router.id}: {router.vector}")
            
            tasks = []
            for router in routers.values():
                tasks.append(router.run_lsr(network, routers))
            await asyncio.gather(*tasks)

async def lsr_main():
    setup_signal_handler()
    network, routers = main()
    await run_lsr(network, routers)
    
if __name__ == "__main__":
    asyncio.run(lsr_main())
    