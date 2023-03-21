from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load two long articles
with open('chatGPTresult.txt', 'r', encoding='utf-8') as f:
    article1 = f.read()

with open('unknowenginer.txt', 'r', encoding='utf-8') as f:
    article2 = f.read()

# Calculate cosine similarity between articles
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([article1, article2])
cosine_sim = cosine_similarity(vectors[0], vectors[1])

print("Cosine similarity between the two articles:", cosine_sim[0][0])

''' w2v....py vd nn.py
Cosine similarity between the two articles: 0.1261650413399344

The two methods use different ways to compute similarity, which may lead to different results.

The first method uses a count vectorizer to represent each article as a bag-of-words model, and then computes the cosine similarity between the two articles based on the frequency of words they share.

The second method uses a TF-IDF vectorizer to represent each article, which takes into account not only the frequency of words but also their importance in distinguishing between articles. This may lead to a more accurate representation of the articles and a more accurate computation of similarity.

In general, the second method is more commonly used and considered more accurate for text similarity tasks.
'''
