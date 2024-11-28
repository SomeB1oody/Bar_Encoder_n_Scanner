
# Barcode Master
*Fully functional barcode (1D/2D) processor*
*完全功能的条形码（1D/2D）处理器*

---
## 0. Table of Content 目录
- 1.Intro 简介
- 2.Functions 功能
- 3.Examples 实例
- 4.Required environment 要求环境
- 5.Contribution 贡献
- 6.License 证书
- 7.Contact information 联系方式

---
## 1.Intro 简介

**Barcode Master** is a lightweight 1D/2D barcode processor using Python wxWidgets as the frontend. Whether it's encoding, decoding, or recognition (with built-in perspective transformation), you can find corresponding solutions in this project. The currently supported barcode formats include: Code39, Code128, UPC, EAN13, EAN8, ITF, PZN, JAN, DataMatrix, PDF417, QR Code, and GS1.
**Barcode Master** 是一个轻量级的1D/2D条形码处理器，使用Python的wxWidgets作为前端。无论是编码、解码还是识别（包含内置透视变换），都可以在这个项目中找到相应的解决方案。目前支持的条形码格式包括：Code39、Code128、UPC、EAN13、EAN8、ITF、PZN、JAN、DataMatrix、PDF417、QR Code和GS1。

Each program comes with both a non-GUI and a GUI version. The non-GUI version offers the simplest operations and code, making it easier to understand. The GUI version supports more complex operations, providing a more advanced and user-friendly experience.
每个程序都提供了GUI和非GUI版本。非GUI版本提供最简单的操作和代码，更易于理解；而GUI版本支持更复杂的操作，提供更先进且用户友好的体验。

Due to my limited capabilities, the code may have some imperfections. I warmly welcome everyone to share their suggestions and contribute to the project. For more details, please see the  Contribution. Thank you for your understanding!
由于个人能力有限，代码可能存在一些不足，热烈欢迎大家分享建议并为项目做出贡献。详细信息请参考 5.贡献方式。感谢您的理解！

---
### 2. Functions 功能

### 2.1. Structure 结构

This is the sturcture of this project:
这是这个项目的结构图：

![Structure](https://github.com/user-attachments/assets/a4f7dab6-1c17-4f03-aaae-1ec70961064c)

### 2.2. Info about 1DEncoder
**1DEncoder** provides support for one-dimensional barcodes, including the following formats: Code39, Code128, UPC, EAN13, EAN8, ITF, PZN, and JAN.
**1DEncoder** 提供对一维条形码的支持，包括以下格式：Code39、Code128、UPC、EAN13、EAN8、ITF、PZN 和 JAN。

#### 2.2.1. AlphanumericBarcodesEncoder
**AlphanumericBarcodesEncoder** supports the Code39 and Code128 barcode formats, both of which allow alphanumeric character input.
**AlphanumericBarcodesEncoder** 支持 Code39 和 Code128 条形码格式，这两种格式都允许输入字母数字字符。

##### 2.2.2. NumericLinearBarcodesEncoder
**NumericLinearBarcodesEncoder** provides support for one-dimensional barcodes with purely numeric input, including formats such as UPC, EAN13, EAN8, ITF, PZN, and JAN.
**NumericLinearBarcodesEncoder** 支持仅使用数字输入的一维条形码格式，包括：UPC、EAN13、EAN8、ITF、PZN 和 JAN。

### 2.3. Info about 2DEncoder
**2DEncoder** provides support for two-dimensional barcodes, including the following formats: DataMatrix, PDF417, QR Code.
**2DEncoder** 提供对二维条形码的支持，包括以下格式：DataMatrix、PDF417、QR Code。

### 2.4. Info about GS1Encoder
Given that **GS1** is more of a standardized identification and data exchange encoding standard rather than a carrier, its carriers include both 1D and 2D barcodes. Therefore, it is listed separately. The program provides support for formats such as EAN13, UPCA, Code128, QR Code, and DataMatrix.
由于 **GS1** 更多是一个标准化的标识和数据交换编码标准，而不是一个载体，其载体包括一维和二维条形码。因此，GS1 被单独列出。该程序支持的格式包括：EAN13、UPCA、Code128、QR Code 和 DataMatrix。

---
## 3.Examples 实例

 [AlphanumericBarcodesEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/AlphanumericBarcodesEncoder/AlphanumericBarcodesEncoder(GUI).py):
![code39](https://github.com/user-attachments/assets/23ca7626-abd8-4d6e-b36c-76b2ed578c08)



[NumericLinearBarcodesEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/NumericLinearBarcodesEncoder/NumericLinearBarcodesEncoder(GUI).py):
![upc](https://github.com/user-attachments/assets/0b03af3a-e4df-4f81-96ea-8518385e7c49)


 [DataMatrixEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/DataMatrixEncoder/DataMatrixEncoder(GUI).py):
![datamatrix](https://github.com/user-attachments/assets/5c4abb14-4f14-494f-8a64-bec9db1d445a)


 [PDF417Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/PDF417Encoder):
![pdf417](https://github.com/user-attachments/assets/70e44b17-cdf1-4551-b038-27af2e64fe07)


[QREncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/QREncoder):
![qr](https://github.com/user-attachments/assets/143ab5a3-4c1f-4f20-bdce-4d0a371402f0)


 [GS1Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/GS1Encoder):
![gs1_1d_ean13](https://github.com/user-attachments/assets/904c119c-1923-49d3-aff8-6966cda08c68)

![gs1_2d_qr](https://github.com/user-attachments/assets/8aa1014e-76b4-421f-be0b-61f66fe2da03)


 [Scanner](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Scanner):
![ScanTest1](https://github.com/user-attachments/assets/f93ec4bd-219f-4cc0-b284-173ba627393f)
![ScanTest2](https://github.com/user-attachments/assets/4fca16b6-eec1-48de-ad8b-7d8bdfeb6d98)


All of the screenshots and example ouput barcodes can be found at [BarcodeMaster/tests/Screenshots](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/Screenshots), [BarcodeMaster/tests/Output](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/Output) and [BarcodeMaster/tests/ScanTest](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/ScanTest)


---
## 4. Required environment 要求环境

Below is a list of libraries used in the project, organized based on the project structure. Libraries marked with (only for GUI version) are only used in the GUI version. If you are not using the GUI version, you do not need to check whether these libraries are installed.
以下是项目中使用的库列表，按项目结构组织。标注为“==（仅适用于GUI版本）==”的库仅用于GUI版本，如果不使用GUI版本，则无需检查这些库是否已安装。

![environment](https://github.com/user-attachments/assets/4b3fd6f9-889b-4928-94df-04a3002a1578)


Python version should be at least 3.10
Python 版本需至少为 3.10。

You can also directly execute the following installation command, which includes all the required libraries:
您还可以直接执行以下命令安装所有所需库：
```bash
pip install python-barcode
pip install wxPython
pip install Pillow
pip install pylibdmtx
pip install qrcode
pip install pdf417gen
pip install numpy
pip install opencv-python
pip install pyzbar
```
---
## 5. Contribution 贡献

Contributions are welcome! Follow these steps:
欢迎贡献！请按照以下步骤操作：
 - 1. Fork project.
      Fork 项目。
 - 2. Create branch:
      创建分支：
 ```bash
 git checkout -b feature-name
```
- 3. Submit changes:
     提交更改：
```bash
git commit -m "Explain changes"
```
- 4. Push branch:
     推送分支：
```bash
git push orgin feature-name
```
- 5. Submit Pull Request.
     提交拉取请求。
---
## 6. License 证书

This project uses [MIT LICENSE](https://github.com/SomeB1oody/BarcodeMaster/blob/main/LICENSE.md).
此项目使用[MIT LICENSE](https://github.com/SomeB1oody/BarcodeMaster/blob/main/LICENSE.md).

---
## 7. Contact information 联系方式

- Email: stanyin64@gmail.com
- GitHub: [@SomeB1ooody](https://github.com/SomeB1oody)
