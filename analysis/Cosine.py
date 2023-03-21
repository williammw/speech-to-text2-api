# CountVectorizer and Cosine Similarity from sklearn:
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the two articles
with open('chatGPTresult.txt', 'r', encoding='utf-8') as f:
    article1 = f.read()
with open('unknowenginer.txt', 'r', encoding='utf-8') as f:
    article2 = f.read()

# Segment the articles into words using jieba
seg_list1 = jieba.cut(article1)
seg_list2 = jieba.cut(article2)
words1 = ' '.join(seg_list1)
words2 = ' '.join(seg_list2)

# Create a count vectorizer and fit it to the segmented words
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([words1, words2])

# Compute the cosine similarity between the two articles
cosine_sim = cosine_similarity(X)[0, 1]

print('Cosine similarity between the two articles:', cosine_sim)
# Cosine similarity between the two articles: 0.8954328809506952
