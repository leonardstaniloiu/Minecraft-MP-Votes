import streamlit as st

st.set_page_config(
    page_title="Minecraft-MP Votes",
    page_icon=":material/emoji_events:",
    layout="centered"
)

user_page = st.Page("pages/user_vote.py", title="User Vote Page", icon=":material/emoji_events:")
topvotes_page = st.Page("pages/top_votes.py", title="Top Votes Page", icon=":material/star:")
pg = st.navigation([user_page, topvotes_page])
pg.run()

