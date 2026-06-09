import re


result = re.search(r"^\s*nb_drones\s*:\s*(\+?[0-9]+)\s*$", "   nb_drones       : -520  ")
if (not result):
    print("No Match")
else:
    print(result.groups())