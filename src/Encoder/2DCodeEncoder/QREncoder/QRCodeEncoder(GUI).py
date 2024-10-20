#Author: Stan Yin
#GitHub Name: SomeB1oody
#This project is based on CC 4.0 BY, please mention my name if you use it.
#This project requires opencv, PIL, qrcode, numpy, base64 and wxWidgets.
import wx
import qrcode
import base64
from PIL import Image
import numpy as np
import cv2

# 读取文件并进行base64编码
def file_to_base64(filepath):
    with open(filepath, "rb") as file:
        encoded = base64.b64encode(file.read())
        return encoded.decode('utf-8')

def get_error_correction_level(level):
    match level:
        case 'Low(7%)': return qrcode.constants.ERROR_CORRECT_L
        case 'Medium(15%)': return qrcode.constants.ERROR_CORRECT_M
        case 'Quartile(25%)': return qrcode.constants.ERROR_CORRECT_Q
        case 'High(30%)': return qrcode.constants.ERROR_CORRECT_H
        case _: return None

def calculate_min_size(data, error_correction, border=4):
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

def generate_qr_code(data, error_correction, size=400, border=4):
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

    return img

def pil_to_opencv_gray(pil_image):
    pil_image = pil_image.convert('L')
    opencv_image = np.array(pil_image)
    return opencv_image

class QREncoderWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(QREncoderWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 输出格式单选框
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

        # 输入文本
        self.vbox.Add(wx.StaticText(panel, label=
        "Text input"), flag=wx.ALL, border=5)
        self.text_input = wx.TextCtrl(panel)
        self.Bind(wx.EVT_TEXT, self.get_available_error_correction_options, self.text_input)
        self.vbox.Add(self.text_input, flag=wx.EXPAND | wx.ALL, border=5)

        # 选择容错率
        self.F_rate_choice = ['Low(7%)', 'Medium(15%)', 'Quartile(25%)', 'High(30%)']
        self.F_rate = wx.RadioBox(panel, label="Choose a fault tolerance rate", choices=self.F_rate_choice)
        self.vbox.Add(self.F_rate, flag=wx.ALL, border=5)

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

        # 边界
        self.vbox.Add(wx.StaticText(panel, label=
        "Broader(at least 4 is recommended)"), flag=wx.ALL, border=5)
        self.broader_size = wx.TextCtrl(panel)
        self.Bind(wx.EVT_TEXT, self.input_check_broader, self.broader_size)
        self.vbox.Add(self.broader_size, flag=wx.EXPAND | wx.ALL, border=5)

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
        else:
            self.text_input.Enable(False)
            self.file_button.Enable(True)

    def on_select_file(self, event):
        with wx.FileDialog(None, "Select a image", wildcard="所有文件 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.input_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_file = dialog.GetPath()
                data_length = len(file_to_base64(self.selected_file))
                if data_length > 2953:
                    wx.MessageBox('Input data too big', 'Error', wx.OK | wx.ICON_ERROR)
                    return

            self.F_rate_choice = []
            if data_length <= 2953:
                self.F_rate_choice.append('Low(7%)')
            if data_length <= 2231:
                self.F_rate_choice.append('Medium(15%)')
            if data_length <= 1663:
                self.F_rate_choice.append('Quartile(25%)')
            if data_length <= 1273:
                self.F_rate_choice.append('High(30%)')

    def get_available_error_correction_options(self, event):
        data_length = len(self.text_input.GetValue())
        if data_length > 2953:
            wx.MessageBox('Input data too big', 'Error', wx.OK | wx.ICON_ERROR)
            return

        self.F_rate_choice = []
        if data_length <= 2953:
            self.F_rate_choice.append('Low(7%)')
        if data_length <= 2231:
            self.F_rate_choice.append('Medium(15%)')
        if data_length <= 1663:
            self.F_rate_choice.append('Quartile(25%)')
        if data_length <= 1273:
            self.F_rate_choice.append('High(30%)')

    def on_generate_button(self, event):
        input_type = self.text_or_file.GetStringSelection()
        if input_type == 'text':
            input_ = self.text_input.GetValue()
        else:
            input_ = file_to_base64(self.selected_file)

        if not input_:
            wx.MessageBox('Input data cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        F_rate = self.F_rate.GetStringSelection()
        img = generate_qr_code(input_, F_rate)

        cv_img = pil_to_opencv_gray(img)
        cv2.imshow("Code", cv_img)
        cv2.waitKey(0)

    def input_check_size(self, event):
        input_ = event.GetString()
        if not input_.isdigit() or int(input_) == 0:
            wx.MessageBox(
            'Size should be a Non-zero positive integer', 'Error', wx.OK | wx.ICON_ERROR)
            return
        self.size_text.SetLabel(f"Image size(pixel): {input_} x {input_}")

    def input_check_broader(self, event):
        input_ = event.GetString()
        if not input_.isdigit() or int(input_) == 0:
            wx.MessageBox(
            'Broader should be a Non-zero positive integer', 'Error', wx.OK | wx.ICON_ERROR)
            return

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
        broader = self.broader_size.GetValue()
        output_path = self.selected_folder
        output_name = self.output_name.GetValue()
        output_format = self.output_format.GetStringSelection()
        F_rate = self.F_rate.GetStringSelection()

        if not input_:
            wx.MessageBox('Input data cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not size:
            wx.MessageBox('Size cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not broader:
            wx.MessageBox('Broader size cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not output_path:
            wx.MessageBox('Output path cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if not output_name:
            wx.MessageBox('Output name cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        path = f'{output_path}/{output_name}{output_format}'

        try:
            img = generate_qr_code(input_, F_rate, int(size), int(broader))
        except ValueError as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
            return

        try:
            cv_img = pil_to_opencv_gray(img)
            cv2.imwrite(path, cv_img)
            wx.MessageBox(f'Image saved at {path}', 'Success', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
            return



if __name__ == "__main__":
    app = wx.App()
    frame = QREncoderWX(None)
    frame.SetTitle('QR Encoder with GUI')
    frame.SetSize((800, 700))
    frame.Show()
    app.MainLoop()
