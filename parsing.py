import re


class Parsing:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.config = {'hubs': {}, 'connections': {}}
        self.message = ""

    def __read_file(self) -> str | None:
        if (not isinstance(self.file_name, str)): #i think this will useless when start take it from argv
            raise ValueError(f'Error: "{self.file_name}" Should Be String')
        with open(self.file_name) as file:
            return file.read()

    def __normalize_lines(self, lines: list[str]) -> list[str]:
        n_lines = []
        for i, line in enumerate(lines, 1):
            if line and not line.startswith("#") and not line.isspace():
                n_lines.append((i, line))
        return n_lines

    def __parse_nb_drones(self, line: tuple[int, str]) -> bool:
        result = re.search(r"^\s*nb_drones\s*:\s*(\+?[1-9]+)\s*$", line[1])
        if (not result):
            raise ValueError(f'Error: Line[{line[0]}] is Invalid')
        else:
            self.config.update({"nb_drones": int(result.group(1))})

    def __validte_set_hub(self, extracted_data : tuple) -> None:
        hub_type, name, x, y, *metadata = extracted_data
        if name in self.config['hubs']:
            raise ValueError(f"Zone Name Duplicated")
        coordinates = set(coor['coor'] for coor in self.config['hubs'].values())
        if (int(x), int(y)) in coordinates:
            raise ValueError(f"Duplicated Coordinates")
        metadata = [{data.split("=")[0]: data.split('=')[-1]} for data in metadata if data]
        if len(metadata) != len(set(next(iter(data)) for data in metadata)):
            raise ValueError("Metadata Key Is Duplicated")
        for data in metadata:
            k, v = next(iter(data.items()))
            if k not in {'zone', 'color', 'max_drones'}:
                raise ValueError("Metadata Key Is Invalid")
            if k == 'zone':
                if v not in {'normal', 'blocked', 'restricted', 'priority'}:
                    raise ValueError("Type Zone Is Invalid")
                if hub_type == "start_hub" or hub_type == "end_hub":
                    if (v == 'blocked'):
                        raise ValueError("start_hub and end_hub Should Not Have Zone Blocked")
            elif k == 'max_drones':
                if not re.search(r"^[-+]?\d+$", v):
                    raise ValueError("max_drones Value Should Be Integer")
            else:
                pass # Validate Color Later With Help of  package Youssef told me

        self.config['hubs'].update({name: {'coor': (int(x), int(y)), 'zone': 'normal', 'max_drones': 1, 'color': None}})
        for data in  metadata:
            k, v = next(iter(data.items()))
            if k == "max_drones":
                k, v = next(iter({k: int(v)}.items()))
                if v < 0:
                    raise ValueError("max_drones Value Should Be Positive")
            else:
                self.config['hubs'][name].update(data)

    def __parse_hubs_connections(self, lines: list[(int, str)]) -> None:
        start_exist = 0
        end_exist = 0
        connection_exist = 0
        for line in lines:
            hub_meta = r"\s+\[(?:\s*(\w+=[-+]?\w+))(?:\s+(\w+=[-+]?\w+))?(?:\s+(\w+=[-+]?\w+))?\s*\]"
            connection_meta = r"\s+\[(?:\s*(max_link_capacity=\+?\d+))\s*\]"
            hub_pattern = rf"^\s*(start_hub|hub|end_hub)\s*:\s*(\w+)\s+([-+]?\d+)\s+([-+]?\d+)(?:{hub_meta})?\s*$"
            connection_pattern = rf"^\s*connection\s*:\s*(\w+)-(\w+)(?:{connection_meta})?\s*$"
            hub = re.search(hub_pattern, line[1])
            connection = re.search(connection_pattern, line[1])
            if (not hub and not connection):
                raise ValueError(f"Error [{line[0]}] Invalid Pattern")
            if (hub):
                hub_type, *_ = hub.groups()
                if (hub_type == "start_hub" or hub_type == "end_hub"):
                    if (hub_type == 'start_hub' and start_exist):
                        raise ValueError(f"Error [{line[0]}] start_hub Key Is Duplicated")
                    elif (hub_type == 'start_hub' and not start_exist):
                        start_exist = 1
                    elif (hub_type == 'end_hub' and end_exist):
                        raise ValueError(f"Error [{line[0]}] end_hub Key Is Duplicated")
                    else:
                        end_exist = 1
                try:
                    self.__validte_set_hub(hub.groups())
                except ValueError as e:
                    raise ValueError(f"Error [{line[0]}] {e}")
            else:
                connection_exist = 1
                first, second, *metadata = connection.groups()
                if not self.config['hubs'].get(first) or not self.config['hubs'].get(second):
                    raise ValueError(f"Error [{line[0]}] Zone Name Not Exist")
                if len({first, second}) == 1:
                    raise ValueError(f"Error: [{line[0]}] Can't Have Self Connection")
                if frozenset([first, second]) in self.config['connections']:
                    raise ValueError(f"Error [{line[0]}] Connection Duplicated")
                if metadata and metadata[0]:
                    self.config['connections'].update({frozenset([first, second]): int(metadata[0].split("=")[-1])})
                else:
                    self.config['connections'].update({frozenset([first, second]): 1})
        if (not start_exist or not end_exist):
            raise ValueError("Error: start_hub and end_hub are required")
        if (not connection_exist):
            raise ValueError("Error: At least One Connection Should Exist")

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
    for k, v in p.config['hubs'].items():
        print(k, ":", v)
    print("\n\n")
    for k, v in p.config['connections'].items():
        print(k, ":", v)

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
