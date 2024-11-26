import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image
from pylibdmtx.pylibdmtx import encode
import wx
import re
from io import BytesIO

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

def calculate_check_digit(gtin):
    # 计算GTIN-13编码的校验位。
    total = 0
    for i, digit in enumerate(gtin[:12]):
        if i % 2 == 0:
            total += int(digit)
        else:
            total += int(digit) * 3
    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)

def generate_gtin(gtin_input):
    # 根据12位输入生成带校验位的完整GTIN-13编码。
    if len(gtin_input) == 12 and gtin_input.isdigit():
        return gtin_input + calculate_check_digit(gtin_input)
    return None

def generate_barcode(gtin, barcode_format):
    # 根据选择生成一维条形码并保存为PNG文件。
    barcode_class = barcode.get_barcode_class(barcode_format)
    barcode_obj = barcode_class(gtin, writer=ImageWriter())

    # 使用 BytesIO 将条形码保存在内存中
    buffer = BytesIO()
    barcode_obj.write(buffer)  # 将图像写入内存
    buffer.seek(0)  # 将内存指针移动到开头

    # 使用 Pillow 打开图像
    img = Image.open(buffer)

    return img

def generate_qr_code(data):
    # 生成QR码并保存为PNG文件。
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    return img

def generate_data_matrix(data):
    # 生成Data Matrix码并保存为PNG文件。
    encoded = encode(data.encode('utf-8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

    return img

class GS1Encoder(wx.Frame):
    def __init__(self, *args, **kw):
        super(GS1Encoder, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 选择维度
        self.dimension = wx.RadioBox(
            panel, label="Choose input type", choices=[
                '1D', '2D'
            ]
        )
        self.vbox.Add(self.dimension, flag=wx.ALL, border=5)
        self.dimension.Bind(wx.EVT_RADIOBOX, self.on_dimension)

        #选择格式
        self.type_choice = ['EAN13', 'UPCA','Code128']
        self.process_type = wx.ListBox(panel, choices=self.type_choice, style= wx.LB_SINGLE)
        self.vbox.Add(self.process_type, flag=wx.ALL, border=5)

        # 输入文本
        self.vbox.Add(wx.StaticText(panel, label=
        "Please enter a 12-digit number to generate:"), flag=wx.ALL, border=5)
        self.text_input = wx.TextCtrl(panel)
        self.vbox.Add(self.text_input, flag=wx.EXPAND | wx.ALL, border=5)

        # 生成按钮
        self.generate_button = wx.Button(panel, label="Generate")
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        self.vbox.Add(self.generate_button, flag=wx.ALL, border=5)

        # 输出路径
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.folder_button = wx.Button(panel, label="Select output folder")
        self.Bind(wx.EVT_BUTTON, self.on_select_folder, self.folder_button)
        self.hbox2.Add(self.folder_button, flag=wx.ALL, border=5)
        self.output_path_text = wx.StaticText(panel, label="Click \"Select output folder\" first")
        self.hbox2.Add(self.output_path_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox2, flag=wx.EXPAND)

        # 输出格式单选框
        self.output_format = wx.RadioBox(
            panel, label="Choose output format:", choices=[
                '.jpg', '.jpeg', '.png', '.tiff',
                '.tif', '.bmp', '.ppm', '.pgm', '.pbm', '.webp'
            ]
        )
        self.vbox.Add(self.output_format, flag=wx.ALL, border=5)

        # 输出名称
        self.vbox.Add(wx.StaticText(panel, label=
        "Output image name:(no file suffix)"), flag=wx.ALL, border=5)
        self.output_name = wx.TextCtrl(panel)
        self.vbox.Add(self.output_name, flag=wx.EXPAND | wx.ALL, border=5)

        # 保存按钮
        self.save_button = wx.Button(panel, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_button)
        self.vbox.Add(self.save_button, flag=wx.ALL, border=5)

        # 设置面板的布局管理器
        panel.SetSizer(self.vbox)
        panel.Layout()

    def on_dimension(self, event):
        selected_dimension = self.dimension.GetStringSelection()
        if selected_dimension == '1D':
            self.type_choice = ['EAN13', 'UPCA','Code128']
        else:
            self.type_choice = ['QR Code', 'DataMatrix']
        self.process_type.Set(self.type_choice)

    def on_select_folder(self, event):
        with wx.DirDialog(None, "Select a folder for output", "",
                          style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.output_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_folder = dialog.GetPath()

    def on_generate_button(self, event):
        dimension_type = self.dimension.GetStringSelection()
        process_type = self.process_type.GetStringSelection()
        input_text = self.text_input.GetValue()

        if len(input_text) == 12 and input_text.isdigit():
            gtin = generate_gtin(input_text)
            if dimension_type == '1D':
                if not process_type == 'UPCA':
                    img = generate_barcode(gtin, process_type.lower())
                else:
                    img = generate_barcode(gtin[:11], 'upca')
            else:
                if process_type == 'QR Code':
                    img = generate_qr_code(gtin)
                else:
                    img = generate_data_matrix(gtin)

            # 显示生成的图像
            img.show()

        else:
            wx.MessageBox(
                'Input is invalid. Please enter a 12-digit number to generate',
                'Error', wx.OK | wx.ICON_ERROR
            )

    def on_save_button(self, event):
        dimension_type = self.dimension.GetStringSelection()
        process_type = self.process_type.GetStringSelection()
        input_text = self.text_input.GetValue()
        output_path = self.selected_folder
        output_name = self.output_name.GetValue()
        selected_format = self.output_format.GetStringSelection()

        if not process_type:
            wx.MessageBox('choose a type for processing first', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not output_path:
            wx.MessageBox('Output folder cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not is_valid_windows_filename(output_name):
            wx.MessageBox('Output name is invalid', 'Error', wx.OK | wx.ICON_ERROR)
            return

        path = f'{output_path}/{output_name}{selected_format}'

        if len(input_text) == 12 and input_text.isdigit():
            gtin = generate_gtin(input_text)
            if dimension_type == '1D':
                if not process_type == 'UPCA':
                    img = generate_barcode(gtin, process_type.lower())
                else:
                    img = generate_barcode(gtin[:11], 'upca')
            else:
                if process_type == 'QR Code':
                    img = generate_qr_code(gtin)
                else:
                    img = generate_data_matrix(gtin)

            try:
                img.save(path)
                wx.MessageBox(f'Image saved to {path}','Success', wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
                return

        else:
            wx.MessageBox(
                'Input is invalid. Please enter a 12-digit number to generate',
                'Error',wx.OK | wx.ICON_ERROR
            )
            return


if __name__ == "__main__":
    app = wx.App()
    frame = GS1Encoder(None)
    frame.SetTitle('GS1 Encode with GUI')
    frame.SetSize((700, 500))
    frame.Show()
    app.MainLoop()
