import numpy as np
import cv2
from pyzbar.pyzbar import decode
import pandas as pd

'''
This code scans for bar codes using the function Bar_ID, and outputs the macronutrient information of the product 
in the form of a Data Frame.
The output shows macros (Energy, Fat, Protein, and Carbohydrate content) per 100g and per serving.

Included Function: Bar_ID
Description: Starts a video capture, and decodes visible Bar/QR codes.
Returns: The utf-8 code data. 
'''


# Identify a bar code
def Bar_ID():
    # Video capture and window initialisation
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    codeData = []
    # Reading the video for bar/qr codes
    while not codeData:
        _, img = cap.read()
        # cv2.imshow('Camera', img)
        cv2.waitKey(1)

        # Decoding the barcodes and returning the first one
        for i in decode(img):
            codeData = i.data.decode('utf-8')
            # Return just the digits of the barcode
            return codeData

    # Terminate capture and window
    cap.release()
    cv2.destroyAllWindows()


print(Bar_ID())

# Calling Bar_ID function to obtain a code
bar_code = Bar_ID()
# Scraping Open Food Facts for the producing and storing their tables
link = "https://world.openfoodfacts.org/product/" + str(bar_code)
tables = pd.read_html(link)

# Initialising dictionaries and lists that will later be column and index names
macros = ['Energy', 'Proteins', 'Carbohydrates', 'Fat']
row_names = {'Carbohydrates': 'Carbs', 'Proteins': 'Protein'}
column_names = {'As sold for 100 g / 100 ml': 'Per 100 g/ml', 'Nutrition facts': 'Nutrition'}

# Accessing the first table off the website
df = pd.DataFrame(tables[0])
pd.set_option('expand_frame_repr', False)

# Formating to only keep the necessary information
df = df[['Nutrition facts', 'As sold for 100 g / 100 ml']]
df = df[df['Nutrition facts'].isin(macros)]

# Standardising index order
df = df.set_index('Nutrition facts')
df2 = df.reindex(macros)
df2 = df.reset_index()

# Renaming entrees and columns for clarity
df2 = df2.replace(row_names)
df2 = df2.rename(columns=column_names)
print(df2)
