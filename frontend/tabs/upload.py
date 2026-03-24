import streamlit as st

import api_client


def render():
    st.subheader("Add an Employee Profile")
    name = st.text_input("Name")
    title = st.text_input("Job Title")
    bio = st.text_area("Profile / Resume (free text)", height=200)
    col1, col2, col3 = st.columns(3)
    department = col1.text_input("Department")
    location = col2.text_input("Location")
    grade = col3.selectbox("Grade", [None, "junior", "mid", "senior", "lead"])

    if st.button("Upload"):
        if not name or not title or not bio:
            st.warning("Name, title, and profile text are required.")
            return
        payload = {"name": name, "title": title, "bio": bio}
        if department:
            payload["department"] = department
        if location:
            payload["location"] = location
        if grade:
            payload["grade"] = grade
        try:
            data = api_client.upload_employee(payload)
            st.success(data.get("message", "Uploaded!"))
            st.json(data.get("parsed_profile", {}))
        except Exception as e:
            st.error(str(e))
