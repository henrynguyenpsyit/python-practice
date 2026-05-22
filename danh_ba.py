import json, os, questionary
from questionary import Choice, Style
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

custom_style = Style([
    ("pointer", "fg:#ffff00 bold"),
    ("highlighted", "fg:#ffff00 bold"),
])

FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(FOLDER, "contact.json")


def add_contact(contact, name, phone):
    contact.append({"name": name, "phone": phone})


def contact_list(contact):
    for i, p in enumerate(contact, 1):
        print(f"{i}. {p['name']} - {p['phone']}")


def find_contact(name, contact):
    query = name.lower()
    return [c for c in contact if query in c['name'].lower()]


def del_contact(target, contact):
    contact.remove(target)


kb = KeyBindings()

@kb.add('escape')
def _(event):
    event.app.exit(result=None)

def ask_nonempty(prompt_text):
    """Hỏi string không rỗng. Nhấn nút ESC để thoát"""
    while True:
        s = prompt(prompt_text, 
                   key_bindings=kb,
                   bottom_toolbar="[ECS] Quay lại")
        if s is None:
            return None
        s = s.strip()
        if s:
            return s
        print("Không được để trống!")


def ask_int(prompt_text):
    while True:
        num = prompt(prompt_text, 
                     key_bindings=kb,
                     bottom_toolbar="[ECS] Quay lại")
        if num is None:
            return None
        try:
            return int(num)
        except ValueError:
            print("Phải nhập số!")


def save_list(contact):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(contact, f, ensure_ascii=False, indent=2)


def load_list():
    try:
        with open(PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:        
        return []

ADD = "Thêm danh bạ"
LIST = "Xem danh bạ"
FIND = "Tìm danh bạ"
EDIT = "Sửa danh bạ"
DEL = "Xoá danh bạ"
EXIT = "Thoát"

def main ():
    contact = load_list()

    while True:
        choice = questionary.select(
            "===TOOL QUẢN LÝ DANH BẠ===",
            choices = [ADD, LIST, FIND, EDIT, DEL, EXIT],
            style=custom_style
        ).ask()


        if choice == ADD:
            name = ask_nonempty("Nhập tên danh bạ: ")
            num = ask_int("Nhập số điện thoại: ")
            if num is None:
                continue
            add_contact(contact, name, num)
            save_list(contact)

        
        elif choice == LIST:
            contact_list(contact)
        

        elif choice == FIND:
            find = ask_nonempty("Nhập danh bạ cần tìm: ")
            if find is None:
                continue
            result = find_contact(find, contact)
            if not result:
                print("Không tìm thấy!")
            else:
                print(f"Tìm thấy {len(result)} phần tử")
                for i, c in enumerate(result, 1):
                    print(f"{i}. {c['name']} - {c['phone']}")
            

        elif choice == EDIT:
            find = ask_nonempty("Nhập danh bạ cần tìm: ")
            if find is None:
                continue
            result = find_contact(find, contact)
            if not result:
                print("Không tìm thấy!")
            else:
                print(f"Tìm thấy {len(result)} phần tử")
                for i, c in enumerate(result, 1):
                    print(f"{i}. {c['name']} - {c['phone']}")
                if len(result) == 1 or len(result) > 1:
                    choose = questionary.select(
                        "Chọn Danh bạ để sửa",
                        choices = [Choice(f"{c['name']} - {c['phone']}", value=c) for c in result],
                        style=custom_style
                    ). ask()
                    config = questionary.select(
                        "Bạn muốn sửa tên/số?",
                        choices = ["Tên", "Số"]
                    ).ask()
                    
                    if config == "Tên":
                        new_name = ask_nonempty("Nhập tên mới: ")
                        if new_name is None:
                            continue
                        choose['name'] = new_name
                        save_list(contact)
                    else:
                        new_num = ask_int("Nhập số điện thoại mới: ")
                        if new_num is None:
                            continue
                        choose['phone'] = new_num
                        save_list(contact)


        elif choice == DEL:
            find = ask_nonempty("Nhập danh bạ cần tìm: ")
            if find is None:
                continue
            result = find_contact(find, contact)
            if not result:
                print("Không tìm thấy!")
            else:
                print(f"Tìm thấy {len(result)} phần tử")
                for i, c in enumerate(result, 1):
                    print(f"{i}. {c['name']} - {c['phone']}")
                if len(result) == 1 or len(result) > 1:
                    choose = questionary.select(
                        "Chọn Danh bạ để xoá",
                        choices = [Choice(f"{c['name']} - {c['phone']}", value=c) for c in result],
                        style=custom_style
                    ).ask()
                    if questionary.confirm(f"Bạn chắc chắn muốn xoá {choose['name']}").ask():
                        del_contact(choose, contact)
                        save_list(contact)
                        print(f"Đã xoá danh bạ của {choose['name']}")
                    else:
                        print("Huỷ bỏ")


        elif choice == EXIT:
            break

if __name__ == "__main__":
    main()    