import os


def tryFloatParse(value):
    try:
        return float(value), True
    except ValueError:
        return value, False


directory = "."
value_set = {}
for filename in os.listdir(directory):
    if filename.endswith(".lua"):
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_04"]["armour_piercing_value"]'):
                    val, is_number = tryFloatParse(line.split("=")[1])
                    if is_number:
                        value_set[filename] = val

for filename in os.listdir(directory):
    if filename.endswith(".lua"):
        with open(filename, "a") as f:
            if filename not in value_set:
                print(filename)
                continue
            val = value_set[filename]
            data = """
\n
GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_piercing_value"] = {0}
GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_type"] = Reference([[type_armour\\tp_infantry_necron.lua]])
GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_type"]["screen_name_id"] = [[$90105]] -- Heavy Infantry
""".format(val)
            f.write(data)