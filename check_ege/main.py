import asyncio
import os

import aiohttp

from check_ege import CheckEge, format_results

# tg_token = os.getenv("TELEGRAM_API_TOKEN")
tg_token = "1950280557:AAGgeci2kr0knTa2S6yLTckFHMvixT37Z2E"

async def main():
    with open("token") as f:
        token = f.read()

    che = CheckEge(token)
    try:
        ex = await che.get_exams(True)
        with open("mezhendosinas_ege.json") as f:
            old_ex = f.read()

        if ex != old_ex:
            print("send new results")
            res = format_results(ex, True)
            print(res)
            async with aiohttp.ClientSession() as session:
                 r = await session.post(    
                    f"https://api.telegram.org/bot{tg_token}/sendMessage",
                    json={
                    "chat_id": 401311369,
                    "text": res
                })
                 print(r.text)
            with open("mezhendosinas_ege.json", "w") as f:
                f.write(ex)
        else:
            print("without changes")
    except Exception as e:
        print(e)
    finally:
        await che.close()


if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(main())]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
