import requests
from bs4 import BeautifulSoup
import textstat
import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def analyze_seo(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title Found"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"] if meta_desc else "No Meta Description Found"

        # Header Tags
        headers = {f"H{i}": [h.get_text() for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

        # Keyword Density using spaCy
        text_content = soup.get_text()
        doc = nlp(text_content.lower())  # Process text with spaCy
        words = [token.text for token in doc if token.is_alpha]  # Extract only alphabetic tokens
        word_freq = {word: words.count(word) for word in set(words)}  # Count word frequencies
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

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

if __name__ == "__main__":
    test_url = "https://www.business-standard.com/world-news/apple-spacex-link-up-to-support-starlink-satellite-network-on-iphones-125012901655_1.html"
    result = analyze_seo(test_url)
    print("SEO Analysis Result:")
    print(result)
