import cv2
import numpy as np
from pyzbar.pyzbar import decode

def scan_code():
    cap = cv2.VideoCapture(0)
    on = True
    while on:
        success, img = cap.read()
        if not success:
            break
        for code in decode(img):
            isbn_13 = code.data.decode("utf-8")
            print(code.data.decode("utf-8"))
            on = False
        
        cv2.imshow("barcode", img)
        cv2.waitKey(1)
    cap.release()
    return isbn_13

#9780552150736