import streamlit as st
import requests
import pandas as pd

def get_top_votes(api_key: str):
    server_url = f"https://minecraft-mp.com/api/?object=servers&element=voters&key={api_key}&month={selected_month}&limit={selected_limit}&format=json"
    response = requests.get(server_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("voters", [])

    else:
        st.error("Failed to fetch top votes. Please check your API key and try again.")
        return []

# If you don't use streamlit secrets, you can directly assign your API key here: api_key = "xxxxxxxxxx"
api_key = st.secrets["minecraft_mp_server_key"]

st.title("Top Votes")
st.divider()
st.subheader("See who has voted the most for our server!")

selected_month = st.radio(
    "📅 Select Month",
    ("current", "previous"),
    horizontal=True
)

selected_limit = st.slider(
    "🔢 Number of Top Voters to Display",
    min_value=10,
    max_value=500,
    value=50,
    step=1
)

if api_key:
    top_voters = get_top_votes(api_key)

    if top_voters:
        st.subheader("🏆 Top Voters This Month")
        df = pd.DataFrame(top_voters)

        df["votes"] = pd.to_numeric(df["votes"])

        df = df.sort_values(by="votes", ascending=False)

        df = df.reset_index(drop=True)

        df.index = df.index + 1
        df.index.name = "Rank"

        def highlight_name(row):
            if row.name == 1:
                return ["color: gold; font-weight: 700;"]
            elif row.name == 2:
                return ["color: silver; font-weight: 700;"]
            elif row.name == 3:
                return ["color: #cd7f32; font-weight: 700;"] 
            return [""]

        styled_df = df.style.apply(
            highlight_name,
            axis=1,
            subset=["nickname"]
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            height=400
        )

    else:
        st.info("No votes found for this month.")
else:
    st.warning("Please enter your API key to view top votes.")