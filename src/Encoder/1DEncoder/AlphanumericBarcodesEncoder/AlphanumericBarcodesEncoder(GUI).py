import barcode
from barcode.writer import ImageWriter
import wx
import re
from io import BytesIO
from PIL import Image

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
def generate_barcode(data, barcode_format):
    # 验证输入数据
    if not validate_input(data, barcode_format.lower()):
        if barcode_format.lower() == 'code39':
            wx.MessageBox('Invalid input, Code39 only support uppercase letters, numbers, and -.$/+% Spaces',
            'Error', wx.OK | wx.ICON_ERROR)
            return
        if barcode_format.lower() == 'code128':
            wx.MessageBox('Invalid input, Code128 only support Ascii','Error', wx.OK | wx.ICON_ERROR)
            return

    # 创建条形码对象并生成图像
    barcode_class = barcode.get_barcode_class(barcode_format)
    barcode_obj = barcode_class(data, writer=ImageWriter())

    return barcode_obj

class AlphanumericBarcodesEncoderWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(AlphanumericBarcodesEncoderWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 选择格式
        self.code39_or_128 = wx.RadioBox(
            panel, label="Choose input type", choices=[
                'Code39', 'Code128'
            ]
        )
        self.vbox.Add(self.code39_or_128, flag=wx.ALL, border=5)

        # 输入文本
        self.vbox.Add(wx.StaticText(panel, label=
        "Text input"), flag=wx.ALL, border=5)
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

    def on_select_folder(self, event):
        with wx.DirDialog(None, "Select a folder for output", "",
                          style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.output_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_folder = dialog.GetPath()

    def on_generate_button(self, event):
        code39_or_128 = self.code39_or_128.GetStringSelection().lower()
        text_input = self.text_input.GetValue()

        if not text_input:
            wx.MessageBox('input cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        barcode_ = generate_barcode(text_input, code39_or_128)
        # 使用 BytesIO 将条形码保存到内存中
        buffer = BytesIO()
        barcode_.write(buffer)

        # 使用 Pillow 显示条形码图像
        image = Image.open(buffer)
        image.show()

    def on_save_button(self, event):
        code39_or_128 = self.code39_or_128.GetStringSelection().lower()
        text_input = self.text_input.GetValue()
        selected_folder = self.selected_folder
        output_format = self.output_format.GetStringSelection()
        output_name = self.output_name.GetValue()

        if not text_input:
            wx.MessageBox('input cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not selected_folder:
            wx.MessageBox('Select output folder first', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not is_valid_windows_filename(output_name):
            wx.MessageBox('Invalid filename', 'Error', wx.OK | wx.ICON_ERROR)
            return

        path = f'{selected_folder}/{output_name}.{output_format}'

        barcode_ = generate_barcode(text_input, code39_or_128)

        try:
            barcode_.save(path)
            wx.MessageBox(f'Image saved at {path}', 'Success', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
            return



if __name__ == "__main__":
    app = wx.App()
    frame = AlphanumericBarcodesEncoderWX(None)
    frame.SetTitle('Alphanumeric Barcodes Encode with GUI')
    frame.SetSize((700, 350))
    frame.Show()
    app.MainLoop()
