import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def extract_keywords(query):
    words = word_tokenize(query.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    pos_tags = pos_tag(filtered_words)
    keywords = [word for word, pos in pos_tags if pos.startswith(('NN', 'VB', 'JJ'))]
    return keywords
