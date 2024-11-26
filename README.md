
# Barcode Master
*Fully functional barcode (1D/2D) processor*

---
## 0. Table of Content
- [[README#1.Intro]]
- [[README#2. Functions]]
- [[README#3.Examples]]
- [[README#4. Required environment]]
- [[README#5. Contribution]]
- [[README#6. Liscence]]
- [[README#7. Contact information]]

---
## 1.Intro

**Barcode Master** is a lightweight 1D/2D barcode processor using Python wxWidgets as the frontend. Whether it's encoding, decoding, or recognition (with built-in perspective transformation), you can find corresponding solutions in this project. The currently supported barcode formats include: Code39, Code128, UPC, EAN13, EAN8, ITF, PZN, JAN, DataMatrix, PDF417, QR Code, and GS1.

Each program comes with both a non-GUI and a GUI version. The non-GUI version offers the simplest operations and code, making it easier to understand. The GUI version supports more complex operations, providing a more advanced and user-friendly experience.

Due to my limited capabilities, the code may have some imperfections. I warmly welcome everyone to share their suggestions and contribute to the project. For more details, please see the [[README#4. Contribution]]. Thank you for your understanding!

---
### 2. Functions

### 2.1. Structure

This is the sturcture of this project:

[BarcodeMaste](https://github.com/SomeB1oody/BarcodeMaster)/
|- [src](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src)/
|     |- [Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder)/
|     |         |- [1DEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/1DEncoder)/
|     |         |            |- [AlphanumericBarcodesEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/1DEncoder/AlphanumericBarcodesEncoder)/
|     |         |            |                         |- [AlphanumericBarcodesEncoder.py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/AlphanumericBarcodesEncoder/AlphanumericBarcodesEncoder.py)
|     |         |            |                         |- [AlphanumericBarcodesEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/AlphanumericBarcodesEncoder/AlphanumericBarcodesEncoder(GUI).py)
|     |         |            |- [NumericLinearBarcodesEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/1DEncoder/NumericLinearBarcodesEncoder)
|     |         |                                      |- [NumericLinearBarcodesEncoder.py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/NumericLinearBarcodesEncoder/NumericLinearBarcodesEncoder.py)
|     |         |                                      |- [NumericLinearBarcodesEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/NumericLinearBarcodesEncoder/NumericLinearBarcodesEncoder(GUI).py)/
|     |         |- [2DEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder)/
|     |         |             |- [DataMatrixEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/DataMatrixEncoder)/
|     |         |             |                 |- [DataMatrixEncoder.py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/DataMatrixEncoder/DataMatrixEncoder.py)
|     |         |             |                 |- [DataMatrixEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/DataMatrixEncoder/DataMatrixEncoder(GUI).py)
|     |         |             |- [PDF417Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/PDF417Encoder)/
|     |         |             |                 |- [PDF417Encoder.py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/PDF417Encoder/PDF417Encoder.py)
|     |         |             |                 |- [PDF147Encoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/PDF417Encoder/PDF147Encoder(GUI).py)
|     |         |             |- [QREncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/QREncoder)/
|     |         |                         |- [QRCodeEncoder.py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/QREncoder/QRCodeEncoder.py)
|     |         |                         |- [QRCodeEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/QREncoder/QRCodeEncoder(GUI).py)
|     |         |- [GS1Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/GS1Encoder)/
|     |                       |- [GS1Encoder.py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/GS1Encoder/GS1Encoder.py)
|     |                       |- [GS1Encoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/GS1Encoder/GS1Encoder(GUI).py)
|     |- [Scanner](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Scanner)/
|              |- [Scanner.py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Scanner/Scanner.py)
|- [test](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests)/
|     |-[ Output](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/Output)/
|     |        |- [code39_wcnm.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Output/code39_wcnm.png)
|     |        |- [datamatrix_example.jpg](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Output/datamatrix_example.jpg)
|     |        |- [gs1_1d_ean13_example.jpg](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Output/gs1_1d_ean13_example.jpg)
|     |        |- [gs1_2d_qr_example.jpg](http://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Output/gs1_2d_qr_example.jpg)
|     |        |- [pdf417_example.jpg](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Output/pdf417_example.jpg)
|     |        |- [qr_example.jpg](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Output/qr_example.jpg)
|     |        |- [upc_114514191981.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Output/upc_114514191981.png)
|     |- [ScanTest](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/ScanTest)/
|     |        |- [qr_test_1.jpg](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/ScanTest/qr_test_1.jpg)
|     |        |- [qr_test_2.jpg](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/ScanTest/qr_test_2.jpg)
|     |        |- [results](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/ScanTest/results)/
|     |                 |- [qr1_result.txt](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/ScanTest/results/qr1_result.txt)
|     |                 |- [qr2_reslut.txt](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/ScanTest/results/qr2_result.txt)
|     |-[ Screenshots](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/Screenshots)/
|     |        |-[ code39.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/code39.png)
|     |        |- [datamatrix.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/datamatrix.png)
|     |        |- [gs1_1d_ean13.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/gs1_1d_ean13.png)
|     |        |- [gs1_2d_qr.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/gs1_2d_qr.png)
|     |        |- [pdf417.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/pdf417.png)
|     |        |- [qr.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/qr.png)
|     |        |- [ScanTest1.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/ScanTest1.png)
|     |        |-[ ScanTest2.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/ScanTest2.png)
|     |        |- [upc.png](https://github.com/SomeB1oody/BarcodeMaster/blob/main/tests/Screenshots/upc.png)
|- README.md
\ - LISCENCE.md

### 2.2. Info about 1DEncoder
**1DEncoder** provides support for one-dimensional barcodes, including the following formats: Code39, Code128, UPC, EAN13, EAN8, ITF, PZN, and JAN.

#### 2.2.1. AlphanumericBarcodesEncoder
**AlphanumericBarcodesEncoder** supports the Code39 and Code128 barcode formats, both of which allow alphanumeric character input.

##### 2.2.2. NumericLinearBarcodesEncoder
**NumericLinearBarcodesEncoder** provides support for one-dimensional barcodes with purely numeric input, including formats such as UPC, EAN13, EAN8, ITF, PZN, and JAN.

### 2.3. Info about 2DEncoder
**2DEncoder** provides support for two-dimensional barcodes, including the following formats: DataMatrix, PDF417, QR Code.

### 2.4. Info about GS1Encoder
Given that **GS1** is more of a standardized identification and data exchange encoding standard rather than a carrier, its carriers include both 1D and 2D barcodes. Therefore, it is listed separately. The program provides support for formats such as EAN13, UPCA, Code128, QR Code, and DataMatrix.

---
## 3.Examples

 [AlphanumericBarcodesEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/AlphanumericBarcodesEncoder/AlphanumericBarcodesEncoder(GUI).py):
![[code39.png]]


[NumericLinearBarcodesEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/1DEncoder/NumericLinearBarcodesEncoder/NumericLinearBarcodesEncoder(GUI).py):
![[upc.png]]


 [DataMatrixEncoder(GUI).py](https://github.com/SomeB1oody/BarcodeMaster/blob/main/src/Encoder/2DCodeEncoder/DataMatrixEncoder/DataMatrixEncoder(GUI).py):![[datamatrix.png]]


 [PDF417Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/PDF417Encoder):![[pdf417.png]]


[QREncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/QREncoder):
![[qr.png]]


 [GS1Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/GS1Encoder):
![[gs1_1d_ean13.png]]
![[gs1_2d_qr.png]]


 [Scanner](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Scanner):![[ScanTest1.png]]
![[ScanTest2.png]]
All of the screenshots and example ouput barcodes can be found at [BarcodeMaster/tests/Screenshots](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/Screenshots), [BarcodeMaster/tests/Output](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/Output) and [BarcodeMaster/tests/ScanTest](https://github.com/SomeB1oody/BarcodeMaster/tree/main/tests/ScanTest)


---
## 4. Required environment

Below is a list of libraries used in the project, organized based on the project structure. Libraries marked with ==(only for GUI version)== are only used in the GUI version. If you are not using the GUI version, you do not need to check whether these libraries are installed.

[BarcodeMaste](https://github.com/SomeB1oody/BarcodeMaster)/
|- [src](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src)/
 |- [Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder)/
 |         |- [1DEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/1DEncoder)/
 |         |            |- python-barcode
 |         |            |- wxPython ==(only for GUI version)==
 |         |            |- re ==(only for GUI version)==
 |         |            |- io ==(only for GUI version)==
 |         |            |- Pillow ==(only for GUI version)==
 |         |- [2DEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder)/
 |         |             |- [DataMatrixEncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/DataMatrixEncoder)/
 |         |             |                 |- pylibdmtx
 |         |             |                 |- Pillow 
 |         |             |                 |- re
 |         |             |                 |- wxPython ==(only for GUI version)==
 |         |             |- [PDF417Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/PDF417Encoder)/
 |         |             |                 |- pdf417gen
 |         |             |                 |- re
 |         |             |                 |- wxPython ==(only for GUI version)==
 |         |             |- [QREncoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/2DCodeEncoder/QREncoder)/
 |         |                         |- qrcode
 |         |                         |- Pillow
 |         |                         |- wxPython ==(only for GUI version)==
 |         |                         |- numpy ==(only for GUI version)==
 |         |                         |- re ==(only for GUI version)==
 |         |                         |- opencv-python ==(only for GUI version)==
 |         |- [GS1Encoder](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Encoder/GS1Encoder)/
 |                       |- python-barcode
 |                       |- qrcode
 |                       |- Pillow
 |                       |- wxPython ==(only for GUI version)==
 |                       |- re ==(only for GUI version)==
 |                       |- io ==(only for GUI version)==
 |- [Scanner](https://github.com/SomeB1oody/BarcodeMaster/tree/main/src/Scanner)/
      |- opencv-python
      |- wxPython
      |- numpy
      |- pyzbar
      |- re

Python version should be at least 3.10

You can also directly execute the following installation command, which includes all the required libraries:
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
## 5. Contribution

Contributions are welcome! Follow these steps:
 - 1. Fork project.
 - 2. Create branch:
 ```bash
 git checkout -b feature-name
```
- 3. Submit changes:
```bash
git commit -m "Explain changes"
```
- 4. Push branch:
```bash
git push orgin feature-name
```
- 5. Submit Pull Request.
---
## 6. License

This project uses [MIT LICENSE](LICENSE).

---
## 7. Contact information

- Author: Stan Yin
- Email: stanyin64@gmail.com
- GitHub: [@SomeB1ooody](https://github.com/SomeB1oody)