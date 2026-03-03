import streamlit as st
import requests
import pandas as pd

def check_vote_status(api_key: str, username: str) -> dict:

    url = f"https://minecraft-mp.com/api/?object=votes&element=claim&key={api_key}&username={username_input}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        result = int(response.text.strip())

        status_map = {
            0: "User has not voted in the last 24 hours.",
            1: "User has voted but has NOT claimed the reward.",
            2: "User has voted and already claimed the reward."
        }

        return {
            "status_code": result,
            "message": status_map.get(result, "Unknown response from API."),
            "success": result in [1, 2]
        }

    except requests.RequestException as e:
        return {
            "status_code": None,
            "message": f"API request failed: {e}",
            "success": False
        }
    
api_key = st.secrets["minecraft_mp_api_key"]

st.title("Check if an user has voted")
st.divider()
username_input = st.text_input("Enter username")

if st.button("Check Vote"):
    if api_key and username_input:
        result = check_vote_status(api_key, username_input)

        if result["status_code"] == 0:
            st.error(result["message"])
        elif result["status_code"] == 1:
            st.warning(result["message"])
        elif result["status_code"] == 2:
            st.success(result["message"])
        else:
            st.info(result["message"])