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

        # Return SEO analysis as a JSON-like structure
        seo_data = {
            "URL": url,
            "Title": title,
            "Meta Description": meta_desc,
            "Headers": headers,
            "Top Keywords": top_keywords,
            "Readability Score": readability
        }

        return seo_data
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def format_output(seo_data):
    output = f"""
SEO Analysis Results:

- **URL**: {seo_data['URL']}
  
- **Title**: *{seo_data['Title']}*

- **Meta Description**: {seo_data['Meta Description']}

---

**Headers:**
"""
    for h, texts in seo_data['Headers'].items():
        output += f"- **{h}**: \n"
        for text in texts:
            output += f"  - {text}\n"
    
    output += f"""
---

**Top Keywords:**
"""
    for word, count in seo_data['Top Keywords']:
        output += f"1. *{word}* - {count} occurrences\n"

    output += f"""
---

**Readability Score**: {seo_data['Readability Score']}
"""
    return output

if __name__ == "__main__":
    test_url = "https://www.livemint.com/companies/apple-iphones-to-support-starlink-satellite-connectivity-in-the-us-11738125647557.html"
    seo_data = analyze_seo(test_url)
    
    # Display SEO Analysis in formatted output
    if "error" not in seo_data:
        formatted_output = format_output(seo_data)
        print(formatted_output)
    else:
        print(seo_data["error"])
