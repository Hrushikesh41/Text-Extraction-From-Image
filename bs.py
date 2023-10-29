import cv2;
from pyzbar.pyzbar import decode;
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
from PIL import Image;
from pytesseract import pytesseract;
import enum;

print("Select Operation")
print("1. Upload Image")
print("2. Open Camera")

userInput = input()

used_codes = []

if userInput == "Upload Image" :
    root = tk.Tk()
    root.title('Select Image file to extract text or Scan Barcode')
    root.resizable(False, False)
    root.geometry('550x250')

    text = tk.Text(root, height=12)
    text.grid(column=0, row=0, sticky='nsew')

    def open_image_file():
        class OS(enum.Enum):
            Mac = 0
            Windows = 1

        class Language(enum.Enum):
            English = "eng"

        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
    # show the open file dialog
        f2 = fd.askopenfile(filetypes=filetypes)
        image_path = os.path.abspath(f2.name)

        class ImageReader:
            text.delete("1.0", "end");

            def __init__(self, os: OS): 
                if os == OS.Mac : 
                    print("Running on Mac")

            if os == OS.Windows :
                windows_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                pytesseract.tesseract_cmd = windows_path
                print("Running on Windows")

            def extract_text(self, image_path:str, lang:str)-> str: 
                imgs = Image.open(image_path)
                extracted_text = pytesseract.image_to_string(imgs, lang=lang)
                print(extracted_text)
                return extracted_text

        if __name__ == '__main__': 
            ir = ImageReader(OS.Mac)
            text1 = ir.extract_text(image_path, lang='eng')
            text.insert('1.0', text1)

    open_image_button = ttk.Button(
    root,
    text='Select Image',
    command=open_image_file
    )
    
    open_image_button.grid(column=0, row=1, padx=10, pady=10) 


    def scan_barcode():
        
    # file type
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
    # show the open file dialog
        f2 = fd.askopenfile(filetypes=filetypes)
        image_path = os.path.abspath(f2.name)
        

        img2 = cv2.imread(image_path)
        for code in decode(img2) :
            text.delete("1.0", "end")
            text.insert('1.0', code.data.decode("utf-8"))

    open_button = ttk.Button(
    root,
    text='Scan Barcode',
    command=scan_barcode
    )

    open_button.grid(column=0, row=2, padx=10, pady=10) 

    root.mainloop();

elif userInput == "Open Camera" : 
    # creating a list of used codes
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) # 3 is for width
    cap.set(4, 480) # 4 is for height
    camera = True

    root = tk.Tk()
    root.title('Select Image file to extract text or Scan Barcode')
    root.resizable(False, False)
    root.geometry('550x250')

    text = tk.Text(root, height=12)
    text.grid(column=0, row=0, sticky='nsew')

    while camera == True : 
        sucess, frame = cap.read()
        for code in decode(frame) : 
            if code.data.decode('utf-8') not in used_codes : 
                text.insert("1.0", code.data.decode('utf-8'))
                root.mainloop();
                used_codes.append(code.data.decode('utf-8'))
                time.sleep(5)
            elif code.data.decode('utf-8') in used_codes : 
                print("This Code is Already Used") 
                time.sleep(5)
        else : 
            pass
        cv2.imshow("Testing", frame)
        cv2.waitKey(1)

else : 
    pass