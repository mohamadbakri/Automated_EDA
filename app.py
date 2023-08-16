import streamlit as st
import pandas as pd
import plotly.express as px

import functions

st.set_page_config(layout="wide", page_icon='./logo.png', page_title='EDA')

# st.header("🎨Exploratory Data Analysis Tool for Data Science Projects")
st.header("🎨Electro Pi Capstone: Automated EDA .")
st.write('<p style="font-size:100%">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 👤 Reverse Engineered By Mohammad Bakri</p>',unsafe_allow_html=True)

st.write('<p style="font-size:160%">You will be able to✅:</p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 1. See the whole dataset</p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 2. Get column names, data types info</p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 3. Get the count and percentage of NA values</p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 4. Get descriptive analysis </p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 5. Check inbalance or distribution of target variable:</p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 6. See distribution of numerical columns</p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 7. See count plot of categorical columns</p>',
         unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 8. Get outlier analysis with box plots</p>',
         unsafe_allow_html=True)

# st.image('header2.png', use_column_width = True)

functions.space(2)
st.write('<p style="font-size:130%">Import Dataset</p>', unsafe_allow_html=True)

file_format=st.radio('Select file format:',
                       ('csv', 'excel'), key='file_format')
dataset=st.file_uploader(label='')

use_defo=st.checkbox('Use example Dataset')
if use_defo:
    dataset='CarPrice_Assignment.csv'

st.sidebar.header('Import Dataset to Use Available Features: 👉')

if dataset:
    if file_format == 'csv' or use_defo:
        df=pd.read_csv(dataset)
    else:
        df=pd.read_excel(dataset)

    st.subheader('Dataframe:')
    # Get dataframe number of rows and columns
    n, m=df.shape
    st.write(
        f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)
    # plot dataframe
    st.dataframe(df)

    all_vizuals=['Info', 'NA Info', 'Descriptive Analysis', 'Target Analysis',
                   'Distribution of Numerical Columns', 'Count Plots of Categorical Columns', 'Box Plots', 'Outlier Analysis']

    functions.sidebar_space(3)
    # Plot Sidebar
    vizuals=st.sidebar.multiselect(
        "Choose which visualizations you want to see 👇", all_vizuals)

    if 'Info' in vizuals:
        st.subheader('Info:')
        c1, c2, c3=st.columns([1, 2, 1])
        c2.dataframe(functions.df_info(df))

    if 'NA Info' in vizuals:
        st.subheader('NA Value Information:')
        if df.isnull().sum().sum() == 0:
            st.write('There is not any NA value in your dataset.')
        else:
            c1, c2, c3=st.columns([0.5, 2, 0.5])
            c2.dataframe(functions.df_isnull(df), width=1500)
            functions.space(2)

    if 'Descriptive Analysis' in vizuals:
        st.subheader('Descriptive Analysis:')
        st.dataframe(df.describe())

    if 'Target Analysis' in vizuals:
        st.subheader("Select target column:")
        target_column=st.selectbox("", df.columns, index=len(df.columns) - 1)

        st.subheader("Histogram of target column")
        fig=px.histogram(df, x=target_column)
        c1, c2, c3=st.columns([0.5, 2, 0.5])
        """
        fi=px.bar(df, x=target_column)
        c1.plotly_chart(fi)
        """
        c2.plotly_chart(fig)

    num_columns=df.select_dtypes(exclude='object').columns
    cat_columns=df.select_dtypes(include='object').columns

    if 'Distribution of Numerical Columns' in vizuals:

        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols=functions.sidebar_multiselect_container(
                'Choose columns for Distribution plots:', num_columns, 'Distribution')
            st.subheader('Distribution of numerical columns')
            i=0
            while (i < len(selected_num_cols)):
                c1, c2=st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_num_cols)):
                        break

                    fig=px.histogram(df, x=selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width=True)
                    i += 1

    if 'Count Plots of Categorical Columns' in vizuals:

        if len(cat_columns) == 0:
            st.write('There is no categorical columns in the data.')
        else:
            selected_cat_cols=functions.sidebar_multiselect_container(
                'Choose columns for Count plots:', cat_columns, 'Count')
            st.subheader('Count plots of categorical columns')
            i=0
            while (i < len(selected_cat_cols)):
                c1, c2=st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_cat_cols)):
                        break

                    fig=px.histogram(
                        df, x=selected_cat_cols[i], color_discrete_sequence=['indianred'])
                    j.plotly_chart(fig)
                    i += 1

    if 'Box Plots' in vizuals:
        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols=functions.sidebar_multiselect_container(
                'Choose columns for Box plots:', num_columns, 'Box')
            st.subheader('Box plots')
            i=0
            while (i < len(selected_num_cols)):
                c1, c2=st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_num_cols)):
                        break

                    fig=px.box(df, y=selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width=True)
                    i += 1

    if 'Outlier Analysis' in vizuals:
        st.subheader('Outlier Analysis')
        c1, c2, c3=st.columns([1, 2, 1])
        c2.dataframe(functions.number_of_outliers(df))

