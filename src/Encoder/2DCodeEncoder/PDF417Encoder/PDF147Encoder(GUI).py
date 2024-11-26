import wx
from pdf417gen import encode, render_image
import re

def generate_pdf417(data):
    # 对输入数据进行编码
    codes = encode(data)

    if not codes:
        raise ValueError("Cannot generate PDF417")

    # 渲染条码为图片
    image = render_image(codes)

    return image

def input_process(input_, encode_mode):
    match encode_mode:
        case 'utf-8':
            data = input_.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        case 'iso-8859-1(Latin-1)':
            data = input_.encode('iso-8859-1', errors='ignore').decode('iso-8859-1', errors='ignore')
        case 'ascii':
            data = input_.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
        case 'Shift JIS5 (Japanese)':
            data = input_.encode('shift_jis5', errors='ignore').decode('shift_jis5', errors='ignore')
        case 'GB2312':
            data = input_.encode('gb2312', errors='ignore').decode('gb2312', errors='ignore')
        case 'GBK':
            data = input_.encode('gbk', errors='ignore').decode('gbk', errors='ignore')
        case 'GB18030':
            data = input_.encode('gb18030', errors='ignore').decode('gb18030', errors='ignore')
        case _:
            data = input_.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

    return data

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

class PDF417EncoderWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(PDF417EncoderWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 输入文本
        self.vbox.Add(wx.StaticText(panel, label=
        "Text input"), flag=wx.ALL, border=5)
        self.text_input = wx.TextCtrl(panel)
        self.Bind(wx.EVT_TEXT, self.on_text_input, self.text_input)
        self.vbox.Add(self.text_input, flag=wx.EXPAND | wx.ALL, border=5)

        # 编码格式单选框
        self.encode_mode = wx.RadioBox(
            panel, label="Choose encode mode:", choices=[
                'utf-8', 'iso-8859-1(Latin-1)', 'ascii', 'Shift JIS5 (Japanese)', 'GB2312', 'GBK', 'GB18030'
            ],
            majorDimension=5,  # 每列5个选项
            style=wx.RA_SPECIFY_COLS  # 指定为按列排列
        )
        self.vbox.Add(self.encode_mode, flag=wx.ALL, border=5)

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

    def on_text_input(self, event):
        data_length = len(input_process(self.text_input.GetValue(), self.encode_mode.GetStringSelection()))
        if data_length > 1850:
            wx.MessageBox('Input too large!', 'Error', wx.OK | wx.ICON_ERROR)
            return

    def on_generate_button(self, event):
        data = self.text_input.GetValue()

        if not data:
            wx.MessageBox('Input data cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        data_ = input_process(data, self.encode_mode.GetStringSelection())

        img = generate_pdf417(data_)
        img.show()

    def on_select_folder(self, event):
        with wx.DirDialog(None, "Select a folder for output", "",
                          style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.output_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_folder = dialog.GetPath()

    def on_save_button(self, event):
        data = self.text_input.GetValue()
        output_path = self.selected_folder
        output_name = self.output_name.GetValue()
        output_format = self.output_format.GetStringSelection()
        encode_mode = self.encode_mode.GetSelection()

        if not data:
            wx.MessageBox('Input data cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
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

        data_ = input_process(data, encode_mode)

        try:
            img = generate_pdf417(data_)
            img.save(path)
            wx.MessageBox(f'Image saved at {path}', 'Success', wx.OK | wx.ICON_INFORMATION)
        except ValueError as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
            return



if __name__ == "__main__":
    app = wx.App()
    frame = PDF417EncoderWX(None)
    frame.SetTitle('PDF417 Encoder with GUI')
    frame.SetSize((750, 450))
    frame.Show()
    app.MainLoop()
