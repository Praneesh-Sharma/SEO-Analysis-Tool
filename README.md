# SEO Analysis Tool

This tool provides an easy way to analyze websites by evaluating SEO performance, generating PageSpeed Insights, and offering AI-powered SEO suggestions.

## Features:
- **Basic SEO Analysis**: Analyze a website’s SEO performance.
- **AI-Powered Suggestions**: Get actionable SEO improvement tips.
- **PageSpeed Insights**: Fetch and display website performance data.

## **Prerequisites**
- Python 3.7+
- API keys for:
  - Groq API (for using the Groq model)
  - Google PageSpeed API (for fetching PageSpeed Insights)

## Setup & Run Locally:

1. Clone the repository:
   ```
   git clone https://github.com/Praneesh-Sharma/SEO-Analysis-Tool.git
   ```

2. Create and Activacte Virtual Environment (for Windows)
   ```
   python -m venv venv
   venv\Scripts\activate
   ``` 

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Fill in your API keys in config/config.toml
   - Create a config/config.toml file in the root directory
   - On your Google Cloud console, enable the PageSpeed API from the Library, and then create a new API key from the Credentials tab
   - Add your API keys for Groq and Google API in this file. Here's the template:
    ```
    [groq]
    api_key = "YOUR_GROQ_API_KEY"
    
    [google_api]
    key = "YOUR_GOOGLE_API_KEY"
    ```

5. Run the application:
   ```
   streamlit run app.py
   ```
