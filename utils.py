# importing the required modules
import json
from transformers import pipeline
from google_play_scraper import search, app, Sort  
from google_play_scraper import reviews as gp_reviews, Sort
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np

# initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def retrieve_data(item):
    try:
        apps = search(item, n_hits=20)
        if not apps:
            st.warning(f"No apps found for search term: {item}")
            return None

        data = []
        reviews_table = []

        for app_info in apps:
            app_id = app_info['appId']
            app_details = app(app_id)
            app_reviews_data, _ = gp_reviews(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=20
            )
            review_texts = [review['content'] for review in app_reviews_data]
            title = app_details.get('title')
            released = app_details.get('released')
            summary = app_details.get('summary')
            overall_rating = app_details.get("score")
            ratings_number = app_details.get('ratings')
            app_reviews = app_details.get('reviews')
            price = app_details.get('price')
            developer = app_details.get('developer')
            categories = [category['name'] for category in app_details.get('categories', [])]
            genre = app_details.get('genre')
            installs = ''.join(filter(str.isdigit, app_details.get('installs', '')))
            installs_number = int(installs) if installs else 0
        
            try:
                sentiments = sentiment_pipeline(review_texts)
                confidences = []
                sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0}


                for review_text, sentiment in zip(review_texts, sentiments):
                    sentiment_label = sentiment['label']
                    reviews_table.append({
                        "title": title,
                        "comment": review_text,
                        "sentiment": sentiment_label,
                        "genre": genre,
                        "overall rating": overall_rating,
                        "ratings": ratings_number,
                        "categories": ", ".join(categories),
                        "confidence": round(sentiment['score'], 3)
                    })
                    confidences.append(round(sentiment['score'], 3))
                    if sentiment_label == "POSITIVE":
                        sentiment_counts["POSITIVE"] += 1
                    elif sentiment_label == "NEGATIVE":
                        sentiment_counts["NEGATIVE"] += 1
            except Exception as e:
                st.error(f"Error retrieving comment: {str(e)}")
                return None
            
            total_reviews = len(review_texts)
            positive_percentage = (sentiment_counts["POSITIVE"] / total_reviews) * 100 if total_reviews > 0 else 0
            negative_percentage = (sentiment_counts["NEGATIVE"] / total_reviews) * 100 if total_reviews > 0 else 0

            data.append({
                "title": title,
                "downloads": installs_number,
                "overall rating": overall_rating,
                "released": released,
                "summary": summary,
                "reviews": app_reviews,
                "ratings": ratings_number,
                "price": price,
                "developer": developer,
                "genre": genre,
                "categories": ", ".join(categories),
                "average score": round(np.mean(confidences), 2) if confidences else 0,
                "positive_percentage": round(positive_percentage, 2),
                "negative_percentage": round(negative_percentage, 2)
            })
            
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {obj.__class__.__name__} not serializable")

        with open(f"{item}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=custom_serializer)
        with open(f"{item}_comments.json", "w", encoding="utf-8") as fl:
            json.dump(reviews_table, fl, indent=4, ensure_ascii=False, default=custom_serializer)

        df = pd.read_json(f"{item}.json")
        df2 = pd.read_json(f"{item}_comments.json")
        df.to_csv(f"{item}.csv", index=False)
        df2.to_csv(f"{item}_comments.csv", index=False)

        st.session_state["retrieving_data"] = data
        st.session_state["retrieving_data_comments"] = reviews_table
        return data, reviews_table

    except Exception as e:
        st.error(f"Error retrieving data: {str(e)}")
        return None

def show_data(item):
    df = pd.read_csv(f'{item}.csv')
    st.write(f"Displaying data for: {item}")
    st.dataframe(df)

def show_sentiment_analysis(item):
    try:
        df_comments = pd.read_csv(f"{item}_comments.csv")
        st.subheader("🧠 Sentiment Analysis of Reviews")
        st.dataframe(df_comments)
    except Exception as e:
        st.error(f"Unable to load sentiment data: {str(e)}")
