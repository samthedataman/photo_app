### IMPORTS ###
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os
from PIL import ImageEnhance
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from os import listdir
import datetime
from random import choice

from datetime import datetime
from gspread_pandas import Spread,Client

### GLOBALS ###
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets', 
    "https://www.googleapis.com/auth/drive.file", 
    "https://www.googleapis.com/auth/drive"
]

PICTURE_FOLDER_PATH = "/Users/samsavage/Pictures/RIOCHE/RIOCHE_Best/Best_Summer_Photos"

PATH = os.listdir(PICTURE_FOLDER_PATH)

SLIDER_DEFAULT = 1.0
PROPERTY_VALUES = {}


### FUNCTIONS ###
def google_sheets(cred_path, sheet_name, scope_list):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f'{cred_path}', scope_list)
    client = Client(scope=scope_list,creds=credentials)
    spreadsheetname = sheet_name
    spread = Spread(spreadsheetname,client = client)
    sh = client.open(spreadsheetname)
    worksheet_list = sh.worksheets()
    return sh, worksheet_list, spread

def update_the_spreadsheet(spread, spreadsheetname, dataframe):
    col = ['UserName', 'Comment', 'TimeCommented']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname, index = False)
    st.sidebar.info('Updated to GoogleSheet')

def load_the_spreadsheet(sh, spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

@st.cache(
    show_spinner=True, 
    persist=True, 
    suppress_st_warning=True
)
def image_meta(path, property_values):
    image_obj = Image.open(path)
    info_dict = {
        "Filename": image_obj.filename,
        "Image Size": image_obj.size,
        "Image Height": image_obj.height,
        "Image Width": image_obj.width,
        "Image Format": image_obj.format,
        "Image Mode": image_obj.mode,
        "Image is Animated": getattr(image_obj, "is_animated", False),
        "Frames in Image": getattr(image_obj, "n_frames", 1)
    }
    df = pd.DataFrame.from_dict(info_dict)
    im_output = image_obj
    for itm in property_values.values():
        enh = itm["image_enhance_func"](image_obj)
        im_output = enh.enhance(itm["slider"])

    return im_output

def display_image(image_data):
    return st.image(image_data)



def write_intro_to_page():
    st.title('~~~~~~~~~Sam\'s Photos~~~~~~~~~')
    st.write(
        f"""This is an image blog for anyone interested in gritty new york city street photography.
        A little about me: My name is Sam, and I have a passion for data analysis and phototgraphy.
        This blog is manifestation and synergy of those two things! If you would like to leave me a commment feel free.
            
        [P.S]:        
        The photos / side filter edits can take a while to load so be patient 
        """
    )

def write_comment_selection(df):
    random_user = []
    n = 10
    n_2 = 15

    for i in df['Comment']:
        random_user.append(i)

    random_comment_choice = [choice(random_user) for i in range(n)]
    random_comment_choice_2 = [choice(random_user) for i in range(n_2)]

    st.write(
        f"""Here is what others are saying:

        \" {random_comment_choice[0]} \"

        \" {random_comment_choice_2[0]} \" 
        """
    )

def main():

    sh, worksheet_list, spread = google_sheets(
        '/Users/samsavage/Documents/PancakeSwap-Data-Pipeline-/poocoin-331423-6227f4a5365e.json',
        "Photo_App", 
        SCOPES
    )

    print("data loaded to sheet")

    df = load_the_spreadsheet(sh, 'Comment_Data')


    write_intro_to_page()
    write_comment_selection(df)

    st.markdown(
        'Follow me on IG @  [link](https://www.instagram.com/samthematzahman/?hl=en/)', 
        unsafe_allow_html=True
    )
    #opening the image
    

    with st.sidebar:

        PROPERTY_VALUES["brightness"] = {
            "image_enhance_func": ImageEnhance.Brightness,
            "slider": st.slider('Toggle Image Brightness', 0.0, 10.0,(SLIDER_DEFAULT)),
        }
        PROPERTY_VALUES["contrast"] = {
            "image_enhance_func": ImageEnhance.Contrast,
            "slider": st.slider('Toggle Image Contrast', -1.0, 5.0,(SLIDER_DEFAULT))
        }
        PROPERTY_VALUES["sharpness"] = {
            "image_enhance_func": ImageEnhance.Sharpness,
            "slider": st.slider('Toggle Image Sharpness', -1.0, 5.0,(SLIDER_DEFAULT))
        }
        PROPERTY_VALUES["color"] = {
            "image_enhance_func": ImageEnhance.Color,
            "slider": st.slider('Toggle Image Color', -1.0, 5.0,(SLIDER_DEFAULT)),
        }
        st.write("**Add your own comment:**")
        form = st.form("comment")
        name = form.text_input("Name", "Name")
        comment = form.text_area("Comment","Write how you feel here!")
        submit = form.form_submit_button("Add comment")

        if submit:
            now = datetime.now()
            opt = {
                'UserName':      [name],
                'Comment':       [comment],
                'TimeCommented': [now]
            }
            opt_df = pd.DataFrame(opt)
            df = load_the_spreadsheet(sh, 'Comment_Data')
            new_df = df.append(opt_df, ignore_index=True)
            update_the_spreadsheet(spread, 'Comment_Data', new_df)

    cols = st.columns(3)
    path_array_splits = np.array_split(PATH, 3)
    arr = []
    for idx in range(3):
        item = {"list": path_array_splits[idx], "col": cols[idx]}
        arr.append(item)

    for item in arr:  
        for count,i in enumerate(item["list"]):
            try:
                with item["col"]:
                    image_data = image_meta(f'{PICTURE_FOLDER_PATH}/{i}', PROPERTY_VALUES)
                    display_image(image_data)
            except:
                print("shit")
            continue

if __name__ == "__main__":
    main()