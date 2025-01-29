import requests
from bs4 import BeautifulSoup
import textstat
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")

def analyze_seo(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title Found"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"] if meta_desc else "No Meta Description Found"

        # Header Tags
        headers = {f"H{i}": [h.get_text() for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

        # Keyword Density
        text_content = soup.get_text()
        words = word_tokenize(text_content.lower())
        word_freq = nltk.FreqDist(words)
        top_keywords = word_freq.most_common(10)

        # Readability Score
        readability = textstat.flesch_reading_ease(text_content)

        return {
            "URL": url,
            "Title": title,
            "Meta Description": meta_desc,
            "Headers": headers,
            "Top Keywords": top_keywords,
            "Readability Score": readability
        }
    except Exception as e:
        return {"error": str(e)}
