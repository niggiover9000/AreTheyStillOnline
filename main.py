
from ping3 import ping, verbose_ping
from socket import gethostbyname, gethostname
import asyncio


async def find_self():
    try:
        return gethostbyname(gethostname())
    except RuntimeError as error:
        print(f"Could not read own IP. Are you root? {error}")
        return False


async def ping_target(ip):
    print(f"Trying to reach {ip}...")
    request = ping(ip, timeout=2)
    if request is False:
        return False
    else:
        print("Ping:", request)
        return True


async def main():
    task1 = asyncio.create_task(ping_target("2.10.100.1"))
    task2 = asyncio.create_task(ping_target("8.8.8.8"))
    await task1
    await task2

asyncio.run(main())

# asyncio.run(find_self())
# asyncio.run(ping_target("8.8.8.8"))
# asyncio.run(ping_target("2.10.100.1"))