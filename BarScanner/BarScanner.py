#Author: Stan Yin
#GitHub Name: SomeB1oody
#This project is based on CC 4.0 BY, please mention my name if you use it.
#This project requires opencv, numpy, wxWidgets and pyzbar.
import cv2
import numpy as np
from pyzbar import pyzbar
import wx

def cv2_to_wx_image(cv_img):
    # OpenCV 图像是 BGR 形式的，先将其转换为 RGB
    cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

    # 获取图像的尺寸（高度、宽度、通道数）
    height, width = cv_img_rgb.shape[:2]

    # 将 NumPy 数组转换为 wx.Image
    wx_img = wx.Image(width, height)

    # 将 NumPy 数据复制到 wx.Image
    wx_img.SetData(cv_img_rgb.tobytes())

    return wx_img

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def detect_barcode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用高斯模糊来减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用Sobel算子来计算图像的梯度
    gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # 计算梯度的绝对值，并相减以突出条形码的竖直部分
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # 对梯度图像进行模糊和二值化处理
    blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
    _, thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # 使用形态学操作关闭小的黑点并突出条形码区域
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 对图像进行腐蚀和膨胀操作
    closed = cv2.erode(closed, kernal=None, iterations=4)
    closed = cv2.dilate(closed, kernnal=None, iterations=4)

    # 找到轮廓
    contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 如果找到任何轮廓，筛选出面积最大的轮廓
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)

        # 获取轮廓的边界框
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.array(box, dtype="int")

        # 对边界框点进行排序
        box = order_points(box)

        # 透视变换矫正图像
        warped = four_point_transform(image, box)

        # 使用 pyzbar 解码条形码
        barcodes = pyzbar.decode(warped)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            print(f"找到条形码： 类型={barcode_type}, 数据={barcode_data}")
            return warped, barcode_data

    return None, None

class BarScanner(wx.Frame):
    def __init__(self, *args, **kw):
        super(BarScanner, self).__init__(*args, **kw)

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
            wx.MessageBox("Please enter image path.", "Error", wx.OK | wx.ICON_ERROR)
            return
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            wx.MessageBox("Cannot load image.", "Error", wx.OK | wx.ICON_ERROR)
            return
        warped_img, text = detect_barcode(img)
        if warped_img is None:
            wx.MessageBox("Cannot find Bar code.", "Error", wx.OK | wx.ICON_ERROR)
            return
        else:
            self.result_text.SetLabel(f"Bar text is: {text}")
            try:
                width_ = warped_img.GetWidth() * (300 // warped_img.GetHeight())
                img_ = warped_img.Scale(width_, 300, wx.IMAGE_QUALITY_HIGH)
                bitmap = wx.Bitmap(img_)
                self.img_show.SetBitmap(bitmap)
            except Exception as e:
                wx.MessageBox(f"Fail to show image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            self.Refresh()


if __name__ == "__main__":
    app = wx.App()
    frame = BarScanner(None)
    frame.SetTitle('SimilarityFinder')
    frame.SetSize((500, 450))
    frame.Show()
    app.MainLoop()