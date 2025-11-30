import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# import all Plotly libraries needed to make interactive charts
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode


st.set_page_config(page_title="Bitcoin Dashboard", layout="wide")
st.title("Bitcoin Price Data Analysis")




# 1st Plot in web app


# Set dashboard sub-heading
st.subheader("Bitcoin Candlestick chart (First 100 days)")

# read csv file
df = pd.read_csv("bitcoin_price_Training - Training.csv")
df["Date"]=df["Date"].astype("datetime64[ns]")

bitcoin_sample = df[0:100]

# Create a candlestick plot points for each row
trace = go.Candlestick(x=bitcoin_sample["Date"],
               high=bitcoin_sample["High"],
               open= bitcoin_sample["Open"],
               close= bitcoin_sample["Close"],
               low= bitcoin_sample["Low"]
               )
# Chart plots in a list
candle_data = [trace]

# Creating the chart layout
layout = {
    "title":"Bitcoin Candlestick Chart",
    "xaxis": {"title": "Date"}
}

candle_stick_fig = go.Figure(data=candle_data, layout=layout)
# To print the chart to the streamlit web app
st.plotly_chart(candle_stick_fig)


# 2nd Plot in Streamlit web app (Line plot)

# Set subheading value
st.subheader("Daily Percentage Change in Closing Price")

# Step 1: Set the index as the Date
bitcoin_sample.set_index("Date", inplace=True)

# Get the percentage change in closing price and add to data frame
bitcoin_sample["%Change in closing price"]=bitcoin_sample["Close"].pct_change()*100

# create a scatter or line plot to display the chart using plotly
scatter_plot = [go.Scatter(x=bitcoin_sample.index, y = bitcoin_sample["%Change in closing price"], mode= "lines")]

layout = {
    "xaxis": {"title":"Date"},
    "yaxis": {"title":"% Change in closing price"}
}
line_plot = go.Figure(data=scatter_plot, layout=layout)
st.plotly_chart(line_plot, use_container_width=True)



# 3rd Plot: Price trends overtime for different price types

st.subheader("Bitcoin Price Trends over time")
price_type = st.selectbox(label="Select Price Type", options=["Open", "High", "Low", "Close"], index=3)

#  We use plotly graph obj, low level API
price_type_plot=[go.Scatter(x = bitcoin_sample.index, y = bitcoin_sample[price_type], mode="lines")]

layout = {
    "title": f"{price_type} over time",
    "xaxis": {"title":"Date"},
    "yaxis": {"title": f"{price_type} price in USD"}
}
price_type_chart = go.Figure(data=price_type_plot, layout=layout)
st.plotly_chart(price_type_chart, use_container_width=True)


# 4th section or Plot

# Dividing a section into 3 columns using st.columns(3)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Yearly Average close price")
    yearly_average = bitcoin_sample["Close"].resample("YE").mean()

    fig_year = px.bar(
        x=yearly_average.index.year.astype(str),
        y=yearly_average.values,
        labels={"x": "Year", "y": "Average Price"},
        title="Yearly average trend",
    )

    # Make x-axis categorical so no 2016.5 nonsense
    fig_year.update_xaxes(type="category")

    st.plotly_chart(fig_year, use_container_width=True)


with col2:
    st.subheader("Quarterly closing price")
    monthly_close_price=bitcoin_sample["Close"].resample("QE").mean()
    # Plot the chart points, use plotly express
    monthly_plots = px.bar(
        x=monthly_close_price.index,
        y=monthly_close_price,
        labels = {"x":"Month", "y":"Average Price (Quarterly)"},
        title="Quarterly Average Trend"
    )
    st.plotly_chart(monthly_plots, use_container_width=True)

with col3:
    st.subheader("Monthly closing price")
    monthly_close_price=bitcoin_sample["Close"].resample("ME").mean()
    # Plot the chart points
    monthly_plots = px.line(
        x=monthly_close_price.index,
        y=monthly_close_price,
        labels = {"x":"Month", "y":"Average Price (Monthly)"},
        title="Monthly Average Trend"
    )
    st.plotly_chart(monthly_plots, use_container_width=True)



# 5th Plot

col4, col5 = st.columns(2)
with col4:
    st.subheader("Closing Price (Normal Scale)")
    # Chart plots, we use plotly express to build the chart quickly
    fig_normal=px.line(
        data_frame=bitcoin_sample,
        x = bitcoin_sample.index,
        y = bitcoin_sample["Close"],
        labels={"x":"Date", "y":"Closing Price"},
        title="Bitcoin Closing Price (Normal Scale)"
    )
    st.plotly_chart(fig_normal, use_container_width=True)

with col5:
    st.subheader("Closing price (log Scale)")
    # Setup the line plots
    fig_log = px.line(
        data_frame=bitcoin_sample,
        x = bitcoin_sample.index,
        y= np.log1p(bitcoin_sample["Close"]),
        labels = {"x":"Date", "y":"log(closing price +1)"},
        title="Bitcoin Closing Price Trend (log Scale)"
    )
    st.plotly_chart(fig_log, use_container_width=True)
