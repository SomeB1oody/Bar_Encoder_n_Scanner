import qrcode
from PIL import Image

def get_error_correction_level(level):
    if level.upper() == 'L':
        return qrcode.constants.ERROR_CORRECT_L
    elif level.upper() == 'M':
        return qrcode.constants.ERROR_CORRECT_M
    elif level.upper() == 'Q':
        return qrcode.constants.ERROR_CORRECT_Q
    elif level.upper() == 'H':
        return qrcode.constants.ERROR_CORRECT_H
    else:
        raise ValueError("Invalid Input! Please choose 'L', 'M', 'Q' or 'H'.")

def calculate_min_size(data, error_correction, border):
    qr = qrcode.QRCode(
        version=None,
        error_correction=get_error_correction_level(error_correction),
        box_size=10,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    version = qr.version
    return (version * 4 + 17 + 2 * border)

def calculate_data_capacity(error_correction):
    capacities = {
        'L': 2953,
        'M': 2331,
        'Q': 1663,
        'H': 1273
    }
    return capacities[error_correction.upper()]

def get_available_error_correction_options(data_length):
    options = []
    if data_length <= calculate_data_capacity('L'):
        options.append('L')
    if data_length <= calculate_data_capacity('M'):
        options.append('M')
    if data_length <= calculate_data_capacity('Q'):
        options.append('Q')
    if data_length <= calculate_data_capacity('H'):
        options.append('H')
    return options

def generate_qr_code(data, error_correction, size, border):
    min_size = calculate_min_size(data, error_correction, border)

    if size < min_size:
        raise ValueError(f"Size too small! Min size is {min_size} pixels.")

    error_correction_level = get_error_correction_level(error_correction)

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction_level,
        box_size=size // min_size,
        border=border,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img = img.resize((size, size), Image.LANCZOS)
    img.save("qrcode_custom_size.png")

    return img

if __name__ == "__main__":
    while True:
        user_data = input("Please enter input data: ")
        data_length = len(user_data)

        available_options = get_available_error_correction_options(data_length)
        if not available_options:
            print(
                f"Too much data! Cannot generate QR code. Max data length is {calculate_data_capacity('L')} characters.")
            continue

        print("Fault tolerance rate: L->7% M->15% Q->20% H->30%")

        while True:
            error_correction = input(
                f"Please choose a fault tolerance rate (Available: {', '.join(available_options)}): ")
            if error_correction.upper() in available_options:
                break
            else:
                print(f"Invalid input! Please choose: {', '.join(available_options)}")

        while True:
            try:
                img_size = int(input("Enter image size (pixel): "))
                border = int(input(
                    "Please enter the blank width of the QR code picture (Module, at least 4 is recommended): "))
                qr_image = generate_qr_code(user_data, error_correction, img_size, border)
                qr_image.show()
                break
            except ValueError as e:
                print(e)
                print("Please enter the values again.")
