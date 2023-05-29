from bs4 import BeautifulSoup


def get_table():
	with open("propusk_leaders/leaders.txt", encoding="utf-8") as f:
		f = f.readlines()

		out_str = "Рейтинг отсутствующих\n"
		c = 1
		for i in f:
			if i != "\n":
				i = i.split(" ", 3)
				name = i[3].replace('\n', '')
				out_str += f"\n{c}. [{name}](t.me/{i[1]}) - {i[2]} "
				count_propusk = int(i[2])

				if count_propusk % 10 == 1:
					out_str += "пропуск"
				elif 2 <= count_propusk % 10 <= 4:
					out_str += "пропуска"
				else:
					out_str += "пропусков"
				c += 1

		return out_str


async def extract_propusk(f: str) -> int:
	c = 0
	soup = BeautifulSoup(f, features="lxml")

	table = soup.find_all("table", "table-print")[0]

	for tr_tags in table.find_all("tr")[2:]:
		td_tags = tr_tags.find_all("td")
		for i in td_tags[1:]:
			i = i.get_text()
			if i is not None:
				c += i.count("Б") + i.count("ОТ") + i.count("НП") + i.count("УП")
	return c


def save_propusk(name, user_id, username, count):
	form_str = f"{user_id} {username} {count} {name}"

	f = open("propusk_leaders/leaders.txt", "r", encoding="utf-8")
	f_read = f.read()

	file = f_read.split("\n")
	if str(user_id) not in f_read or (username not in f_read and username != "None"):
		position = -1
		for i in range(len(file) - 1):
			if int(file[i].split(" ")[2]) <= count:
				position = i
				break

		if position == -1:
			file.append(form_str)
		else:
			file.insert(position, form_str)
		f.close()
		with open("propusk_leaders/leaders.txt", "w", encoding="utf-8") as fw:
			fw.write("\n".join(file))
			fw.close()
	else:
		for i in range(len(file)):
			if str(user_id) in file[i] or (username in f_read and username != "None"):
				file.pop(i)
				f.close()
				with open("propusk_leaders/leaders.txt", "w", encoding="utf-8") as fw:
					fw.write("\n".join(file))

				save_propusk(name, user_id, username, count)
				break


