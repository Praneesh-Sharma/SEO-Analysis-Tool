import nltk
import streamlit as st
from seo_analysis import analyze_seo, format_output
from suggestions import generate_ai_suggestions

# Automatically download punkt resource if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

st.set_page_config(page_title="AI SEO Analysis Tool", layout="wide")
st.title("🚀 AI-Powered SEO Analysis Tool")

# User Input
url = st.text_input("🔗 Enter Website URL:", "")

if st.button("Analyze"):
    if url:
        with st.spinner("Analyzing..."):
            seo_data = analyze_seo(url)
            
            if "error" in seo_data:  # Check if there's an error in the response
                st.error(f"❌ {seo_data['error']}")
            else:
                # Display SEO Results
                st.subheader("📊 Basic SEO Analysis Results")
                formatted_output = format_output(seo_data)
                st.markdown(formatted_output)

                # Generate AI Suggestions
                ai_suggestions = generate_ai_suggestions(seo_data)
                st.subheader("🤖 AI-Powered SEO Suggestions")
                st.write(ai_suggestions)

    else:
        st.error("❌ Please enter a valid URL")
