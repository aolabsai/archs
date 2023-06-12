# -*- coding: utf-8 -*-
"""
Following this guide for easy digestion of MNIST into my algorithm: https://stackoverflow.com/questions/40427435/extract-images-from-idx3-ubyte-file-or-gzip-via-python/40430149#40430149


"""
#%% Importing Core Modules

# Standard Python modules
import numpy as np
import pandas as pd

from keras.datasets import mnist        
from pathlib import Path


#%% Importing From Keras MNIST
        
(MN_TRAIN, MN_TRAIN_labels), (MN_TEST, MN_TEST_labels) = mnist.load_data()



#%% instead of a dictonary, this object will store the MNIST to binary conversions

label_to_binary = np.zeros([10, 4], dtype="int8")
for i in np.arange(10):
    label_to_binary[i]= np.array(list(np.binary_repr(i, 4)), dtype=int)



#%% Standard Fonts - Importing them from Excel

font_name_list = [
"Times New Roman",
"Calibri",
"Arial",
"Helvetica",
"Cambria",
"Garamond Bold",
"Edwardian Script",
"Bradley Hand",
"Viner Hand",
"Freestyle Script",
"Comic Sans",
"Interstellar"]

nF = len(font_name_list) # number of training fonts

ST_TRAIN = np.copy(MN_TRAIN[0:nF*10])  # times 10 since each nF has 10 characters (0-9)
ST_TRAIN_labels = np.zeros(nF*10)

data_folder = Path(r'./Demos/MNIST_files/Original/Standard Training')


nf = 0
for font in font_name_list:

    file_name = font + str(".xlsx")
    file_to_open = data_folder / file_name
    
    excel_import = pd.read_excel(file_to_open, sheet_name="export")

    cs = 28+1                
    ST_TRAIN[nf + 0] = np.asarray(excel_import.iloc[0:28, 0:28])
    ST_TRAIN[nf + 1] = np.asarray(excel_import.iloc[0:28, 28+1:28+28+1])
    ST_TRAIN[nf + 2] = np.asarray(excel_import.iloc[0:28, 28+1+cs :28+28+1+cs])
    ST_TRAIN[nf + 3] = np.asarray(excel_import.iloc[0:28, 28+1+cs+cs :28+28+1+cs+cs])
    ST_TRAIN[nf + 4] = np.asarray(excel_import.iloc[0:28, 28+1+cs+cs+cs :28+28+1+cs+cs+cs])
    ST_TRAIN[nf + 5] = np.asarray(excel_import.iloc[28+2:28+28+2, 0:28])
    ST_TRAIN[nf + 6] = np.asarray(excel_import.iloc[28+2:28+28+2, 28+1:28+28+1])
    ST_TRAIN[nf + 7] = np.asarray(excel_import.iloc[28+2:28+28+2, 28+1+cs :28+28+1+cs])
    ST_TRAIN[nf + 8] = np.asarray(excel_import.iloc[28+2:28+28+2, 28+1+cs+cs :28+28+1+cs+cs])
    ST_TRAIN[nf + 9] = np.asarray(excel_import.iloc[28+2:28+28+2, 28+1+cs+cs+cs :28+28+1+cs+cs+cs])

    ST_TRAIN_labels[nf : nf+10] = np.arange(10)
        
    nf += 10