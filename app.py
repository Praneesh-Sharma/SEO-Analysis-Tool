import nltk
import streamlit as st
import pandas as pd
from seo_analysis import analyze_seo, format_output
from suggestions import generate_ai_suggestions
from pagespeed_insights import get_page_speed_insights

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
                pagespeed_insights = get_page_speed_insights(url)
                ai_suggestions = generate_ai_suggestions(seo_data)

                # Display Results
                st.subheader("📊 SEO Analysis Results")
                formatted_output = format_output(seo_data)
                st.markdown(formatted_output)

                # Display PageSpeed Insights
                st.subheader("🚀 PageSpeed Insights")
                if "error" not in pagespeed_insights:
                    st.write(f"**Performance Score**: {pagespeed_insights['Performance Score']}%")
                    st.write(f"**FCP (First Contentful Paint)**: {pagespeed_insights['FCP (First Contentful Paint)']}")
                    st.write(f"**LCP (Largest Contentful Paint)**: {pagespeed_insights['LCP (Largest Contentful Paint)']}")
                    st.write(f"**CLS (Cumulative Layout Shift)**: {pagespeed_insights['CLS (Cumulative Layout Shift)']}")
                    st.write(f"**TBT (Total Blocking Time)**: {pagespeed_insights['TBT (Total Blocking Time)']}")
                else:
                    st.error(f"❌ {pagespeed_insights['error']}")

                st.subheader("🤖 AI-Powered SEO Suggestions")
                st.write(ai_suggestions)

    else:
        st.error("❌ Please enter a valid URL")
