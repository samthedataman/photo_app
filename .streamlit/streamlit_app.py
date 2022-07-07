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

scopes = ['https://www.googleapis.com/auth/spreadsheets', 
          "https://www.googleapis.com/auth/drive.file", 
          "https://www.googleapis.com/auth/drive"]

def google_sheets(CRED_PATH,SHEET_NAME,SCOPE_LIST):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(F'{CRED_PATH}', SCOPE_LIST)
    client = Client(scope=SCOPE_LIST,creds=credentials)
    spreadsheetname = SHEET_NAME
    spread = Spread(spreadsheetname,client = client)
    sh = client.open(spreadsheetname)
    worksheet_list = sh.worksheets()
    return sh,worksheet_list,spread

def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['UserName','Comment','TimeCommented']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

@st.cache(show_spinner=True, persist=True, suppress_st_warning=True)
def image_meta(path):
        image_OBJ = Image.open(path)
        info_dict = {
            "Filename": image_OBJ.filename,
            "Image Size": image_OBJ.size,
            "Image Height": image_OBJ.height,
            "Image Width": image_OBJ.width,
            "Image Format": image_OBJ.format,
            "Image Mode": image_OBJ.mode,
            "Image is Animated": getattr(image_OBJ, "is_animated", False),
            "Frames in Image": getattr(image_OBJ, "n_frames", 1)
        }
        df = pd.DataFrame.from_dict(info_dict)
        enh = ImageEnhance.Contrast(image_OBJ)
        im_output = enh.enhance(Contrast_values)
        enh = ImageEnhance.Brightness(im_output)
        im_output = enh.enhance(Brightness_values)
        enh = ImageEnhance.Sharpness(im_output)
        im_output = enh.enhance(Sharpness_values)
        enh = ImageEnhance.Color(im_output)
        im_output = enh.enhance(Color_values)
        return st.image(im_output)



sh,worksheet_list,spread = google_sheets('poocoin-331423-6227f4a5365e.json',"Photo_App",scopes)

df = load_the_spreadsheet('Comment_Data')

random_user = []
n=10
n_2 =15

for i in df['Comment']:
    random_user.append(i)

random_comment_choice = [choice(random_user) for i in range(n)]

random_comment_choice_2 = [choice(random_user) for i in range(n_2)]



st.title('~~~~~~~~~Sam\'s Photos~~~~~~~~~')
st.write(
        f"""This is an image blog for anyone interested in gritty new york city street photography.
        A little about me: My name is Sam, and I have a passion for data analysis and phototgraphy.
        This blog is manifestation and synergy of those two things! If you would like to leave me a commment feel free.
        
        [P.S]:        
        The photos / side filter edits can take a while to load so be patient 
        """
    )
user_comments = st.write(f"""Here is what others are saying:

\" {random_comment_choice[0]} \"

\" {random_comment_choice_2[0]} \" """)

link='Follow me on IG @  [link](https://www.instagram.com/samthematzahman/?hl=en/)'
st.markdown(link,unsafe_allow_html=True)
#opening the image
PATH = os.listdir('/Users/samsavage/Desktop/Streamlit App/.streamlit/Best_Summer_Photos/')

bightness_slider_default = 1.0
contrast_slider_default = 1.0
sharpness_slider_default = 1.0
color_slider_default = 1.0


comments = []
user_names = []
with st.sidebar:
    Brightness_values = st.slider('Toggle Image Brightness', 0.0, 10.0,(bightness_slider_default))
    Contrast_values = st.slider('Toggle Image Contrast', -1.0, 5.0,(contrast_slider_default))
    Sharpness_values = st.slider('Toggle Image Sharpness', -1.0,5.0,(sharpness_slider_default))
    Color_values = st.slider('Toggle Image Color', -1.0,5.0,(color_slider_default))
    st.write("**Add your own comment:**")
    form = st.form("comment")
    name = form.text_input("Name","")
    comment = form.text_area("Comment","")
    submit = form.form_submit_button("Add comment")



    if submit:
        now = datetime.now()
        opt = {
            'UserName':[name],
            'Comment':[comment],
            'TimeCommented':[now]
        }
        opt_df = pd.DataFrame(opt)
        df = load_the_spreadsheet('Comment_Data')
        new_df = df.append(opt_df, ignore_index=True)
        update_the_spreadsheet('Comment_Data', new_df)
  



index = 0
col1, col2, col3 = st.columns(3)
list1,list2,list3 = np.array_split(PATH, 3)


user_feedback = []

for count,i in enumerate(list1):
    try:
        with col1:
            image_meta(f'/Users/samsavage/Desktop/Streamlit App/.streamlit/Best_Summer_Photos/{i}')
    except:
        print("image not available")
    continue
for count,i in enumerate(list2):
    try:
        with col2:
            image_meta(f'/Users/samsavage/Desktop/Streamlit App/.streamlit/Best_Summer_Photos/{i}')
    except:
        print("image not available")
    continue
for count,i in enumerate(list3):
    try:
        with col3:
            image_meta(f'/Users/samsavage/Desktop/Streamlit App/.streamlit/Best_Summer_Photos/{i}')
    except:
        print("image not available")
    continue