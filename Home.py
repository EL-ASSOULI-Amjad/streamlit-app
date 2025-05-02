import streamlit as st

st.set_page_config(
    page_title="Competition analysis",
    page_icon="📊",
    layout="wide"
)

st.title("Competition analysis 🔎")
st.subheader("A data visualization tool for app market analysis ")

st.info("""
## ℹ️ About This Project

This application helps you analyze mobile applications available on the Google Play Store.
By simply entering a search term, you can retrieve and visualize data about competing apps in that market segment.""")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
> ## ⚙️ Features

- **Data Retrieval**: Search for apps based on any keyword.
- **Results Table**: View detailed information about each app including ratings, reviews, and more.
- **Interactive Visualizations**: Explore various charts and graphs to understand the market landscape.
- **Competitive Analysis**: Compare apps based on different metrics.
- **Word Cloud**: Discover common themes in app descriptions.
    """)

with col2:
    st.markdown("""                
> ## 📋 How to Use
1. Navigate to the **Results Table** page.
2. Enter a search term (e.g., "Gaming", "Productivity", "Language learning").
3. Enter to retrieve the data.
4. Explore the results table.
5. Navigate to the **Visualizations** page to see graphical representations of the data.
6. Use the sidebar filters to customize your view.
7. Navigate to the **Sentiment Analysis** page to see graphical representations of the sentiments.                 
             
    """)


col3, col4 = st.columns(2)

with col3:
    st.markdown("""                
> ## 🖥️ Technical Details

This application uses:
- **google-play-scraper**: For retrieving app data from the Google Play Store.
- **Streamlit**: For the web interface.
- **Pandas**: For data manipulation.
- **Plotly**: For useful and clear visualizations.
- **WordCloud**: For text visualization.     
    """)

with col4:
    st.markdown("""
> ## 🔧 Future Improvements

- Add data from other sources like App Store, ProductHunt, and GitHub...
- Implement sentiment analysis on app reviews.
- Add competitor benchmarking features.
- Create user persona analysis based on reviews.
- Add time-series analysis for app rating changes.
    """)



st.markdown("## Start exploring by selecting a page from the sidebar ◀️")