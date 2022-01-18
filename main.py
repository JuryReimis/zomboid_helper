import os
import time
import json

os.chdir("D:\\Steam\\steamapps\\workshop\\content\\108600")


def check_modify(dir_name: str):
    print(dir_name)
    zomboid_place = find_dir(name="Zomboid", start_drive="C:\\Users")
    latest_update_time = record_info_from_file(flag="y")
    updated_files = {}
    time_of_update = {}
    walk = os.walk(dir_name)
    for path, directories, files in walk:
        for file in files:
            now_check = "\\".join([path, file])
            file_lm = time.gmtime(os.path.getmtime(now_check))
            if latest_update_time <= file_lm:
                latest_update_time = file_lm
                relative_path = now_check.replace(os.getcwd() + "\\", "").split(sep="\\")
                time_of_update[relative_path[2]] = file_lm
                updated_files[(relative_path[
                    2])] = f"{relative_path[0]} - {time.strftime('%Y-%m-%d %H:%M', time_of_update[relative_path[2]])}"
    updated_files["Отчет сделан"] = time.strftime('%Y-%m-%d %H:%M', time.gmtime(time.time()))
    file_name = f"{time.strftime(r'%Y-%m-%d', time.gmtime(time.time()))}.txt"
    check_existence_dir(zomboid_place, "mod updates")
    with open(file=os.path.join(zomboid_place, "mod updates", file_name), mode="w", encoding="utf-8") as f:
        print(json.dumps(updated_files, indent=4, ensure_ascii=False), file=f)


def record_info_from_file(flag: str, path: str = r"C:\Users\indli\Zomboid\mod updates"):
    if flag.lower() == "y":
        file_name = "default"
        latest_record = time.gmtime(os.path.getmtime(path))
        for file in os.scandir(path):
            file: os.DirEntry
            file_m_time = time.gmtime(os.path.getmtime(file.path))
            if file_m_time >= latest_record:
                latest_record = file_m_time
                file_name = file.path
        with open(file=file_name, mode="r", encoding="utf-8") as f:
            return time.strptime(json.load(f)["Отчет сделан"], "%Y-%m-%d %H:%M")
    else:
        return time.gmtime(time.time())


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


check_modify(os.getcwd())
