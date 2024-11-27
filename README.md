
# Barcode Master
*Fully functional barcode (1D/2D) processor*

---
## 0. Table of Content
- 1.Intro
- 2.Functions
- 3.Examples
- 4.Required environment
- 5.Contribution
- 6.License
- 7.Contact information

---
## 1.Intro

**Barcode Master** is a lightweight 1D/2D barcode processor using Python wxWidgets as the frontend. Whether it's encoding, decoding, or recognition (with built-in perspective transformation), you can find corresponding solutions in this project. The currently supported barcode formats include: Code39, Code128, UPC, EAN13, EAN8, ITF, PZN, JAN, DataMatrix, PDF417, QR Code, and GS1.

Each program comes with both a non-GUI and a GUI version. The non-GUI version offers the simplest operations and code, making it easier to understand. The GUI version supports more complex operations, providing a more advanced and user-friendly experience.

Due to my limited capabilities, the code may have some imperfections. I warmly welcome everyone to share their suggestions and contribute to the project. For more details, please see the  Contribution. Thank you for your understanding!

---
### 2. Functions

### 2.1. Structure

This is the sturcture of this project:

![Structure](https://github.com/user-attachments/assets/a4f7dab6-1c17-4f03-aaae-1ec70961064c)

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
## 4. Required environment

Below is a list of libraries used in the project, organized based on the project structure. Libraries marked with (only for GUI version) are only used in the GUI version. If you are not using the GUI version, you do not need to check whether these libraries are installed.

![environment](https://github.com/user-attachments/assets/4b3fd6f9-889b-4928-94df-04a3002a1578)


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

This project uses [MIT LICENSE](https://github.com/SomeB1oody/BarcodeMaster/blob/main/LICENSE.md).

---
## 7. Contact information

- Email: stanyin64@gmail.com
- GitHub: [@SomeB1ooody](https://github.com/SomeB1oody)
