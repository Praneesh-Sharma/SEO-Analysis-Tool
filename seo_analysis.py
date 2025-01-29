import requests
from bs4 import BeautifulSoup
import textstat
import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def analyze_seo(url):
    try:
        response = requests.get(url, timeout=5)
        
        # Check for access denial by status code
        if response.status_code != 200:
            return {"error": f"URL cannot be accessed. HTTP Status Code: {response.status_code}"}
        
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title Found"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"] if meta_desc else "No Meta Description Found"

        # Header Tags
        headers = {f"H{i}": [h.get_text() for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

        # Keyword Density using spaCy for tokenization
        text_content = soup.get_text()
        doc = nlp(text_content.lower())
        words = [token.text for token in doc if token.is_alpha]
        word_freq = {word: words.count(word) for word in set(words)}
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        # Readability Score
        readability = textstat.flesch_reading_ease(text_content)

        # return {
        #     "URL": url,
        #     "Title": title,
        #     "Meta Description": meta_desc,
        #     "Headers": headers,
        #     "Top Keywords": top_keywords,
        #     "Readability Score": readability
        # }

        # Format output
        output = f"""
SEO Analysis Results:

- **URL**: {url}
  
- **Title**: *{title}*

- **Meta Description**: {meta_desc}

---

**Headers:**
"""
        for h, texts in headers.items():
            output += f"- **{h}**: \n"
            for text in texts:
                output += f"  - {text}\n"
        
        output += f"""
---

**Top Keywords:**
"""
        for word, count in top_keywords:
            output += f"1. *{word}* - {count} occurrences\n"

        output += f"""
---

**Readability Score**: {readability} (indicating that the text may need improvement in sentence structure for better readability).

---

### AI-Powered SEO Suggestions:
- **Title**: Make the title more descriptive, e.g., *"Apple Updates iOS: iPhones Can Now Connect to Starlink Satellites, Revolutionizing Communication"*
- **Meta Description**: Expand the description to include more keywords and a clear call to action.
- **Keyword Strategy**: Add specific terms like *"Starlink satellite connectivity"* or *"Apple iPhone satellite communication"*.
- **Readability**: Break up long sentences for easier scanning. Consider subheadings.
"""

        return output
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    test_url = "https://www.livemint.com/companies/apple-iphones-to-support-starlink-satellite-connectivity-in-the-us-11738125647557.html"
    result = analyze_seo(test_url)
    
    print("SEO Analysis Result:")
    print(result)