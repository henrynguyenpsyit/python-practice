import questionary
import os
import json
from questionary import Style

custom_style = Style([
    ("pointer", "fg:#00ff00 bold"),
    ("highlighted", "fg:#00ff00 bold"),
    ("selected", "fg:#cc5454"),
])

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
    total_bought = sum(c["price"] for c in cart if c["bought"])
    total_unbought = sum(c["price"] for c in cart if not c["bought"])

    print(f"\n🛒 ĐÃ CÓ TRONG GIỎ ({len(bought_items)}) - {total_bought:,} VND")
    for c in bought_items:
        print(f" ✓  {c['item']} - {c['price']:,} VND")


    print(f"\n📋 CHƯA CÓ TRONG GIỎ ({len(unbought_items)}) - {total_unbought:,} VND")
    for i, c in enumerate(cart, 1):
        if not c["bought"]:
            print(f" {i}. {c['item']} - {c['price']:,} VND")

     
    total = sum(c["price"] for c in cart)
    print(f"\n💰 TỔNG SỐ TIỀN CẢ GIỎ HÀNG: {total:,} VND")


def check_out(cart):
    total_bought = sum(c["price"] for c in cart if c["bought"])
    if total_bought == 0:
        print("Chưa có món nào trong giỏ hàng")
        return
    pocket = ask_int("Số tiền mang theo: ", min_value=0)
    print(f"> Bạn mang theo: {pocket:,} VND")
    print(f">>Tổng đã mua: {total_bought:,} VND")
    change = pocket - total_bought
    if change > 0:
        print(f"→ Tiền thừa: {change:,} VND")
    elif change < 0:
        print(f"→ Còn thiếu: {abs(change):,} VND")
    elif change == 0:
        print("→ Vừa đủ tiền!")
    

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
    TOTAL = "Kiểm tra giỏ hàng"
    EDIT = "Chỉnh sửa giá"
    MARK = "Đánh dấu đã mua"
    CHECK = "Tính tiền"
    DEL = "Xoá món hàng"
    CLEAR = "Xoá toàn bộ"
    EXIT = "Thoát"
    while True:
        choice = questionary.select(
            "Chọn mục:",
            choices = [ADD, TOTAL, EDIT, MARK, DEL, CHECK, CLEAR, EXIT],
            style=custom_style
        ). ask()
        
        if choice == ADD:
            name = input("Thêm món hàng cần mua: ").strip()
            if not name:
                print("Tên không được rỗng!")
                continue
            if any (c['item'].lower() == name.lower() for c in cart):
                print(f"{name} đã có trong giỏ. Hãy chỉnh sửa giá!")
                continue
            price = ask_int("Giá: ", min_value=0)
            add_item(cart, name, price)
            save_cart(cart)

        elif choice == TOTAL:
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
                print("Lỗi. Vui lòng nhập lại!")
                continue
            confirm = questionary.confirm(f"Bạn chắc chắn muốn xoá {cart[dlt-1]['item']}?").ask()
            if confirm:
                deleted = delete_item(cart, dlt)
                save_cart(cart)
                print(f"Đã xoá {deleted['item']}")
            else:
                print("Huỷ xoá")

        elif choice == CHECK:
            check_out(cart)

        elif choice == CLEAR:
            cnfrm = questionary.confirm(f"Bạn chắc chắn muốn xoá toàn bộ giỏ hàng?").ask()
            if cnfrm:
                cart.clear()
                save_cart(cart)
                print("Đã xoá toàn bộ giỏ hàng!")
            else:
                print("Huỷ bỏ")
        
        elif choice == EDIT:
            check_cart(cart)
            index = ask_int("Sửa giá mặt hàng: ")
            if not (0 < index <= len(cart)):
                print(f"Không hợp lệ. Chỉ có {len(cart)} món!")
                continue
            item=cart[index-1]
            confirm_index = questionary.confirm(f"Sửa giá {item['item']} (hiện đang {item['price']:,})?").ask()
            if not confirm_index:
                print("Huỷ bỏ")
                continue
            new_price = ask_int("Giá mới: ", min_value=0)
            item["price"] = new_price
            save_cart(cart)
            print(f"Đã sửa: {item['item']} = {new_price:,} VND")
            
        elif choice == EXIT:
            print("Chương trình kết thúc. Tạm biệt!")
            break

if __name__ == "__main__":
    main()