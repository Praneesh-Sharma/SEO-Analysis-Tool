import subprocess
import spacy
import streamlit as st
from seo_analysis import analyze_seo, format_output
from suggestions import generate_ai_suggestions
from pagespeed_insights import get_page_speed_insights

# Automatically download en_core_web_sm resource if not present
@st.cache_resource
def download_en_core_web_sm():
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

download_en_core_web_sm()

# Try to load the model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    st.error("❌ Error: Could not load the 'en_core_web_sm' model. Please ensure it is installed.")

st.set_page_config(page_title="AI SEO Analysis Tool", layout="wide")
st.title("🚀 AI-Powered SEO Analysis Tool")

# Initialize session state for storing the results
if 'seo_data' not in st.session_state:
    st.session_state.seo_data = None
if 'ai_suggestions' not in st.session_state:
    st.session_state.ai_suggestions = None
if 'pagespeed_insights' not in st.session_state:
    st.session_state.pagespeed_insights = None

# User Input
url = st.text_input("🔗 Enter Website URL:", "")

if st.button("Analyze"):
    if url:
        with st.spinner("Analyzing..."):
            seo_data = analyze_seo(url)
            
            if "error" in seo_data:  # Check if there's an error in the response
                st.error(f"❌ {seo_data['error']}")
            else:
                # Save results in session state
                st.session_state.seo_data = seo_data
                ai_suggestions = generate_ai_suggestions(seo_data)
                st.session_state.ai_suggestions = ai_suggestions

                # Display SEO Results and AI Suggestions
                st.subheader("📊 Basic SEO Analysis Results")
                formatted_output = format_output(seo_data)
                st.markdown(formatted_output)

                st.subheader("🤖 AI-Powered SEO Suggestions")
                st.write(ai_suggestions)

# Show PageSpeed Insights if requested
if st.session_state.seo_data and st.button("Generate PageSpeed Insights"):
    with st.spinner("Fetching Insights..."):
        pagespeed_insights = get_page_speed_insights(url)
        st.session_state.pagespeed_insights = pagespeed_insights

        if "error" in pagespeed_insights:
            st.error(f"❌ {pagespeed_insights['error']}")
        else:
            st.subheader("🚀 PageSpeed Insights")
            st.write(f"**Performance Score**: {pagespeed_insights['Performance Score']}%")
            st.write(f"**FCP (First Contentful Paint)**: {pagespeed_insights['FCP (First Contentful Paint)']}") 
            st.write(f"**LCP (Largest Contentful Paint)**: {pagespeed_insights['LCP (Largest Contentful Paint)']}")
            st.write(f"**CLS (Cumulative Layout Shift)**: {pagespeed_insights['CLS (Cumulative Layout Shift)']}")
            st.write(f"**TBT (Total Blocking Time)**: {pagespeed_insights['TBT (Total Blocking Time)']}")
