import math

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

df = pd.read_csv("MARKET_Car_Prices_clean.csv")
st.set_page_config(layout="wide")


# Histograms
st.header("Histogram of:")
cols = st.multiselect("Select columns:", df.columns, ['price', 'make'])

if len(cols) > 0:
    fig = make_subplots(rows=math.ceil(len(cols) / 2), cols=2)
    row = 1
    col = 1
    for c in cols:
        data = go.Histogram(x=df[c], name=c)
        fig.add_trace(data, row=row, col=col)
        col += 1
        if col == 3:
            row += 1
            col = 1

    st.plotly_chart(fig, use_container_width=True)

# Scatter plot
st.header("Select columns for scatter plot:")
col1, col2 = st.columns(2)
with col1:
    x, y, hover_name, size, color = (st.selectbox("X axis: ",
                                                  df.select_dtypes(include=['number']).columns, 15),
                                     st.selectbox("Y axis:",
                                                  df.select_dtypes(include=['number']).columns, 13),
                                     st.selectbox("Hover name:",
                                                  df.columns, 0),
                                     st.selectbox("Size:",
                                                  df.select_dtypes(include=['number']).columns, 7),
                                     st.selectbox("Color:",
                                                  df.columns, 0))
with col2:
    fig = px.scatter(
        df,
        x=x,
        y=y,
        hover_name=hover_name,
        size=size,
        color=color
    )
    st.plotly_chart(fig)

# Scatter plot with marginals
with col1:
    st.header("Select columns for scatter plot with marginals:")

    x, y, marginal_x, marginal_y, color = (st.selectbox("X:",
                                                        df.select_dtypes(include=['number']).columns, 7),
                                           st.selectbox("Y:",
                                                        df.select_dtypes(include=['number']).columns, 11),
                                           st.selectbox("Marginal for X:",
                                                        ['histogram', 'box', 'violin'], 1),
                                           st.selectbox("Marginal for Y:",
                                                        ['histogram', 'box', 'violin'], 2),
                                           st.selectbox("Marginal Color:",
                                                        df.columns, 1))
with col2:
    fig = px.scatter(df, x=x, y=y, color=color, marginal_y=marginal_y,
                     marginal_x=marginal_x, trendline="ols", template="simple_white")
    st.plotly_chart(fig)

# Pie chart
labels = df['make'].unique()
values = [df["make"].value_counts()[x] for x in labels]
with col1:
    st.header('Percentage of car makes:')
    fig2 = go.Figure(go.Bar(y=values, x=labels, ))
    st.plotly_chart(fig2)

with col2:
    st.header('Percentage of car makes with Pie chart:')
    data = go.Pie(labels=labels, values=values, hole=0.6)
    fig = go.Figure(data=data)
    st.plotly_chart(fig)

st.columns(1)
st.header('Mean values for city and highway over makes')
mean_city_mpg = [df.loc[df['make'] == x, 'city_mpg'].mean() for x in labels]
mean_highway_mpg = [df.loc[df['make'] == x, 'highway_mpg'].mean() for x in labels]
trace_1 = go.Bar(x=labels, y=mean_city_mpg, name="Mean city mpg")
trace_2 = go.Bar(x=labels, y=mean_highway_mpg, name="Mean highway mpg")

data = [trace_1, trace_2]

fig = go.Figure(data)
st.plotly_chart(fig, use_container_width=True)

