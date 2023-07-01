import config
from StudentEntity import StudentEntity
from itmo_requests import Itmo


class CheckUnis:
    def __init__(self, snils, user_agent=config.user_agent):
        self.snils = snils
        self.user_agent = user_agent

    async def itmo(self) -> str:
        c = Itmo(self.snils, self.user_agent)
        out = "*iTMO*\n"
        for program_id in config.itmo_programs:
            request = await c.get_res(program_id)
            place = self._get_place(request.peoples)
            admitted = "✅" if request.count >= place else "❌"

            out += f"{admitted} _{request.name}({request.date})_ - {str(place)}/{str(request.count)}/{len(request.peoples)}\n"
        await c.close()
        return out

    def _get_place(self, students: list) -> int:
        for i in range(len(students)):
            if students[i].snils == self.snils:
                return i + 1
        return -1
