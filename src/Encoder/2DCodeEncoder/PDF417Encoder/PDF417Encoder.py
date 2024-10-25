from pdf417gen import encode, render_image
import re

max_capacity = 1850

def is_valid_windows_filename(filename: str) -> bool:
    # 检查是否包含非法字符
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, filename):
        return False
    # 检查是否是保留名称
    reserved_names = [
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    ]
    if filename.upper() in reserved_names:
        return False
    # 检查是否以空格或点结尾
    if filename.endswith(' ') or filename.endswith('.'):
        return False
    # 检查文件名长度
    if len(filename) > 255:
        return False
    # 如果所有检查都通过，返回 True
    return True

def generate_pdf417(data):
    # 对输入数据进行编码
    codes = encode(data)

    if not codes:
        raise ValueError("Cannot generate PDF417")

    # 渲染条码为图片
    image = render_image(codes)

    return image

if __name__ == "__main__":
    while True:
        user_data = input("Please enter input data: ")
        if not user_data:
            print("Input cannot be empty! Please try again.")
            continue

        # 获取编码模式
        while True:
            encode_mode = input(
                "Please enter encode mode (Available: utf-8, ascii, latin1, gbk, shift_jis): "
            ).strip().lower()
            if encode_mode in ["utf-8", "ascii", "latin1", "gbk", "shift_jis"]:
                break
            else:
                print("Invalid encoding mode. Please try again.")

        match encode_mode:
            case "utf-8":
                data = user_data.encode(
                        'utf-8', errors='ignore').decode('utf-8', errors='ignore')
            case "ascii":
                data = user_data.encode(
                        'ascii', errors='ignore').decode('ascii', errors='ignore')
            case "latin1":
                data = user_data.encode(
                        'iso-8859-1', errors='ignore').decode('iso-8859-1', errors='ignore')
            case "gbk":
                data = user_data.encode(
                        'gbk', errors='ignore').decode('gbk', errors='ignore')
            case "shift_jis":
                data = user_data.encode(
                        'shift_jis', errors='ignore').decode('shift_jis', errors='ignore')
            case _:
                data = user_data.encode(
                    'utf-8', errors='ignore').decode('utf-8', errors='ignore')

        data_length = len(data)
        if data_length > max_capacity:
            print("Maximum capacity exceeded.")
            break

        while True:
            try:
                img = generate_pdf417(data)
                img.show()
                # 选择是否保存
                save_option = input("Do you want to save the image? (y/n): ").strip().lower()
                if save_option == 'y':
                    while True:
                        save_name = input("Enter a name for the image file (without extension): ").strip()
                        if is_valid_windows_filename(save_name):
                            img.save(f"{save_name}.png")
                            print(f"Image saved as {save_name}.png")
                            break
                        else:
                            print("Invalid filename. Please try again.")
                else:
                    print("Image not saved.")
            except ValueError as e:
                print(e)
                print("Please enter the values again.")