from pylibdmtx.pylibdmtx import encode
from PIL import Image
import re
import base64
import wx

MAX_LENGTH = 1556

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

# 读取文件并进行base64编码
def file_to_base64(filepath):
    with open(filepath, "rb") as file:
        encoded = base64.b64encode(file.read())
        return encoded.decode('utf-8')

def generate_datamatrix(data, encode_mode, size = 300):
    # 生成Data Matrix条码
    encoded = encode(data.encode(encode_mode))

    # 获取条码的原始宽度和高度
    width, height = encoded.width, encoded.height

    # 检查输入的 size 是否足够大
    if size < max(width, height):
        raise Exception(
        f"Specified size {size} is too small. It must be at least {max(width, height)} to accommodate the Data Matrix."
        )

    # 将生成的字节转换为图片
    image = Image.frombytes('RGB', (width, height), encoded.pixels)

    # 调整图片大小
    image = image.resize((size, size), Image.LANCZOS)

    # 返回图片
    return image

class DataMatrixEncoderWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(DataMatrixEncoderWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 选择文件输入还是字符输入
        self.text_or_file = wx.RadioBox(
            panel, label="Choose input type", choices=[
                'text', 'file(Max: 2,214 bytes)'
            ]
        )
        self.Bind(wx.EVT_RADIOBOX, self.input_type, self.text_or_file)
        self.vbox.Add(self.text_or_file, flag=wx.ALL, border=5)

        # 输入路径
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.file_button = wx.Button(panel, label="Select file")
        self.Bind(wx.EVT_BUTTON, self.on_select_file, self.file_button)
        self.hbox.Add(self.file_button,flag=wx.ALL, border=5)
        self.input_path_text = wx.StaticText(panel, label=
        "Click \"Select file\" first"
                                             )
        self.hbox.Add(self.input_path_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox, flag=wx.EXPAND)
        self.file_button.Enable(False)

        # 输入文本
        self.vbox.Add(wx.StaticText(panel, label=
        "Text input"), flag=wx.ALL, border=5)
        self.text_input = wx.TextCtrl(panel)
        self.Bind(wx.EVT_TEXT, self.on_text_input, self.text_input)
        self.vbox.Add(self.text_input, flag=wx.EXPAND | wx.ALL, border=5)

        # 编码格式单选框
        self.encode_mode = wx.RadioBox(
            panel, label="Choose encode mode:", choices=[
                'utf-8', 'base64', 'iso-8859-1(Latin-1)', 'ascii', 'Shift JIS5 (Japanese)', 'GB2312', 'GBK', 'GB18030'
            ],
            majorDimension=5,  # 每列5个选项
            style=wx.RA_SPECIFY_COLS  # 指定为按列排列
        )
        self.vbox.Add(self.encode_mode, flag=wx.ALL, border=5)

        # 生成按钮
        self.generate_button = wx.Button(panel, label="Generate")
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        self.vbox.Add(self.generate_button, flag=wx.ALL, border=5)

        # 尺寸
        self.size_text = wx.StaticText(panel, label="Image size(pixel):")
        self.vbox.Add(self.size_text, flag=wx.ALL, border=5)
        self.img_size = wx.TextCtrl(panel)
        self.Bind(wx.EVT_TEXT, self.input_check_size, self.img_size)
        self.vbox.Add(self.img_size, flag=wx.EXPAND | wx.ALL, border=5)

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

    def input_type(self, event):
        input_type = self.text_or_file.GetStringSelection()
        if input_type == 'text':
            self.file_button.Enable(False)
            self.input_path_text.SetLabel("Select \"file\" to enable button")
            self.text_input.Enable(True)
            self.encode_mode.Enable(True)
        else:
            self.text_input.Enable(False)
            self.file_button.Enable(True)
            self.encode_mode.Enable(False)
            self.encode_mode.SetSelection(1)

    def on_select_file(self, event):
        with wx.FileDialog(None, "Select a file", wildcard="所有文件 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.input_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_file = dialog.GetPath()
                data_length = len(file_to_base64(self.selected_file))
                if data_length > MAX_LENGTH:
                    wx.MessageBox('Input data too big', 'Error', wx.OK | wx.ICON_ERROR)
                    return

    def on_text_input(self, event):
        if len(self.text_input.GetValue()) > MAX_LENGTH:
            wx.MessageBox('Input data too big', 'Error', wx.OK | wx.ICON_ERROR)
            return

    def on_generate_button(self, event):
        input_type = self.text_or_file.GetStringSelection()
        if input_type == 'text':
            input_data = self.text_input.GetValue()
        else:
            input_data = file_to_base64(self.selected_file)

        encode_mode = self.encode_mode.GetSelection()
        match encode_mode:
            case 'utf-8': encode_mode = 'utf-8'
            case 'base64': encode_mode = 'utf-8'
            case 'iso-8859-1(Latin-1)': encode_mode = 'iso-8859-1'
            case 'ascii': encode_mode = 'ascii'
            case 'Shift JIS5 (Japanese)': encode_mode = 'Shift JIS5'
            case 'GB2312': encode_mode = 'gb2312'
            case 'GBK': encode_mode = 'gbk'
            case 'GB18030': encode_mode = 'gb18030'
            case _: encode_mode = 'utf-8'

        if not input_data:
            wx.MessageBox('Input data cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        img = generate_datamatrix(input_data, encode_mode)
        img.show()

    def input_check_size(self, event):
        input_ = event.GetString()
        if not input_.isdigit() or int(input_) == 0:
            wx.MessageBox(
                'Size should be a Non-zero positive integer', 'Error', wx.OK | wx.ICON_ERROR)
            return
        self.size_text.SetLabel(f"Image size(pixel): {input_} x {input_}")

    def on_select_folder(self, event):
        with wx.DirDialog(None, "Select a folder for output", "",
                          style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.output_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_folder = dialog.GetPath()

    def on_save_button(self, event):
        input_type = self.text_or_file.GetStringSelection()
        if input_type == 'text':
            input_ = self.text_input.GetValue()
        else:
            input_ = file_to_base64(self.selected_file)
        size = self.img_size.GetValue()
        output_path = self.selected_folder
        output_name = self.output_name.GetValue()
        output_format = self.output_format.GetStringSelection()
        encode_mode = self.encode_mode.GetSelection()

        match encode_mode:
            case 'utf-8': encode_mode = 'utf-8'
            case 'base64': encode_mode = 'utf-8'
            case 'iso-8859-1(Latin-1)': encode_mode = 'iso-8859-1'
            case 'ascii': encode_mode = 'ascii'
            case 'Shift JIS5 (Japanese)': encode_mode = 'Shift JIS5'
            case 'GB2312': encode_mode = 'gb2312'
            case 'GBK': encode_mode = 'gbk'
            case 'GB18030': encode_mode = 'gb18030'
            case _: encode_mode = 'utf-8'

        if not input_:
            wx.MessageBox('Input data cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not size:
            wx.MessageBox('Size cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not output_path:
            wx.MessageBox('Output path cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not is_valid_windows_filename(output_name):
            wx.MessageBox('Output name invalid, try another one', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not output_name:
            wx.MessageBox('Output name cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        path = f'{output_path}/{output_name}{output_format}'

        try:
            img = generate_datamatrix(input_, encode_mode, int(size))
            img.save(path)
            wx.MessageBox(f'Image saved at{path}', 'Success', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App()
    frame = DataMatrixEncoderWX(None)
    frame.SetTitle('DataMatrix Encoder GUI')
    frame.SetSize((750, 600))
    frame.Show()
    app.MainLoop()