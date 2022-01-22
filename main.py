import nt
import os
import shutil
import sys
import time
import json


def check_modify(dir_name: str):
    zomboid_dir = find_dir(name="Zomboid", start_path="C:\\Users")
    info_from_file = record_info_from_file(flag=check_existence_dir(zomboid_dir, "mod updates"))
    latest_update_time = time.strptime(info_from_file["Отчет сделан"], "%Y-%m-%d %H:%M")
    updated_files = {}
    time_of_update = {}
    walk = os.walk(dir_name)
    for path, directories, files in walk:
        for file in files:
            now_check = "\\".join([path, file])
            file_lm = time.gmtime(os.path.getmtime(now_check))
            if latest_update_time <= file_lm:
                relative_path = now_check.replace(dir_name + "\\", "").split(sep="\\")
                time_of_update[relative_path[2]] = file_lm
                updated_files[(relative_path[
                    2])] = f"{relative_path[0]} - {time.strftime('%Y-%m-%d %H:%M', time_of_update[relative_path[2]])}"
    updated_files["Отчет сделан"] = time.strftime('%Y-%m-%d %H:%M', time.gmtime(time.time()))
    file_name = f"{time.strftime(r'%Y-%m-%d', time.gmtime(time.time()))}.txt"

    with open(file=os.path.join(zomboid_dir, "mod updates", file_name), mode="w", encoding="utf-8") as f:
        print(json.dumps(dict(sorted(updated_files.items(), key=lambda x: x[0].lower())), indent=4, ensure_ascii=False),
              file=f)
        print(f"По пути {os.path.join(zomboid_dir, 'mod updates')} находятся документы с информацией о всех изменениях")
    info_from_file = record_info_from_file(flag=check_existence_dir(zomboid_dir, "mod updates"), last=True)
    return {"zomboid_dir": zomboid_dir, "info_from_file": info_from_file}


def copy_modify(zomboid_dir: str, workshop_dir: str, info_from_file: dict) -> None:
    print("копирование")
    if len(info_from_file.keys()) < 2:
        for mod in get_realpath_of_mods(workshop_dir=workshop_dir):
            print(f"Копирую {os.path.basename(mod)}")
            shutil.copytree(mod, os.path.join(zomboid_dir, "mods", os.path.basename(mod)), dirs_exist_ok=True)
    elif len(info_from_file.keys()) >= 2:
        for mod in get_realpath_of_mods(workshop_dir=workshop_dir, mods_filter=info_from_file.keys()):
            print(f"Копирую {os.path.basename(mod)}")
            shutil.copytree(mod, os.path.join(zomboid_dir, "mods", os.path.basename(mod)), dirs_exist_ok=True)


def get_realpath_of_mods(workshop_dir: str, mods_filter=None):
    list_of_mods = []
    for item in os.scandir(workshop_dir):
        item: nt.DirEntry
        for name in os.scandir(item.path):
            name: nt.DirEntry
            if name.name == "mods":
                for mod in os.scandir(name.path):
                    mod: nt.DirEntry
                    if mods_filter is None or mod.name in mods_filter:
                        list_of_mods.append(mod.path)
    return list_of_mods


def record_info_from_file(flag: bool, path: str = r"C:\Users\indli\Zomboid\mod updates", last=False) -> dict:
    if flag is True and not next(os.scandir(path), None) is None:
        file_name = "default"
        dir_creation_time = time.gmtime(os.path.getctime(path))
        for file in os.scandir(path):
            file: os.DirEntry
            file_m_time = time.gmtime(os.path.getmtime(file.path))
            if file_m_time >= dir_creation_time:
                dir_creation_time = file_m_time
                if file.name != time.strftime("%Y-%m-%d", time.gmtime(time.time())) + ".txt":
                    file_name = file.path
                elif last is True:
                    file_name = file.path
        with open(file=file_name, mode="r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("Документы с информацией об обновлении не найдены")
        return {"Отчет сделан": time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time()))}


def find_dir(start_path: str, name: str = "content\\108600") -> str:
    relative_path, name = os.path.split(name)
    for path, directory, files in os.walk(start_path):
        if name in directory and relative_path in path:
            d = os.path.join(path, name)
            print(f"Найдена директория {d}")
            return d
    print("По указанным данным ничего не найдено\nЗавершаю программу")
    sys.exit()


def check_existence_dir(path, name_dir):
    if os.path.exists(os.path.join(path, name_dir)):
        print(f"Директория {name_dir} существует")
        return True
    else:
        os.mkdir(os.path.join(path, name_dir))
        print(f"Директория {name_dir} создана")
        return False


def main():
    user_call_dir = input("Знаете полный путь к папке с мастерской стим? y/n ")
    if user_call_dir.lower() == "y":
        user_call_workshop_path = input("Введите полный путь,который должен заканчиваться на steamapps\\workshop ")
    elif user_call_dir.lower() == "n":
        user_call_workshop_path = input("Введите букву диска, где установлен стим ")
        if len(user_call_workshop_path) and user_call_workshop_path.isalpha():
            user_call_workshop_path += ":\\"
            print(user_call_workshop_path)
        else:
            print("Введен неправильный символ")
    else:
        print("Ответ не читаем, повторите попытку")
        sys.exit()
    user_call_start_searching = input("Преступить к поиску директории с файлами из мастерской? y/n ")
    if user_call_start_searching.lower() == "y":
        print("Приступаю к поиску...")
        workshop_dir = find_dir(start_path=user_call_workshop_path)
        check_modify_dict = check_modify(workshop_dir)
    elif user_call_start_searching.lower() == "n":
        print("Завершаю программу")
        sys.exit()
    else:
        print("Ответ не читаем, повторите попытку")
        sys.exit()
    call_user_copy_files = input(
        f"""Приступить к копированию обновленных файлов в корневую директорию 
        {os.path.realpath(check_modify_dict['zomboid_dir'])} 
        в автоматическом режиме? y/n? """)
    if call_user_copy_files.lower() == "y":
        copy_modify(zomboid_dir=check_modify_dict["zomboid_dir"], workshop_dir=workshop_dir,
                    info_from_file=check_modify_dict["info_from_file"])
    print("Программа завершена!")


if __name__ == "__main__":
    main()
