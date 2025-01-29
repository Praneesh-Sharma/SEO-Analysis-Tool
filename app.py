import streamlit as st
import pandas as pd
from seo_analysis import analyze_seo
from suggestions import generate_ai_suggestions

st.set_page_config(page_title="AI SEO Analysis Tool", layout="wide")
st.title("🚀 AI-Powered SEO Analysis Tool")

# User Input
url = st.text_input("🔗 Enter Website URL:", "")

if st.button("Analyze"):
    if url:
        with st.spinner("Analyzing..."):
            seo_data = analyze_seo(url)  # Call backend function
            ai_suggestions = generate_ai_suggestions(seo_data)

        # Display Results
        st.subheader("📊 SEO Analysis Results")
        st.json(seo_data)  # Display structured JSON data

        st.subheader("🤖 AI-Powered SEO Suggestions")
        st.write(ai_suggestions)

    else:
        st.error("❌ Please enter a valid URL")
