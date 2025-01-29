import toml
import requests
import os

config_path = os.path.join("config", "config.toml")

try:
    config = toml.load(config_path)
except FileNotFoundError:
    print(f"Error: The file {config_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

GOOGLE_API_KEY = config["google_api"]["key"]

def get_pagespeed_data(url, api_key):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
    response = requests.get(api_url)
    return response.json()

def get_page_speed_insights(url):
    """Extracts relevant PageSpeed Insights metrics (e.g., speed score, FCP, LCP, CLS, TBT)."""
    api_key = GOOGLE_API_KEY 
    data = get_pagespeed_data(url, api_key)
    
    # Check if 'lighthouseResult' exists in the response
    if 'lighthouseResult' not in data:
        return {"error": "PageSpeed Insights data not available for the provided URL."}
    
    try:
        lighthouse = data['lighthouseResult']
        performance_score = lighthouse['categories']['performance']['score'] * 100
        fcp = lighthouse['audits']['first-contentful-paint']['displayValue']
        lcp = lighthouse['audits']['largest-contentful-paint']['displayValue']
        cls = lighthouse['audits']['cumulative-layout-shift']['displayValue']
        tbt = lighthouse['audits']['total-blocking-time']['displayValue']
        
        insights = {
            "Performance Score": performance_score,
            "FCP (First Contentful Paint)": fcp,
            "LCP (Largest Contentful Paint)": lcp,
            "CLS (Cumulative Layout Shift)": cls,
            "TBT (Total Blocking Time)": tbt
        }
        return insights
    except KeyError as e:
        return {"error": f"KeyError: {str(e)} - Data may be missing or malformed."}

if __name__ == "__main__":
    test_url = "https://www.livemint.com/companies/apple-iphones-to-support-starlink-satellite-connectivity-in-the-us-11738125647557.html"
    insights = get_page_speed_insights(test_url)
    print("PageSpeed Insights for URL:", test_url)
    print(insights)
