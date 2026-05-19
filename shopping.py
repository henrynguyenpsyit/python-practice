import questionary
import os
import json

FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(FOLDER,"shopping_cart.json")

DEFAULTS = {
    "item": "",
    "price": 0,
    "bought": False,
    # tương lai thêm fỉeld nào chỉ cần thêm ở đây: 
    # "quantity" : 1
    # "category" : "",
} 
#Đây là giá trị default của các field mới trong tương lai#

def migrate(item):
    """Bổ sung các field còn thiếu trong item."""
    for key, default_value in DEFAULTS.items():
        if key not in item:
            item[key] = default_value
    return item


def add_item(cart, item_name, price=0):
    new = {**DEFAULTS, "item": item_name, "price": price}
    cart.append(new)


def check_cart(cart):
    if not cart:
        print("Giỏ hàng trống")
        return
    
    bought_items = [c for c in cart if c["bought"]]
    unbought_items = [c for c in cart if not c["bought"]]

    print(f"\n🛒 ĐÃ MUA {len(bought_items)}")
    for c in bought_items:
        print(f" ✓  {c['item']} - {c['price']} VND")
    
    total_bought = sum(c["price"] for c in cart if c["bought"])
    print(f"\n ĐÃ MUA: {total_bought} VND")

    print(f"\n📋 CHƯA MUA {len(unbought_items)}")
    for i, c in enumerate(cart, 1):
        if not c["bought"]:
            print(f" {i}. {c['item']} - {c['price']} VND")

    total_unbought = sum(c["price"] for c in cart if not c["bought"])
    print(f"\n CHƯA MUA: {total_unbought} VND")
     
    total = sum(c["price"] for c in cart)
    print(f"\n💰 TỔNG SỐ TIỀN CẢ GIỎ HÀNG: {total} VND")


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


def ask_int(prompt, min_value=None):
    """Hỏi user 1 số int, lặp lại cho đến khi đúng"""
    while True:
        a = input(prompt)
        try:
            n = int(a)
            if min_value is not None and n < min_value:
                print (f"Phải >= {min_value}!")
                continue
            return n
        except ValueError:
            print("Bạn phải nhập số!")


def save_cart(cart):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(cart, f, ensure_ascii=False, indent=2)


def load_cart():
    try:
        with open(PATH, "r", encoding="utf-8") as f:
            cart = json.load(f)
        return [migrate(c) for c in cart]
    except FileNotFoundError:
        return []


def main():
    cart = load_cart()
    ADD = "Thêm vào giỏ hàng"
    CHECK = "Kiểm tra giỏ hàng"
    MARK = "Đánh dấu đã mua"
    DEL = "Xoá món hàng"
    CLEAR = "Xoá toàn bộ"
    EXIT = "Thoát"
    while True:
        choice = questionary.select(
            "Chọn mục:",
            choices = [ADD, CHECK, MARK, DEL, CLEAR, EXIT]
        ). ask()
        print(choice)
        
        if choice == ADD:
            name = input("Thêm món hàng cần mua: ").strip()
            if not name:
                print("Tên không được rỗng!")
                continue
            price = ask_int("Giá: ", min_value=0)
            add_item(cart, name, price)
            save_cart(cart)

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
                save_cart(cart)
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
                save_cart(cart)
                print(f"Đã xoá {deleted['item']}")
            else:
                print("Huỷ xoá")

        elif choice == CLEAR:
            cnfrm = questionary.confirm(f"Bạn chắc chắn muốn xoá toàn bộ giỏ hàng?").ask()
            if cnfrm:
                cart.clear()
                save_cart(cart)
                print("Đã xoá toàn bộ giỏ hàng!")
            else:
                print("Huỷ bỏ")

        elif choice == EXIT:
            print("Chương trình kết thúc. Tạm biệt!")
            break

if __name__ == "__main__":
    main()