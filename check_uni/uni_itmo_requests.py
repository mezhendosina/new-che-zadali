import datetime

import aiohttp

from ProgramEntity import ProgramEntity
from StudentEntity import StudentEntity


class Itmo:
    def __init__(self, snils, user_agent):
        self.snils = snils
        self.client = aiohttp.ClientSession(
            "https://abitlk.itmo.ru",
            headers={"User-Agent": "iTMO " + user_agent}
        )

    async def get_res(self, program_id: int) -> ProgramEntity:
        params = [("program_id", str(program_id)), ("manager_key", ""), ("sort", ""), ("showLosers", "true")]
        request = await self.client.get("/api/v1/rating/bachelor/budget", params=params)
        response = await request.json()
        response = response["result"]

        out = []
        for i in response["without_entry_tests"]:
            out.append(StudentEntity(i["snils"], -1))

        for i in response["by_unusual_quota"]:
            out.append(StudentEntity(i["snils"], i["total_scores"]))

        for i in response["by_special_quota"]:
            out.append(StudentEntity(i["snils"], i["total_scores"]))

        for i in response["by_target_quota"]:
            out.append(StudentEntity(i["snils"], i["total_scores"]))

        for i in response["general_competition"]:
            out.append(StudentEntity(i["snils"], i["total_scores"], True))
        update_time = datetime.datetime.strptime(response["update_time"], "%Y-%m-%dT%X%z") + datetime.timedelta(hours=2)
        return ProgramEntity(
            response["direction"]["program_title"],
            response["direction"]["budget_min"],
            update_time.strftime("%H:%M"),
            out
        )

    async def close(self):
        await self.client.close()
