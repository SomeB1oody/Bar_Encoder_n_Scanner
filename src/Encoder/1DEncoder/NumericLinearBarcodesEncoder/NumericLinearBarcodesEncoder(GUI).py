import barcode
from barcode.writer import ImageWriter
import wx
import re
from io import BytesIO
from PIL import Image

# 条形码格式对应的长度要求
valid_lengths = {
    'upc': 12,
    'ean13': 13,
    'ean8': 8,
    'itf': None,  # ITF 可以是任意偶数位数字
    'pzn': 7,     # PZN 需要7位数字
    'jan': 13     # JAN 与 EAN-13 相同，需要13位数字
}

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

def input_check(barcode_format, barcode_number):
    # 检查数字长度是否有效
    if valid_lengths[barcode_format] is not None:
        if len(barcode_number) != valid_lengths[barcode_format] or not barcode_number.isdigit():
            return False
    else:
        # ITF 条形码要求是偶数位数字
        if len(barcode_number) % 2 != 0 or not barcode_number.isdigit():
            return False

    return True

def generate_numeric_barcodes(barcode_format, barcode_number):
    flag = input_check(barcode_format, barcode_number)
    if not flag:
        if barcode_format != 'itf':
            error_message = f'Invalid input! {barcode_format.upper()} needs {valid_lengths[barcode_format]} digits'
        else:
            error_message = f'Invalid input! {barcode_format.upper()} needs even digits'

        wx.MessageBox(error_message, 'Error', wx.OK | wx.ICON_ERROR)
        return

    barcode_class = barcode.get(barcode_format, barcode_number, writer=ImageWriter())

    return barcode_class

class NumericLinearBarcodesEncoderWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(NumericLinearBarcodesEncoderWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 选择格式
        self.barcode_type = wx.RadioBox(
            panel, label="Choose input type", choices=[
                'UPC', 'EAN13', 'EAN8', 'ITF', 'PZN', 'JAN'
            ]
        )
        self.vbox.Add(self.barcode_type, flag=wx.ALL, border=5)

        # 输入数字
        self.vbox.Add(wx.StaticText(panel, label=
        "Digits input"), flag=wx.ALL, border=5)
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

    def on_select_folder(self, event):
        with wx.DirDialog(None, "Select a folder for output", "",
                          style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.output_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_folder = dialog.GetPath()

    def on_generate_button(self, event):
        selected_type = self.barcode_type.GetStringSelection().lower()
        text_input = self.text_input.GetValue()

        if not text_input:
            wx.MessageBox('Input cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        barcode_img = generate_numeric_barcodes(selected_type, text_input)

        # 使用 BytesIO 将条形码保存到内存中
        buffer = BytesIO()
        barcode_img.write(buffer)

        # 使用 Pillow 显示条形码图像
        image = Image.open(buffer)
        image.show()

    def on_save_button(self, event):
        selected_type = self.barcode_type.GetStringSelection().lower()
        text_input = self.text_input.GetValue()
        output_path = self.selected_folder
        output_name = self.output_name.GetValue()

        if not text_input:
            wx.MessageBox('Input cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        if not is_valid_windows_filename(output_name):
            wx.MessageBox('Invalid output name!', 'Error', wx.OK | wx.ICON_ERROR)
            return

        try:
            barcode_img = generate_numeric_barcodes(selected_type, text_input)
            path = f"{output_path}/{output_name}"
            barcode_img.save(path)
            wx.MessageBox(f'Image saved at {path}', 'Success', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
            return

if __name__ == "__main__":
    app = wx.App()
    frame = NumericLinearBarcodesEncoderWX(None)
    frame.SetTitle('Numeric Barcodes Encode with GUI')
    frame.SetSize((700, 350))
    frame.Show()
    app.MainLoop()
