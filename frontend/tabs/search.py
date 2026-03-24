import streamlit as st

import api_client


def render():
    st.subheader("Search for Talent")
    query = st.text_input("Describe the candidate you're looking for")
    top_k = st.slider("Results to return", 1, 20, 5)

    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
            return
        try:
            results = api_client.search_talent(query, top_k)
        except Exception as e:
            st.error(str(e))
            return

        if not results:
            st.info("No matching candidates found.")
        for r in results:
            with st.expander(f"{r['name']} — {r['title']} (score: {r['score']:.3f})"):
                skills_display = (
                    ", ".join(
                        f"{s['name']} ({s.get('years_experience') or '?'}y)"
                        for s in r["skills"]
                    )
                    if r["skills"]
                    else "N/A"
                )
                st.write(f"**Skills:** {skills_display}")
                st.write(f"**Experience:** {r['years_experience']} years")
                st.write(f"**Department:** {r.get('department', 'N/A')}")
                st.write(f"**Grade:** {r.get('grade', 'N/A')}")
                st.write(f"**Location:** {r['location']}")
                st.write(f"**Bio:** {r['bio']}")
