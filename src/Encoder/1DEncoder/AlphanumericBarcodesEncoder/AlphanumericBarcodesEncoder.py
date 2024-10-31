import barcode
from barcode.writer import ImageWriter

# 支持的条形码格式列表
SUPPORTED_FORMATS = ['code39', 'code128']

# 验证输入内容是否符合所选格式的要求
def validate_input(data, barcode_format):
    if barcode_format == 'code39':
        # Code39 只能包含大写字母、数字和 -.$/+% 空格
        valid_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.$/+% '
        return all(char in valid_chars for char in data)
    elif barcode_format == 'code128':
        # Code128 可以包含所有ASCII字符，不需要额外验证
        return True
    else:
        return False

# 生成条形码函数
def generate_barcode(data, barcode_format, filename='barcode'):
    # 检查选择的条形码格式是否受支持
    if barcode_format.lower() not in SUPPORTED_FORMATS:
        print(f"Invalid barcode type: {barcode_format}. Please choose 'Code39' or 'Code128'.")
        return

    # 验证输入数据
    if not validate_input(data, barcode_format.lower()):
        print("Invalid input")
        return

    # 创建条形码对象并生成图像
    barcode_class = barcode.get_barcode_class(barcode_format)
    barcode_obj = barcode_class(data, writer=ImageWriter())
    barcode_obj.save(filename)
    print(f"Barcode saved as '{filename}.png'")

if __name__ == '__main__':
    while True:
        # 获取用户输入
        data = input("Please enter data (Enter 'exit' to exit): ")
        if data.lower() == 'exit':
            print("Bye")
            break

        barcode_format = input("Please choose barcode format (Code39, Code128): ")

        # 生成条形码并命名文件
        filename = input("Enter filename(no suffix): ")
        generate_barcode(data, barcode_format, filename)

        # 提示是否继续生成
        continue_choice = input("If continue generating (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("Bye")
            break
