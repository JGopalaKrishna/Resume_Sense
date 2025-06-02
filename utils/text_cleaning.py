import re

def clean_text(text):
    text = text.lower()                             # Lowercase
    text = re.sub(r'[^a-z0-9\s\.-@]', '', text)     # Remove special characters and digits except spaces
    text = re.sub(r'\s+', ' ', text).strip()        # Remove extra spaces
    return text
