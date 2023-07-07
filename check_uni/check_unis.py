import config
from StudentEntity import StudentEntity
from check_uni.ProgramEntity import ProgramEntity
from check_uni.uni_csu import CSU
from uni_itmo import Itmo


class CheckUnis:
    def __init__(self, snils, snils_with_spacing, user_agent=config.user_agent):
        self.snils = snils
        self.snils_with_spacing = snils_with_spacing
        self.user_agent = user_agent

    async def itmo(self) -> str:
        c = Itmo(self.snils, self.user_agent)
        out = "*iTMO*\n"
        for program_id in config.itmo_programs:
            request = await c.get_res(program_id)
            out += self._format_str(request)
        await c.close()
        return out

    async def chelgu(self) -> str:
        c = CSU(self.snils_with_spacing, self.user_agent)
        out = "*ЧелГУ*\n"
        for program in config.chelgu_programs:
            request = await c.get_res(program)
            out += self._format_str(request)
        await c.close()
        return out

    def _format_str(self, program_entity: ProgramEntity) -> str:
        place = self._get_place(program_entity.peoples)
        if place != -1:
            admitted = "✅" if program_entity.count >= place else "❌"
            return f"{admitted} _{program_entity.name}({program_entity.date})_ - {str(place)}/{str(program_entity.count)}/{len(program_entity.peoples)}\n"
        else:
            return f"_{program_entity.name}({program_entity.date})_ - нет в рейтинге\n"

    def _get_place(self, students: list, snils_with_spacing=False) -> int:
        for i in range(len(students)):
            if snils_with_spacing:
                if students[i].snils == self.snils_with_spacing:
                    return i + 1
            else:
                if students[i].snils == self.snils:
                    return i + 1
        return -1
