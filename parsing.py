import re


class Parsing:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.config = {'hubs': {}}
        self.message = ""

    def __read_file(self) -> str | None:
        if (not isinstance(self.file_name, str)):
            raise ValueError(f'Error: "{self.file_name}" Should Be String')
        with open(self.file_name) as file:
            return file.read()

    def __normalize_lines(self, lines: list[str]) -> list[str]:
        return [
            line.split("#")[0] for line in lines if line and not line.startswith("#")
            and not line.isspace()
        ]

    def __parse_nb_drones(self, line: str) -> bool:
        result = re.search(r"^\s*nb_drones\s*:\s*([0-9]+)\s*$", line)
        if (not result):
            raise ValueError("Error: line[1]")
        else:
            self.config.update({"nb_drones": int(result.group(1))})

    def __validte_set_hub(self, extracted_data : tuple) -> None:
        _, name, x, y, *metadata = extracted_data
        if name in self.config['hubs']:
            raise ValueError("Zone Name Duplicated")
        metadata = [{data.split("=")[0]: data.split('=')[-1]} for data in metadata if data]
        if len(metadata) != len(set(next(iter(data)) for data in metadata)):
            raise ValueError("Metadata Is Duplicated")
        for data in metadata:
            k, v = next(iter(data.items()))
            if k not in {'zone', 'color', 'max_drones'}:
                raise ValueError("Metadata Key Is Invalid")
            if k == 'zone':
                if v not in {'normal', 'blocked', 'restricted', 'priority'}:
                    raise ValueError("Type Zone Is Invalid")
            elif k == 'max_drones':
                if not re.search("^\d+$", v):
                    raise ValueError("max_drones Value Should Be Integer")
        self.config['hubs'].update({name: {'coor': (int(x), int(y)), 'zone': 'normal', 'max_drones': 1}})
        for data in  metadata:
            self.config['hubs'][name].update(data)

    def __parse_hubs_connections(self, lines: list[str]) -> None:
        start_exist = 0
        end_exist = 0
        for i, line in enumerate(lines, 1):
            hub_meta = r"\s+\[(?:\s*(\w+=\w+))(?:\s+(\w+=\w+))?(?:\s+(\w+=\w+))?\s*\]"
            connection_meta = r"\s+\[(?:\s*(max_link_capacity=\d+))\s*\]"
            hub_pattern = rf"^\s*(start_hub|hub|end_hub)\s*:\s*(\w+)\s+(\d+)\s+(\d+)(?:{hub_meta})?\s*$"
            connection_pattern = rf"^\s*connection\s*:\s*(\w+-\w+)(?:{connection_meta})?\s*$"
            hub = re.search(hub_pattern, line)
            connection = re.search(connection_pattern, line)
            if (not hub and not connection):
                raise ValueError("Error: Invalid Pattern")
            if (hub):
                hub_type, *_ = hub.groups()
                if (hub_type == "start_hub" or hub_type == "end_hub"):
                    if (hub_type == 'start_hub' and start_exist):
                        raise ValueError("Error: start_hub Key Is Duplicated")
                    elif (hub_type == 'start_hub' and not start_exist):
                        start_exist = 1
                    elif (hub_type == 'end_hub' and end_exist):
                        raise ValueError("Error: end_hub Key Is Duplicated")
                    else:
                        end_exist = 1
                self.__validte_set_hub(hub.groups())
            else:
                connection, *metadata = connection.groups()
        if (not start_exist or not end_exist):
            raise ValueError("Error: start_hub and end_hub are required")

    def parser(self) -> bool:
        content = self.__read_file()
        lines = content.split('\n')
        lines = self.__normalize_lines(lines)
        if (not lines):
            raise ValueError("Error: File is Empty")
        self.__parse_nb_drones(lines[0])
        self.__parse_hubs_connections(lines[1:])



def main() -> None:
    p = Parsing("config.txt")
    p.parser()
    print(*[data for data in p.config['hubs'].values()], sep="\n")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("Error: File Name Not Found")
    except PermissionError:
        print("Error: File Permission")
    except (Exception, KeyboardInterrupt):
        print("Error: Unexpected")
