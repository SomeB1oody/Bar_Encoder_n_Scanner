#Author: Stan Yin
#GitHub Name: SomeB1oody
#This project is based on CC 4.0 BY, please mention my name if you use it.
#This project requires opencv, pyzbar and wxWidgets.
import cv2
import wx
import numpy as np
from pyzbar.pyzbar import decode

def correct_perspective(img, original_img):
    # 查找轮廓
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 按轮廓面积从大到小排序，选择最大的轮廓
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(contours) == 0:
        raise ValueError("No outline was found in the image.")

    # 将最大的轮廓逼近为多边形
    epsilon = 0.02 * cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], epsilon, True)

    # 确保逼近后的多边形有 4 个点（即四边形）
    if len(approx) != 4:
        raise ValueError("The quadrilateral outline for perspective transformation could not be found.")

    # 获取四个角点
    pts = approx.reshape(4, 2)

    # 对角点进行排序：左上、右上、右下、左下
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # 左上角
    rect[2] = pts[np.argmax(s)]  # 右下角
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # 右上角
    rect[3] = pts[np.argmax(diff)]  # 左下角

    # 计算新图像的宽度和高度
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    # 目标图像的四个点位置（透视变换后的位置）
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    # 计算透视变换矩阵
    M = cv2.getPerspectiveTransform(rect, dst)

    # 应用透视变换
    warped = cv2.warpPerspective(original_img, M, (maxWidth, maxHeight))

    return warped

def convert_opencv_to_wx(opencv_image, BGR_or_GRAY):
    # 获取原始图像的高度和宽度
    height, width = opencv_image.shape[:2]

    # 使用高度和宽度来进行条件判断
    if height >= width:
        target_height = 300
        scale = target_height / height
        target_width = int(width * scale)
    else:
        target_width = 300
        scale = target_width / width
        target_height = int(height * scale)

    # 使用OpenCV调整图像大小
    resized_image = cv2.resize(opencv_image, (target_width, target_height))

    if BGR_or_GRAY == 'GRAY':
        # 转换颜色空间，从 GRAY 转换为 RGB
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    else:
        # 转换颜色空间，从 BGR 转换为 RGB
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # 将numpy数组转换为wx.Image
    height, width = rgb_image.shape[:2]
    wx_image = wx.Image(width, height)
    wx_image.SetData(rgb_image.tobytes())

    # 转换为wx.Bitmap
    wx_bitmap = wx_image.ConvertToBitmap()

    return wx_bitmap

def decode_qr_with_perspective_correction(cv_image):
    # 尝试直接解码二维码
    decoded_objects = decode(cv_image)
    if decoded_objects:
        return None, decoded_objects[0].data.decode('utf-8'), cv_image, True

    # 调整对比度和亮度
    contrast_image = cv2.convertScaleAbs(cv_image, alpha=1.8, beta=-30)

    # 将图像转换为灰度图
    gray_image = cv2.cvtColor(contrast_image, cv2.COLOR_BGR2GRAY)

    # 使用双边滤波以保留边缘并减少噪声
    filter_image = cv2.bilateralFilter(gray_image, 13, 26, 6)

    # 使用二值化处理（阈值210，最大值255）
    _, binary = cv2.threshold(filter_image, 210, 255, cv2.THRESH_BINARY_INV)

    # Canny
    edges = cv2.Canny(binary, 100, 200)

    # 膨胀
    kernel = np.ones((16, 16), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=5)

    try:
        warped_img = correct_perspective(dilated, filter_image)
        decoded_objects = decode(warped_img)
        if decoded_objects:
            return None, decoded_objects[0].data.decode('utf-8'), warped_img, False
    except ValueError as e:
        return str(e), None, None, None


class QRDecoder(wx.Frame):
    def __init__(self, *args, **kw):
        super(QRDecoder, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 输入路径
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.file_button = wx.Button(panel, label="Select image")
        self.Bind(wx.EVT_BUTTON, self.on_select_file, self.file_button)
        self.hbox.Add(self.file_button,flag=wx.ALL, border=5)
        self.input_path_text = wx.StaticText(panel, label="Click \"Select image\" first")
        self.hbox.Add(self.input_path_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox, flag=wx.EXPAND)
        # 解码按钮
        self.decode_button = wx.Button(panel, label="Decode")
        self.decode_button.Bind(wx.EVT_BUTTON, self.on_decode_button)
        self.vbox.Add(self.decode_button, flag=wx.ALL, border=5)
        # 解码内容
        self.result_text = wx.StaticText(panel, label="Click \"Decode\" first to get QR text.")
        self.vbox.Add(self.result_text, flag=wx.ALL, border=5)
        # 展示图片
        empty_image = wx.Image(300, 300)  # 创建一个空白的 wx.Image
        empty_image.Replace(0, 0, 0, 255, 255, 255)  # 将所有像素设为白色
        empty_bitmap = wx.Bitmap(empty_image)  # 将 wx.Image 转换为 wx.Bitmap
        self.img_show = wx.StaticBitmap(panel, bitmap=empty_bitmap)
        self.vbox.Add(self.img_show, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        # 设置面板的布局管理器
        panel.SetSizer(self.vbox)
        panel.Layout()

    def on_select_file(self, event):
        with wx.FileDialog(None, "Select a image", wildcard="所有文件 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.input_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_file = dialog.GetPath()

    def on_decode_button(self, event):
        path = self.selected_file
        if not path:
            wx.MessageBox("Please select a input file", "Error", wx.OK | wx.ICON_ERROR)
            return

        img = cv2.imread(path)
        if img is None:
            wx.MessageBox("Cannot load image", "Error", wx.OK | wx.ICON_ERROR)
            return

        # 使用透视校正和解码函数
        error_message, qr_text, corrected_image, flag = decode_qr_with_perspective_correction(img)

        if not qr_text:
            wx.MessageBox(f"{error_message}", "Error", wx.OK | wx.ICON_ERROR)
            return

        self.result_text.SetLabel(f"QR text is: {qr_text}")

        if flag:
            BGR_or_GRAY = 'BGR'
        else:
            BGR_or_GRAY = 'GRAY'

        # 可视化二维码检测区域
        try:
            img_ = convert_opencv_to_wx(corrected_image, BGR_or_GRAY)
            self.img_show.SetBitmap(img_)
        except Exception as e:
            wx.MessageBox(f"Fail to show image on GUI: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

        self.Refresh()



if __name__ == "__main__":
    app = wx.App()
    frame = QRDecoder(None)
    frame.SetTitle('Barcode Scanner')
    frame.SetSize((500, 450))
    frame.Show()
    app.MainLoop()