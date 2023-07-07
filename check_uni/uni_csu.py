import asyncio
import datetime

import aiohttp
import pytz
from bs4 import BeautifulSoup

from check_uni.ProgramEntity import ProgramEntity
from check_uni.StudentEntity import StudentEntity


class CSU:
    def __init__(self, snils, user_agent):
        self.snils = snils
        self.client = aiohttp.ClientSession(
            "https://abit.csu.ru",
            headers={"User-Agent": "csu " + user_agent, "Referer": "https://abit.csu.ru/contest/"}
        )

    async def get_res(self, program: tuple) -> ProgramEntity:
        params = [
            ("level", 3), ("faculty", program[0]), ("form", 2), ("direction", program[1]), ("payment", "budget"),
            ("type", "all")
        ]
        await self.client.request("get", "/contest/", ssl=False)
        request = await self.client.request("get", "/api/contest.php", params=params, ssl=False)
        response = await request.text()
        return self._extract_programs(response)

    def _extract_programs(self, html: str) -> ProgramEntity:
        soup = BeautifulSoup(html, features="lxml")
        tables = soup.find_all("div", class_="table-scroll")
        rating_table = tables[-1]
        out = []
        for i in rating_table.find_all("tr")[1:]:
            td = i.find_all("td")
            out.append(StudentEntity(td[1].text, int(td[2].text), True))

        head_table = tables[0].find("table").find_all("tr")
        program_name = self._delete_spacing(head_table[1].find_all("td")[1].text \
                                            .replace("\n                        ", "").replace("\n                    ",
                                                                                               ""))
        return ProgramEntity(
            program_name,
            int(head_table[-1].find_all("td")[1].find_all("p")[0].text.split("-")[-1]),
            datetime.datetime.now(tz=pytz.timezone('Asia/Yekaterinburg')).strftime("%H:%M"),
            out
        )

    def _delete_spacing(self, s):
        while not s[0].isalpha():
            s = s[1:]
        while not s[-1].isalpha():
            s = s[:-1]
        return s

    async def close(self):
        await self.client.close()
