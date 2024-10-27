import barcode
from barcode.writer import ImageWriter

def generate_numeric_barcode(barcode_format, barcode_number):
    # 条形码格式对应的长度要求
    valid_lengths = {
        'upc': 12,
        'ean13': 13,
        'ean8': 8,
        'itf': None,  # ITF 可以是任意偶数位数字
        'pzn': 7,     # PZN 需要7位数字
        'jan': 13     # JAN 与 EAN-13 相同，需要13位数字
    }

    # 检查格式是否有效
    if barcode_format not in valid_lengths:
        print("无效的条形码格式！请选择 'upc'、'ean13'、'ean8'、'itf'、'pzn' 或 'jan'。")
        return

    # 检查数字长度是否有效
    if valid_lengths[barcode_format] is not None:
        if len(barcode_number) != valid_lengths[barcode_format] or not barcode_number.isdigit():
            print(f"无效的输入！{barcode_format.upper()} 条形码需要 {valid_lengths[barcode_format]} 位数字。")
            return
    else:
        # ITF 条形码要求是偶数位数字
        if len(barcode_number) % 2 != 0 or not barcode_number.isdigit():
            print("无效的输入！ITF 条形码需要偶数位数字。")
            return

    # 生成条形码
    try:
        barcode_class = barcode.get(barcode_format, barcode_number, writer=ImageWriter())
        filename = barcode_class.save(f"{barcode_format}_barcode")
        print(f"{barcode_format.upper()} 条形码已保存为：{filename}.png")
    except Exception as e:
        print(f"条形码生成失败：{e}")

if __name__ == '__main__':
    while True:
        # 用户输入条形码类型和数字
        barcode_format = input("请输入条形码格式（upc、ean13、ean8、itf、pzn、jan）：").lower()
        barcode_number = input("请输入条形码数字：")

        generate_numeric_barcode(barcode_format, barcode_number)

        # 是否继续生成
        cont = input("是否继续生成条形码？(y/n)：").strip().lower()
        if cont != 'y':
            print("程序结束。")
            break