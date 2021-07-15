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

def get_armour_damage(dir):
    values = {}
    for filename in get_files(dir):
        file_path = dir + "\\" + filename      
        with open(file_path, "r") as f:
            line_to_find = 'Reference([[type_armour\\tp_infantry_heavy_med.lua]])'
            for line in f.readlines():
                if line_to_find in line:
                    value, success = tryFloatParse(prev_line.split('=')[1])
                    if success:
                        values[filename] = value
                    else:
                        values[filename] = None
                prev_line = line
    return values

def read_lines(filename):
    with open(filename, "r") as f:
        return f.readlines()

def remove_nil_line(dir):    
    line_to_remove = 'GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"] = nil'
    for filename in get_files(dir):
        file_path = dir + "\\" + filename
        lines = read_lines(file_path)
        with open(file_path, "w") as f:
            for line in lines:
                if line.strip("\n") != line_to_remove:
                    f.write(line)

def append_armour_damage(dir, values):
    for filename in get_files(dir):
        file_path = dir + "\\" + filename
        with open(file_path, "a") as f:
            if not filename in values:
                continue

            f.write("\n\n")
            if values[filename] != None:
                f.write('GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_piercing_value"] = ' + str(values[filename]) + "\n")
            f.write("""GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_type"] = Reference([[type_armour\\tp_infantry_necron.lua]])
GameData["area_effect"]["weapon_damage"]["armour_damage"]["armour_piercing_types"]["entry_16"]["armour_type"]["screen_name_id"] = [[$90105]] -- Necron""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Directory must be provided")
        sys.exit(0)
    dir = sys.argv[1]

    values = get_armour_damage(dir)
    remove_nil_line(dir)
    append_armour_damage(dir, values)