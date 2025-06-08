import streamlit as st
from cyberai.assessment import assess_website

st.title("Cyber Assessment Tool")
url = st.text_input("Website URL")
if st.button("Run Assessment") and url:
    with st.spinner("Scanning..."):
        result = assess_website(url)
    st.write(f"**Score:** {result['score']}")
    if result['issues']:
        st.subheader("Issues")
        for issue in result['issues']:
            st.write(f"- {issue}")
