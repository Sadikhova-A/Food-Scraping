import numpy as np
import cv2
from pyzbar.pyzbar import decode
import pandas as pd


# Function to identify a bar code
def Bar_ID():
    # Video capture and identification of barcode
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    codeData = []
    # Reading the video for codes
    while not codeData:
        _, img = cap.read()
        # cv2.imshow('Camera', img)
        cv2.waitKey(1)

        # Decoding the barcodes and returning the first one
        for i in decode(img):
            codeData = i.data.decode('utf-8')
            return codeData

    cap.release()
    cv2.destroyAllWindows()

print(Bar_ID())

bar_code = Bar_ID()
link = "https://world.openfoodfacts.org/product/" + str(bar_code)
tables = pd.read_html(link)

df = pd.DataFrame(tables[0])
# df = df.drop(df.columns[-1], axis=1)
# df = df.drop([7, 8])
pd.set_option('expand_frame_repr', False)
df = df.drop(df.columns[-1], axis=1)
macros = ['Nutrition facts', 'Energy', 'Fat', 'Proteins', 'Carbohydrates']
df = df[df['Nutrition facts'].isin(macros)]
print(df)
