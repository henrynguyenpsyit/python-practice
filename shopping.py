import questionary

def add_item(cart, item):
    cart.append({"item":item, "bought":False})


def check_cart(cart):
    if not cart:
        print("Giỏ hàng trống")
        return
    
    bought_items = [c for c in cart if c["bought"]]
    unbought_items = [c for c in cart if not c["bought"]]

    print(f"\n🛒 ĐÃ MUA {len(bought_items)}")
    for c in bought_items:
        print(f" ✓  {c['item']}")

    print(f"\n📋 CHƯA MUA {len(unbought_items)}")
    for i, c in enumerate(cart, 1):
        if not c["bought"]:
            print(f" {i}. {c['item']}")


def mark_bought(cart, index):
    if not (0 < index <= len(cart)):
        return "invalid"
    elif cart[index - 1]["bought"]:
        return "already"
    cart[index - 1]['bought'] = True
    return cart[index-1]


def delete_item(cart, index):
    if 0 < index <= len(cart):
        return cart.pop(index - 1)
    return None


def ask_int(prompt):
    """Hỏi user 1 số int, lặp lại cho đến khi đúng"""
    while True:
        a = input(prompt)
        try:
            return int(a)
        except ValueError:
            print("Bạn phải nhập số!")


def main():
    cart = []
    ADD = "Thêm vào giỏ hàng"
    CHECK = "Kiểm tra giỏ hàng"
    MARK = "Đánh dấu đã mua"
    DEL = "Xoá món hàng"
    EXIT = "Thoát"
    while True:
        choice = questionary.select(
            "Chọn mục:",
            choices = [ADD, CHECK, MARK, DEL, EXIT]
        ). ask()
        print(choice)
        
        if choice == ADD:
            add = input("Thêm món hàng cần mua: ").strip()
            add_item(cart, add)

        elif choice == CHECK:
            check_cart(cart)
        
        elif choice == MARK:
            check_cart(cart)
            number = ask_int("Nhập thứ tự món đã mua: ")
            result = mark_bought(cart, number)
            if result == "invalid":
                print(f"Không hợp lệ. Chỉ có {len(cart)} món!")
            elif result == "already":
                print("Món này đã mua rồi! Hãy chọn lại.")
            else:
                print(f"Đã mua {result['item']}")
            
        elif choice == DEL:
            check_cart(cart)
            dlt = ask_int("Nhập thứ tự món muốn xoá: ")
            if not (0 < dlt <= len(cart)):
                print("Lỗi. Vui lòng nhập lại")
                continue
            confirm = questionary.confirm(f"Bạn chắc chắn muốn xoá {cart[dlt-1]['item']}?").ask()
            if confirm:
                deleted = delete_item(cart, dlt)
                print(f"Đã xoá {deleted['item']}")
            else:
                print("Huỷ xoá")

        elif choice == EXIT:
            print("Chương trình kết thúc. Tạm biệt!")
            break

if __name__ == "__main__":
    main()