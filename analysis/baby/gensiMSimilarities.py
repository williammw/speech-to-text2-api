import jieba
from gensim import corpora, models, similarities

# Sample texts to compare
# Load the two articles
with open('chatGPTresult.txt', 'r', encoding='utf-8') as f:
    text1 = f.read()
with open('unknowenginer.txt', 'r', encoding='utf-8') as f:
    text2 = f.read()

# Tokenize the texts using jieba
text1_tokens = list(jieba.cut(text1))
text2_tokens = list(jieba.cut(text2))

# Create dictionary and corpus using gensim
dictionary = corpora.Dictionary([text1_tokens, text2_tokens])
corpus = [dictionary.doc2bow(text) for text in [text1_tokens, text2_tokens]]

# Train TF-IDF model
tfidf = models.TfidfModel(corpus)

# Apply TF-IDF transformation to corpus
corpus_tfidf = tfidf[corpus]

# Create similarity index using cosine similarity
index = similarities.MatrixSimilarity(corpus_tfidf)

# Get similarity score between text1 and text2
similarity_score = index[corpus_tfidf[0]][1]

print(similarity_score)

'''
Building prefix dict from the default dictionary ...
Loading model from cache /var/folders/fs/1w6nxlhs1wb7jhmm34qjmcr40000gn/T/jieba.cache
Loading model cost 0.365 seconds.
Prefix dict has been built successfully.
0.0
'''