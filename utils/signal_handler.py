import signal
import asyncio

stop_event = asyncio.Event()

def signal_handler():
    print("Gracefully shutting down...")
    stop_event.set()

def setup_signal_handler():
    signal.signal(signal.SIGINT, lambda s, f: signal_handler())

def get_stop_event(): 
    return stop_event 
