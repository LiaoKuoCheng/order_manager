import json

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> list:
    """讀取 JSON 檔案，若檔案不存在則回傳空列表"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_orders(filename: str, orders: list) -> None:
    """儲存訂單資料到 JSON 檔案"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)

def calculate_order_total(order: dict) -> int:
    """計算單筆訂單總金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])

def add_order(orders: list) -> str:
    """新增訂單並加入 orders 清單"""
    order_id = input("請輸入訂單編號：").strip().upper()
    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：").strip()
    items = []
    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if not name:
            break

        # 價格輸入
        while True:
            try:
                price_input = input("請輸入價格：").strip()
                price = int(price_input)
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        # 數量輸入
        while True:
            try:
                qty_input = input("請輸入數量：").strip()
                quantity = int(qty_input)
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({
        "order_id": order_id,
        "customer": customer,
        "items": items
    })
    return f"=> 訂單 {order_id} 已新增！"

def Display_Order(data: list, title: str = "訂單報表", single: bool = False) -> None:
    """印出訂單報表"""
    if not data:
        print("=> 沒有任何訂單")
        return

    if not single:
        print("\n==================== 訂單報表 ====================")

    for idx, order in enumerate(data, 1):
        if not single:
            print(f"\n訂單 #{idx}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print(f"{'商品名稱 '}{'單價':>8}{'數量':>8}{'小計':>10}")
        print("-" * 50)
        total = 0
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            print(f"{item['name']:<10}{item['price']:>8}{item['quantity']:>8}{subtotal:>15}")
        print("-" * 50)
        print(f"訂單總額: {total}")
        print("=" * 50)

def process_order(orders: list) -> tuple[str, dict | None]:
    """處理出餐訂單並從待處理訂單中移除"""
    if not orders:
        return ("=> 無待處理訂單", None)

    print("\n======== 待處理訂單列表 ========")
    for idx, order in enumerate(orders, 1):
        print(f"{idx}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    while True:
        choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
        if not choice:
            return ("=> 已取消出餐", None)
        if not choice.isdigit():
            print("=> 錯誤：請輸入有效的數字")
            continue

        index = int(choice) - 1
        if 0 <= index < len(orders):
            finished_order = orders.pop(index)
            output_orders = load_data(OUTPUT_FILE)
            output_orders.append(finished_order)
            save_orders(OUTPUT_FILE, output_orders)
            return (f"=> 訂單 {finished_order['order_id']} 已出餐完成", finished_order)
        else:
            print("=> 錯誤：編號超出範圍")

def main():
    """主程式流程"""
    orders = load_data(INPUT_FILE)

    while True:
        print("***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()
        if choice == "":
            break
        elif choice == "1":
            msg = add_order(orders)
            print(msg)
            save_orders(INPUT_FILE, orders)
        elif choice == "2":
            Display_Order(orders)
        elif choice == "3":
            msg, order = process_order(orders)
            print(msg)
            if order:
                print("\n==================== 出餐訂單 ====================")
                print_order_report([order], single=True)
            save_orders(INPUT_FILE, orders)
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()
