import streamlit as st

from tabs import upload, search

st.set_page_config(page_title="TalentStream AI", layout="wide")
st.title("TalentStream AI")

tab_upload, tab_search = st.tabs(["Upload Employee", "Search Talent"])

with tab_upload:
    upload.render()

with tab_search:
    search.render()
