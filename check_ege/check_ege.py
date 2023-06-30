import aiohttp


def format_result(result):
    if result["HasResult"]:
        if result["IsComposition"]:
            return "зачет"
        else:
            return str(result["TestMark"])
    else:
        return "результата нет"


def format_results(json_r, new=False):
    out_str = "Обновление результатов ЕГЭ\n\n" if new else "Как @mezhendosina сдал ЕГЭ?\n\n"
    print(json_r)
    for i in json_r["Result"]["Exams"]:
        out_str += f"<b>{i['Subject']}</b> - <i>{format_result(i)}</i>\n"
    return out_str


class CheckEge:
    def __init__(self, token=None) -> None:
        self.session = aiohttp.ClientSession(
            "https://checkege.rustest.ru"
        )
        self.captcha = None
        self.token = token

    async def get_captcha(self):
        r = await self.session.get("/api/captcha")
        json_r = await r.json()
        self.captcha = json_r
        return json_r

    async def login(self, fio_hash, passport, captcha, region=74):
        if self.token is None:
            r = await self.session.post("/api/participant/login",
                                        data={
                                            "Hash": fio_hash,
                                            "Code": "",
                                            "Document": "000000" + passport,
                                            "Region": region,
                                            "AgereeCheck": "on",
                                            "Captcha": captcha,
                                            "Token": self.captcha["Token"],
                                            "reCaptureToken": captcha
                                        })
            self.token = r.cookies.get("Participant")

    async def get_exams(self, as_json=False):
        r = await self.session.get("/api/exam")
        json_r = await r.json()
        if as_json:
            return json_r
        else:
            return format_results(json_r)

    async def close(self):
        await self.session.close()
