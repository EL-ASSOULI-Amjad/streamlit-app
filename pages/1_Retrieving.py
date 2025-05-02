from utils import *

st.title("Retrieving data")
st.markdown("""
    ### Example search terms:
    - note taking ai
    - productivity
    - language learning
    - meditation
    - fitness tracker
    """)

# Initialize the history list only once
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []

# Input box for user search
user_input = st.text_input("Enter a search term: ")

# Add search term when user hits Enter
if user_input:
    if user_input not in st.session_state["search_history"]:
        st.session_state["search_history"].append(user_input)

    st.write("🔍 Previous Searches:")
    for i, item in enumerate(st.session_state["search_history"], 1):
        st.write(f"{i}. {item}")

    with st.spinner("Retrieving data..."):
        data = retrieve_data(user_input)
        if data:
            show_data(user_input)
            show_sentiment_analysis(user_input)
            st.success("Data retrieved successfully!")
            st.markdown("[Go to Visualizations ➡️](/Visualizations)")