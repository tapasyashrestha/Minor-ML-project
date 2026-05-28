import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Proactively download necessary NLTK resources
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Initialize stemmer and stop words set
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Preprocesses raw text:
    1. Converts to lowercase.
    2. Removes punctuation, special characters, and digits.
    3. Removes stopwords.
    4. Applies Porter stemming.
    
    Parameters:
    text (str): The raw text string.
    
    Returns:
    str: A cleaned, space-separated string of stemmed words.
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation, digits, and special characters
    # Keep only letters and whitespace
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # Split into words (tokenization)
    words = text.split()
    
    # Filter out stopwords and stem
    cleaned_words = [stemmer.stem(word) for word in words if word not in stop_words]
    
    # Rejoin into a single string
    return " ".join(cleaned_words)
