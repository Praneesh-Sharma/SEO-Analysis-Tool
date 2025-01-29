import toml
import groq

config = toml.load("config.toml")
GROQ_API_KEY = config["GROQ"]["API_KEY"]

def generate_ai_suggestions(seo_data):
    prompt = f"""
    Analyze the following SEO data and suggest improvements:

    Title: {seo_data.get("Title", "N/A")}
    Meta Description: {seo_data.get("Meta Description", "N/A")}
    Readability Score: {seo_data.get("Readability Score", "N/A")}
    Top Keywords: {seo_data.get("Top Keywords", "N/A")}

    Provide concise SEO improvement suggestions.
    """

    client = groq.Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are an SEO expert."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
