import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np



df = pd.read_csv("/Users/samsavage/Desktop/Grailed_Scraper/0202_data_grailed_clean.csv")
st.title('Grailed Data Analysis')

condition_types= list(df['condition_flag'].drop_duplicates())
clothing_types = list(df['type_flag'].drop_duplicates())
color_types = list(df['color_flag'].drop_duplicates())

color_choice = st.sidebar.multiselect(
    "Colors:", color_types, default=color_types)

clothing_choice = st.sidebar.multiselect(
    "Clothing:", clothing_types, default=clothing_types)


condition_choice = st.sidebar.multiselect(
    "Condition:", condition_types, default=condition_types)

cols = ["color_flag","type_flag","likes_flag","size_flag"]

st_ms = st.multiselect("Columns",df.columns.to_list(),default=cols)


price_values = st.slider('Price range',float(df['new_price_flag'].min()), 2., (4., 100.))

df = df[df['condition_flag'].isin(condition_choice)]
df = df[df['type_flag'].isin(clothing_choice)]
df = df[df['color_flag'].isin(color_choice)]


st.subheader('Sample Data')


st.dataframe(df.head())

# st.table(df.groupby("color_flag")['new_price_flag'].mean().reset_index())


f = px.histogram(df.query(f'new_price_flag.between{price_values}'), x='new_price_flag', nbins=50, title='Price distribution')
f.update_xaxes(title='new_price_flag')
f.update_yaxes(title='No. of listings')
st.plotly_chart(f)
