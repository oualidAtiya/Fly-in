import re


class Parsing:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.config = {'hubs': {}}
        self.message = ""

    def __read_file(self) -> str | None:
        if (not isinstance(self.file_name, str)):
            self.message = f'Error: "{self.file_name}" Should Be String'
            return None
        try:
            with open(self.file_name) as file:
                return file.read()
        except FileNotFoundError:
            self.message = f'Error: "{self.file_name}" Not Found'
            return None

    def __normalize_lines(self, lines: list[str]) -> list[str]:
        return [
            line.split("#")[0] for line in lines if line and not line.startswith("#")
            and not line.isspace()
        ]

    def __parse_nb_drones(self, line: str) -> bool:
        result = re.search(r"^\s*nb_drones\s*:\s*([0-9]+)\s*$", line)
        if (not result):
            self.message = ('Error: line[1]')
            return False
        else:
            self.config.update({"nb_drones": int(result.group(1))})
        return True

    def __parse_hubs_connections(self, lines) -> bool:
        is_error = False
        for i, line in enumerate(lines, 1):
            hub_meta = r"\s+\[(?:\s*(\w+=\w+))(?:\s+(\w+=\w+))?(?:\s+(\w+=\w+))?\s*\]"
            connection_meta = r"\s+\[(?:\s*(max_link_capacity=\d+))\s*\]"
            hub_pattern = rf"^\s*(?:start_hub|hub|end_hub)\s*:\s*(\w+)\s+(\d+)\s+(\d+)(?:{hub_meta})?\s*$"
            connection_pattern = rf"^\s*connection\s*:\s*(\w+-\w+)(?:{connection_meta})?\s*$"
            hub = re.search(hub_pattern, line)
            connection = re.search(connection_pattern, line)
            if (not hub and not connection):
                is_error = True
                break
            if (hub):
                name, x, y, *metadata = hub.groups()
                if name in self.config['hubs']:
                    is_error = True
                    break
                metadata = [{data.split("=")[0]: data.split('=')[-1]} for data in metadata if data]
                if len(metadata) != len(set(next(iter(data)) for data in metadata)):
                    is_error = True
                    break
                for data in metadata:
                    k, v = next(iter(data.items()))
                    if k not in {'zone', 'color', 'max_drones'}:
                        self.message = (f'Error: line[{i+1}]')
                        return False
                    if k == 'zone':
                        if v not in {'normal', 'blocked', 'restricted', 'priority'}:
                            self.message = (f'Error: line[{i+1}]')
                            return False
                    elif k == 'max_drones':
                        if not re.search("^\d+$", v):
                            self.message = (f'Error: line[{i+1}]')
                            return False
                self.config['hubs'].update({name: {'coor': (int(x), int(y))}})
                for data in  metadata:
                    self.config['hubs'][name].update(data)
            else:
                connection, *metadata = connection.groups()

        if (not is_error):
            return True
        self.message = (f'Error: line[{i+1}]')
        return False

    def parser(self) -> bool:
        content = self.__read_file()
        lines = content.split('\n')
        lines = self.__normalize_lines(lines)
        if (lines and not self.__parse_nb_drones(lines[0])):
            return False

        self.__parse_hubs_connections(lines[1:])


p = Parsing("config.txt")
p.parser()
print(p.message)
for k, v in p.config['hubs'].items():
    print(f"{k}: {v}")
