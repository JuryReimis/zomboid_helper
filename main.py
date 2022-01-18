import os
import time
from collections import namedtuple
import json

os.chdir("D:\\Steam\\steamapps\\workshop\\content\\108600")


def check_modify(dir_name: str):
    print(dir_name)
    last_check_time = namedtuple("years", "tm_year, tm_mon, tm_mday")
    latest_update_time = last_check_time(tm_year=2022, tm_mon=1, tm_mday=14)
    updated_files = {}
    time_of_update = {}
    walk = os.walk(dir_name)
    for path, directories, files in walk:
        print(path, directories)
        for file in files:
            now_check = "\\".join([path, file])
            file_lm = time.gmtime(os.path.getmtime(now_check))
            if latest_update_time <= file_lm:
                latest_update_time = file_lm
                relative_path = now_check.replace(os.getcwd() + "\\", "").split(sep="\\")
                time_of_update[relative_path[2]] = file_lm
                updated_files[(relative_path[2])] = f"{relative_path[0]} - {time.strftime('%Y-%m-%d %H:%M', time_of_update[relative_path[2]])}"
    file_name = f"{time.strftime('%Y-%m-%d', time.gmtime(time.time()))}.txt"
    zomboid_place = find_dir(name="Zomboid", start_drive="C:\\Users")
    check_existence_dir(zomboid_place, "mod updates")
    with open(file=os.path.join(zomboid_place, "mod updates", file_name), mode="w", encoding="utf-8") as f:
        print(json.dumps(updated_files, indent=4), f"\nПоследнее найденное обновление файлов: {time.strftime('%Y-%m-%d %H:%M', latest_update_time)}", file=f)


def find_dir(name: str, start_drive: str) -> str:
    for path, directory, files in os.walk(start_drive):
        if name in directory:
            return os.path.join(path, name)


def check_existence_dir(path, name_dir):
    if os.path.exists(os.path.join(path, name_dir)):
        return print(f"Директория {name_dir} существует")
    else:
        os.mkdir(os.path.join(path, name_dir))
        return print(f"Директория {name_dir} создана")


# os.path.relpath(now_check, os.getcwd())
check_modify(os.getcwd())
