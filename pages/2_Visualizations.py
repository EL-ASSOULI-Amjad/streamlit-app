import streamlit as st
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
    st.sidebar.header("⚙️ Filter Options")
    
    # Category filter
    all_categories = sorted(set([category for sublist in df['categories'].dropna().str.split(', ') for category in sublist]))
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=all_categories
    )

    # Genre filter
    all_genres = sorted(set([genre for sublist in df['genre'].dropna().str.split(', ') for genre in sublist]))
    selected_genres = st.sidebar.multiselect(
        "Select genres",
        options=all_genres
    )

     # app filter
    all_apps = sorted(set([app for sublist in df['title'].dropna().str.split(', ') for app in sublist]))
    selected_apps = st.sidebar.multiselect(
        "Select apps",
        options=all_apps
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
    st.title("📊 App Market Visualizations")
    
    # Tab layout for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📰 Market Overview", "📈 Trends", "📝 Descriptions", "🔎 Specific app info"])

    with tab1:
        # Market Overview Tab
        st.subheader("📰 Market Overview")
        st.subheader("⚖️ Reviews Comparison")

        st.markdown(f"**Displaying {len(filtered_df)} apps**")

        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Rating", f"{round(filtered_df['overall rating'].mean(), 2)} ⭐")
        with col2:
            st.metric("Average downloads", f"{filtered_df['downloads'].mean():,.0f} 📥")
        with col3:
            st.metric("Free Apps", f"{len(filtered_df[filtered_df['price'] == 0])} ({len(filtered_df[filtered_df['price'] == 0])/len(filtered_df)*100:.0f}%) 💰")


        fig = px.bar(
            filtered_df,
            x='title',
            y='overall rating',
            title="Ratings by App",
            color='overall rating',
            color_continuous_scale='Blues',
            labels={'title': 'App Title', 'overall rating': 'Rating'}
        )

        # Update layout to improve readability
        fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            title_font=dict(size=20),
            xaxis_title='App Title',
            yaxis_title='Overall Rating',
            margin=dict(t=60, b=120)
        )

        st.plotly_chart(fig, use_container_width=True)





    with tab2:
        # Trends Tab
        st.subheader("📈 Market Trends")

        if not filtered_df['title'].isnull().all():  # Ensure that titles are available
            # Plot Apps released with their titles on X-axis
            st.subheader("Apps Released")
            fig = px.scatter(
            filtered_df,
            x="title",
            y="year_released",
            title="App Release Years",
            labels={"title": "App Title", "year_released": "Year Released"},
            color="genre"  # Optional: color by genre
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

           # Genre trends over time
            st.subheader("Genre Trends Over Time")

            # Ensure 'year_released' and 'genre' columns exist
            if 'year_released' in df.columns and 'genre' in df.columns:
                # Explode multiple genres per app
                genre_time_df = df.dropna(subset=['genre', 'year_released']).copy()
                genre_time_df['genre'] = genre_time_df['genre'].str.split(', ')
                genre_time_df = genre_time_df.explode('genre')

                # Group by year and genre
                genre_trend = genre_time_df.groupby(['year_released', 'genre']).size().reset_index(name='App Count')

                # Plot with Plotly
                fig_genre_trend = px.area(
                    genre_trend,
                    x="year_released",
                    y="App Count",
                    color="genre",
                    title="Number of Apps per Genre Over Time",
                    markers=True
                )
                fig_genre_trend.update_layout(xaxis_title="Year Released", yaxis_title="Number of Apps")
                st.plotly_chart(fig_genre_trend, use_container_width=True)
            else:
                st.info("Genre or year information is missing.")

        else:
            st.warning("No title information available for selected apps")


    with tab3:
        st.subheader("☁️ Description Word Cloud")
        all_text = ' '.join(filtered_df['summary'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
        st.image(wordcloud.to_array(), use_container_width=True)

    with tab4:
        st.subheader("ℹ️ Show info about a specific app")
        all_apps = sorted(set([app for sublist in df['title'].dropna().str.split(', ') for app in sublist]))
        selected_app = st.selectbox(
                "⚙️ Select one app to analyze",
                options=all_apps,
                index=0 if all_apps else None
            )
        select_app = df.copy()
        select_app = df[df['title'].str.contains(selected_app, case=False)]

        release_date = select_app['released'].iloc[0]
        formatted_date = release_date.strftime('%B %d, %Y') if not pd.isnull(release_date) else "Unknown"
        downloads = select_app['downloads'].iloc[0]
        formatted_downloads = f"{downloads:,}"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall rating", f"{select_app['overall rating'].iloc[0]:.2f} ⭐")
        with col2:
            st.metric("Total downloads", f"{formatted_downloads} 📥")
        with col3:
            st.metric("Release date", f"{formatted_date} 📅")

        st.subheader("🗂️ Categories")
        st.write(select_app['categories'].iloc[0])
        st.subheader("🏷️ Genres")
        st.write(select_app['genre'].iloc[0])
              
    # Raw data expander
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df.sort_values('downloads', ascending=False))

except Exception as e:
    st.error(f"An error occurred while processing the data: {str(e)}")
    st.markdown("[Go back to Results Table ➡️](/Retrieving)")