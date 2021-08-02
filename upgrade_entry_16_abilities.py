import os
import sys


def tryFloatParse(value):
    try:
        return float(value), True
    except ValueError:
        return value, False

def get_files(dir):
    for filename in os.listdir(dir):
        if filename.endswith(".lua"):
            yield filename

def get_target_filter(dir):
    values = {}
    for filename in get_files(dir):
        file_path = dir + "\\" + filename      
        with open(file_path, "r") as f:
            start = 'GameData["area_effect"]["area_effect_information"]["target_filter"]'
            end = 'Reference([[type_armour\\tp_infantry_heavy_med.lua]])'
            for line in f.readlines():
                if start in line and end in line:
                    values[file_path] = True
    return values

def read_lines(filename):
    with open(filename, "r") as f:
        return f.readlines()

def remove_nil_line(dir):    
    lines_to_remove = ['GameData["area_effect"]["area_effect_information"]["target_filter"]["entry_16"] = nil', 'GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"] = nil']
    for filename in get_files(dir):
        file_path = dir + "\\" + filename
        lines = read_lines(file_path)
        with open(file_path, "w") as f:
            for line in lines:
                if line.strip("\n") not in lines_to_remove:
                    f.write(line)


def get_armour_damage(dir):
    values = {}
    for filename in get_files(dir):
        file_path = dir + "\\" + filename      
        with open(file_path, "r") as f:
            start = 'GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]'
            end = '["armour_type"] = Reference([[type_armour\\tp_infantry_heavy_med.lua]])'
            for line in f.readlines():
                if start in line and end in line:
                    value, success = tryFloatParse(prev_line.split('=')[1])
                    if success:
                        values[file_path] = value
                    else:
                        values[file_path] = None
                prev_line = line
    return values

def append_armour_damage(dir, has_target_values, piercing_values):
    for filename in get_files(dir):
        file_path = dir + "\\" + filename
        with open(file_path, "a") as f:
            if not file_path in has_target_values:
                continue

            f.write("\n\n")
            f.write("""GameData["area_effect"]["area_effect_information"]["target_filter"]["entry_16"] = Reference([[type_armour\\tp_infantry_necron.lua]])
GameData["area_effect"]["area_effect_information"]["target_filter"]["entry_16"]["screen_name_id"] = [[$90105]] -- Infantry Necron""")
            f.write("\n\n")
            if file_path in piercing_values:
                f.write('GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_piercing_value"] = ' + str(piercing_values[file_path]) + '\n')
                f.write("""GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_type"] = Reference([[type_armour\\tp_infantry_necron.lua]])
GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_type"]["screen_name_id"] = [[$90105]] -- Infantry Necron""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Directory must be provided")
        sys.exit(0)
    dir = sys.argv[1]

    has_target_values = get_target_filter(dir)
    piercing_values = get_armour_damage(dir)
    remove_nil_line(dir)
    append_armour_damage(dir, has_target_values, piercing_values)