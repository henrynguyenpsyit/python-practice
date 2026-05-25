import os, questionary, json
from questionary import Choice, Style
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from rich import print as rprint

FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(FOLDER, "student.json")


ADD = "Thêm học sinh"
LIST = "Xem danh sách"
AVG = "Trung bình cả lớp"
DEL = "Xoá/Sửa điểm"
EXIT = "Thoát"

custom_style = Style([
    ("pointer",  "fg:#00ff00 bold"),
    ("highlighted", "fg:#00ff00 bold"),
])

def add_student(students, name, score):
    students.append({"name": name, "score": score})


def student_list(students):
    for i, s in enumerate(students, 1):
        print(f"{i}. {s['name']} | {s['score']}đ")
    

def average_score(students):
    if not students:
        return 0
    return sum(c['score'] for c in students) / len(students)
    

def ask_key(toolbar_text, keys):
    """Single-key input. Hiện Toolbar dưới, bấm phím trong `keys` để chọn."""
    kb = KeyBindings()
    result = {"key": None}

    for k in keys:
        @kb.add(str(k).lower())
        def _(event, key=k):
            result["key"] = key
            event.app.exit()

    prompt("", key_bindings=kb, bottom_toolbar=toolbar_text)
    key = result['key']
    try:
        return int(key)
    except (ValueError, TypeError):
        return key


def ask_float(prompt, min_value = None, max_value = None):
    while True: 
        try:
            f = float(input(prompt))
            if min_value is not None and f < min_value:
                print(f"Sai rồi, phải >= {min_value}")
                continue
            elif max_value is not None and f > max_value:
                print(f"Sai rồi, phải <= {max_value}")
                continue
            return f
        except ValueError:
            print("Không phải số!")


def ask_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if not s:
            print("Không hợp lệ. Vui lòng nhập lại!")
            continue
        return s


def save_list(students):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


def load_list():
    try:
        with open(PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def main():
    students = load_list()
    while True:
        choice = questionary.select(
            "_______TOOL QUẢN LÝ HỌC SINH_______",
            style=custom_style,
            choices = [ADD, LIST, AVG, DEL, EXIT]
        ).ask()
        

        if choice == ADD:
            name = ask_nonempty("Nhập tên học sinh: ")
            score = ask_float("Nhập điểm số: ", min_value=0, max_value=10)
            add_student(students, name, score)
            save_list(students)


        elif choice == LIST:
            student_list(students)
            while True:
                action = questionary.select(
                    "Thao tác:",
                    style=custom_style,
                    choices = [
                        Choice("Sắp xếp điểm số từ cao - thấp", value=1),
                        Choice("Sắp xếp điểm từ thấp - cao", value=2),
                        Choice("Quay lại", value=3)]
                ).ask()
                if action == 1:
                    sorted_list = sorted(students, key=lambda s: s['score'], reverse=True)
                    student_list(sorted_list)

                elif action == 2:
                    sorted_list = sorted(students, key=lambda s: s['score'], reverse=False)
                    student_list(sorted_list)

                elif action == 3:
                    break
            

        elif choice == AVG:
            if not students:
                print("Chưa có HS nào!")
                continue
            avg = average_score(students)
            if avg < 5:
               rprint(f"Điểm trung bình lớp: [bold red]{avg:.2f}") 
            elif avg <= 7:
                rprint(f"Điểm trung bình lớp: [bold yellow]{avg:.2f}")
            else:
                rprint(f"Điểm trung bình lớp: [bold green]{avg:.2f}")
            while True:
                key = ask_key(
                    "[1] Dưới TB | [2] Trên TB | [3] Trên 8đ | [4] Dưới 1đ | [Q] Quay lại",
                    [1, 2, 3, 4, "q"],
                )
                conditions = {
                    1: lambda s: s['score'] < 5,
                    2: lambda s: s['score'] >= 5,
                    3: lambda s: s['score'] > 8,
                    4: lambda s: s['score'] < 1,
                }
                labels = {
                    1: "Dưới TB",
                    2: "Trên TB",
                    3: "Trên 8đ",
                    4: "Dưới 1đ",
                }
                if key == "q":
                    break
                action = key
                filtered = [s for s in students if conditions [action](s)]
                sorted_list = sorted(filtered, key=lambda s: s['score'])
                rprint(f"[bold yellow]{labels[action]}[/]: có [red]{len(filtered)}[/] học sinh ")
                student_list(sorted_list)
            
                    
        elif choice == DEL:
            if not students:
                print("Không có học sinh!")
                continue
            
            name = ask_nonempty("Nhập tên HS: ")
            matches = [s for s in students if name.lower() in s['name'].lower()]
            if not matches:
                print("Không tìm thấy HS")
                continue
            target = questionary.select(
                "Chọn HS:",
                style=custom_style,
                choices = [Choice(f"{s['name']} | {s['score']}đ", value=s) for s in matches],
            ).ask()

            action = questionary.select(
                "Thao tác:",
                style=custom_style,
                choices = [
                    Choice("Xoá", value = "del"),
                    Choice("Sửa điểm", value = "edit"),
                    Choice("Huỷ bỏ", value="cancel")
                ]
            ).ask()

            if action == "del":
                if questionary.confirm(f"Xoá {target['name']}-{target['score']}đ?").ask():
                    students.remove(target)
                    save_list(students)
                    print(f"Đã xoá HS {target['name']}" )

            elif action == "edit":
                new_score = ask_float("Nhập điểm mới: ", min_value=0, max_value=10)
                target['score'] = new_score
                save_list(students)
                print(f"Đã sửa điểm HS {target['name']}: {new_score}")


        elif choice == EXIT:
            print("Chương trình kết thúc. Hẹn gặp lại!")
            break


if __name__ == "__main__":
    main()