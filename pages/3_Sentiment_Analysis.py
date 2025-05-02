#importing manually the modules in case 'utils.py' fails
import streamlit as st
from transformers import pipeline
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from utils import *

# Page configuration
st.set_page_config(page_title="App Visualizations", layout="wide")

# Check if data exists
if "retrieving_data" not in st.session_state:
    st.warning("No data available. Please retrieve data first from the 'Results Table' page.")
    st.markdown("[Go to Results Table ➡️](/Retrieving)")
    st.stop()

try:
    # Convert data to DataFrame
    df = pd.DataFrame(st.session_state["retrieving_data"])
    comments = pd.DataFrame(st.session_state["retrieving_data_comments"])
    
    # Data preprocessing
    df['released'] = pd.to_datetime(df['released'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['year_released'] = df['released'].dt.year
    

    # Sidebar filters
    st.sidebar.header("Filter Options")
    
    # Category filter
    all_categories = sorted(set([category for sublist in df['categories'].dropna().str.split(', ') for category in sublist]))
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=all_categories
    )

    # app filter
    all_apps = sorted(set([app for sublist in df['title'].dropna().str.split(', ') for app in sublist]))
    selected_apps = st.sidebar.multiselect(
        "Select apps",
        options=all_apps
    )

    # Genre filter
    all_genres = sorted(set([genre for sublist in df['genre'].dropna().str.split(', ') for genre in sublist]))
    selected_genres = st.sidebar.multiselect(
        "Select genres",
        options=all_genres
    )


    
    # Apply filters
    filtered_df = df.copy()
    filtered_comments = comments.copy()
    min_rating = st.sidebar.slider("Minimum rating",1.0, 5.0, 3.0)
    filtered_df = filtered_df[filtered_df['overall rating'] >= min_rating]
    filtered_comments = filtered_comments[filtered_comments['overall rating'] >= min_rating]
    if selected_categories:
        filtered_df = filtered_df[filtered_df['categories'].str.contains('|'.join(selected_categories), case=False)]
        filtered_comments = filtered_comments[filtered_comments['categories'].str.contains('|'.join(selected_categories), case=False)]
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genre'].str.contains('|'.join(selected_genres), case=False)]
        filtered_comments = filtered_comments[filtered_comments['genre'].str.contains('|'.join(selected_genres), case=False)]
    if selected_apps:
        filtered_df = filtered_df[filtered_df['title'].str.contains('|'.join(selected_apps), case=False)]
        filtered_comments = filtered_comments[filtered_comments['title'].str.contains('|'.join(selected_apps), case=False)]

    # Main content


    st.subheader("🧠 Sentiment Analysis")

    if comments.empty:
        st.info("No sentiment data available.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            # Calculate sentiment distribution
            sentiment_counts = filtered_comments['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']
            
            # Calculate the percentage for each sentiment type
            sentiment_counts['Percentage'] = (sentiment_counts['Count'] / sentiment_counts['Count'].sum()) * 100
            
            # Create the pie chart with sentiment and percentage labels
            fig_sentiment_pie = px.pie(sentiment_counts, 
                                        names='Sentiment', 
                                        values='Count', 
                                        title="Sentiment Distribution of reviews across apps",
                                        color_discrete_sequence=px.colors.qualitative.Set2,
                                        labels={'Sentiment': 'Sentiment Type', 'Count': 'Number of Reviews'},
                                        hole=0.3)

            # Show percentage on the chart
            fig_sentiment_pie.update_traces(textinfo='percent+label', textfont_size=14)

            st.plotly_chart(fig_sentiment_pie, use_container_width=True)

        with col2:
            # Bar chart: Average confidence per app 
            # Calculating mean confidence per app
            confidence_by_app = (
                filtered_comments
                .groupby("title")["confidence"]
                .mean()
                .reset_index()
            )

            
            fig_sentiment_bar = px.bar(
                confidence_by_app,
                x='title',
                y='confidence',
                title="Sentiment precision per App",
                color='confidence',
                text_auto='.2f',
                color_continuous_scale='Viridis'
            )

            fig_sentiment_bar.update_layout(xaxis_tickangle=-45)

            # Display the chart
            st.plotly_chart(fig_sentiment_bar, use_container_width=True)

    # Raw data expander
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df.sort_values('downloads', ascending=False))

except Exception as e:
    st.error(f"An error occurred while processing the data: {str(e)}")
    st.markdown("[Go back to Results Table ➡️](/Retrieving)")