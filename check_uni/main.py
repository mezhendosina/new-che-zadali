import asyncio

import config
from check_unis import CheckUnis


async def main():
    ch = CheckUnis(config.snils)
    itmo = await ch.itmo()
    with open("unis", "w") as f:
        f.write(itmo)


if __name__ == "__main__":
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(main())]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
