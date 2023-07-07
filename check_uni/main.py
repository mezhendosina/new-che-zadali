import asyncio

import config
from check_unis import CheckUnis


async def main():
    ch = CheckUnis(config.snils, config.snils_with_spacing)
    itmo = await ch.itmo()
    chelgu = await ch.chelgu()
    out = [itmo, chelgu]
    with open("unis", "w") as f:
        f.write("\n".join(out))


if __name__ == "__main__":
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(main())]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
