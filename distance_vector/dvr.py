import asyncio 
from main import main
from main import update_network_continuously
from utils.signal_handler import setup_signal_handler, get_stop_event
from distance_vector.poison_reverse import state_manager 

async def run_dvr(network, routers):
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

    print("Listening for changes in the config file...")

    post_poison_reverse = False 

    stop_event = get_stop_event()
    while not stop_event.is_set(): 
        await asyncio.sleep(1)
        updated, new_network = await asyncio.create_task(update_network_continuously(network, routers))
        network = new_network
        if updated or post_poison_reverse:
            post_poison_reverse = False 
            print("Change detected!")
            for router in routers.values():
                print(f"{router.id}: {router.vector}")
            
            tasks = []
            for router in routers.values():
                tasks.append(router.run_dvr(routers))
            await asyncio.gather(*tasks)

            # Trigger routers to run Bellman-Ford for auto-correction post poison reverse
            if state_manager.get_poison_reverse():
                state_manager.set_poison_reverse(False)
                post_poison_reverse = True

async def dvr_main():
    setup_signal_handler()
    network, routers = main()
    await run_dvr(network, routers)
    
if __name__ == "__main__":
    asyncio.run(dvr_main())
    