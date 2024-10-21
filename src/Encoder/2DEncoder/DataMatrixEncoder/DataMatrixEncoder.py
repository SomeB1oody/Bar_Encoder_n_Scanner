from pylibdmtx.pylibdmtx import encode
from PIL import Image
import re

MAX_CAPACITY = 2335  # 适用于 ASCII 编码

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

def generate_datamatrix(data, encode_mode):
    # 生成Data Matrix条码
    encoded = encode(data.encode(encode_mode))
    # 将生成的字节转换为图片
    image = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    # 保存图片
    return image

if __name__ == '__main__':
    while True:
        # 获取用户输入
        while True:
            user_input = input("Please enter data: ")
            if not user_input:
                print("Input cannot be empty! Please try again.")
                continue
            if len(user_input) > MAX_CAPACITY:
                print("Input is too large! Please try again.")
                continue
            break

        # 获取编码模式
        while True:
            encode_mode = input("Please enter encode mode (Available: utf-8, ascii, latin1, gbk, shift_jisx0213): ").strip().lower()
            if encode_mode in ["utf-8", "ascii", "latin1", "gbk", "shift_jisx0213"]:
                break
            else:
                print("Invalid encoding mode. Please try again.")

        try:
            img = generate_datamatrix(user_input, encode_mode)
            img.show()  # 显示生成的 Data Matrix 图片

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
            print(f"Error: {e}")
