import cv2
from pyzbar.pyzbar import decode

def scan_code():
    cap = cv2.VideoCapture(0)
    num = ""
    while not num.startswith("978"):
        success, img = cap.read()
        if not success:
            break
        for code in decode(img):
            isbn_13 = code.data.decode("utf-8")
            code = code.data.decode("utf-8")
            print(code)
            num = code
        cv2.imshow("barcode", img)
        cv2.waitKey(1)
    cap.release()
    return isbn_13
